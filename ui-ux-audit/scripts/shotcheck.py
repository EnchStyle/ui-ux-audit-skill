#!/usr/bin/env python3
"""Checks that can be made from an image alone (ui-ux-audit skill): simulator, emulator or device screenshots of a
native app, or a picture of a design. Use uicheck.py instead whenever the screen can be rendered in a browser.

  python3 shotcheck.py shots/*.png --platform ios|android|web [--scale N] [--out out/]

--scale is device pixels per point (iPhone) or per density-independent pixel (Android). When it is not given it is
guessed from the image width and every size in points is labelled an estimate.

Every item says how it was obtained:
  measured   read directly from pixels (contrast of a text box, positions, sizes in pixels, the home indicator found)
  estimate   needs an assumption (sizes in points without --scale, font size from the height of a text line, what
             counts as a tappable control: an image cannot say what responds to touch)
It cannot see: what is tappable, hover or focus behaviour, accessible names, text scaling, anything off screen.
Needs Pillow. Text checks need the tesseract program and the pytesseract module; without them only the
whole-image checks run and the output says so.
"""
import argparse, glob, hashlib, json, os, sys

try:
    from PIL import Image
except ImportError:
    sys.exit('shotcheck: Pillow is not installed (pip install pillow).')
try:
    import pytesseract
    pytesseract.get_tesseract_version(); OCR = True
except Exception:
    OCR = False

MIN_TARGET = {'ios': 44, 'android': 48, 'web': 44}
MIN_TEXT = {'ios': 11, 'android': 12, 'web': 12}


def lum(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def guess_scale(w, platform):
    if platform == 'ios':
        return 3 if w >= 1100 else 2 if w >= 640 else 1
    if platform == 'android':
        return round(w / 412, 3) if w > 500 else 1
    return 2 if w >= 700 and w <= 900 else 1


def box_colours(img, box):
    """Background = most common colour in the box; text = mean of the 8% of pixels furthest from it in luminance."""
    x0, y0, x1, y1 = box; crop = img.crop((max(0, x0 - 2), max(0, y0 - 2), min(img.width, x1 + 2), min(img.height, y1 + 2)))
    raw = crop.tobytes(); px = [raw[i:i + 3] for i in range(0, len(raw), 3)]
    if len(px) < 12:
        return None
    counts = {}
    for p in px:
        k = (p[0] >> 3, p[1] >> 3, p[2] >> 3); counts[k] = counts.get(k, 0) + 1
    bk = max(counts, key=counts.get); bg_px = [p for p in px if (p[0] >> 3, p[1] >> 3, p[2] >> 3) == bk]
    bg = tuple(sum(p[i] for p in bg_px) // len(bg_px) for i in range(3)); lb = lum(bg)
    far = sorted(px, key=lambda p: -abs(lum(p) - lb))[:max(3, len(px) * 8 // 100)]
    fg = tuple(sum(p[i] for p in far) // len(far) for i in range(3))
    return fg, bg


def text_lines(img):
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config='--psm 11')
    lines = {}
    for i, t in enumerate(d['text']):
        t = t.strip()
        try:
            conf = float(d['conf'][i])
        except Exception:
            conf = -1
        if not t or conf < 45:
            continue
        k = (d['block_num'][i], d['par_num'][i], d['line_num'][i]); x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
        L = lines.setdefault(k, {'words': [], 'x0': x, 'y0': y, 'x1': x + w, 'y1': y + h})
        L['words'].append(t); L['x0'] = min(L['x0'], x); L['y0'] = min(L['y0'], y); L['x1'] = max(L['x1'], x + w); L['y1'] = max(L['y1'], y + h)
    out = []
    for L in lines.values():
        txt = ' '.join(L['words'])
        if len(txt) < 2 or L['y1'] - L['y0'] < 6:
            continue
        out.append({'text': txt[:60], 'box': [L['x0'], L['y0'], L['x1'], L['y1']]})
    return sorted(out, key=lambda l: (l['box'][1], l['box'][0]))


def home_indicator(img, scale):
    """Find the home-indicator bar: a centred, uniform horizontal bar about a third of the width in the bottom strip."""
    W, H = img.size; band = int(H * 0.06); px = img.load(); rows = []
    for y in range(H - band, H):
        edge = px[int(W * 0.08), y]; mid = px[W // 2, y]
        if ratio(edge, mid) < 1.6:
            continue
        l = W // 2
        while l > 0 and ratio(px[l, y], mid) < 1.15: l -= 1
        r = W // 2
        while r < W - 1 and ratio(px[r, y], mid) < 1.15: r += 1
        if 0.25 * W <= r - l <= 0.45 * W and abs((l + r) / 2 - W / 2) < 0.03 * W:
            rows.append((y, l, r))
    if len(rows) < 2:
        return None
    top, bottom = rows[0][0], rows[-1][0]
    if bottom - top + 1 > 12 * scale or bottom - top + 1 != len(rows):
        return None
    return {'top': top, 'bottom': bottom, 'height_px': bottom - top + 1, 'left': rows[0][1], 'right': rows[0][2]}


def filled_region(img, box, page_bg):
    """If the text sits on a filled shape (a button or chip), grow outward to the shape's edges. Returns its box or None."""
    cols = box_colours(img, box)
    if not cols or ratio(cols[1], page_bg) < 1.12:
        return None
    bg = cols[1]; px = img.load(); W, H = img.size; x0, y0, x1, y1 = box; cy = (y0 + y1) // 2; cx = (x0 + x1) // 2
    same = lambda p: abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) < 36
    l = x0
    while l > 0 and (same(px[l - 1, cy]) or same(px[l - 1, y0 - 1 if y0 > 0 else 0])): l -= 1
    r = x1
    while r < W - 1 and (same(px[r + 1, cy]) or same(px[r + 1, y0 - 1 if y0 > 0 else 0])): r += 1
    t = y0
    while t > 0 and same(px[max(l + 2, min(cx, W - 1)), t - 1]): t -= 1
    b = y1
    while b < H - 1 and same(px[max(l + 2, min(cx, W - 1)), b + 1]): b += 1
    if r - l >= W * 0.97 or b - t >= H * 0.5:
        return None                                  # a band or panel, not a control
    return [l, t, r, b]


def check(path, platform, scale=None):
    img = Image.open(path).convert('RGB'); W, H = img.size
    guessed = scale is None; scale = scale or guess_scale(W, platform)
    pt = lambda v: round(v / scale, 1); basis_pt = 'estimate (scale guessed from width)' if guessed else 'measured'
    small = img.resize((64, 64)); raw = small.tobytes(); mean = sum(lum(raw[i:i + 3]) for i in range(0, len(raw), 3)) / (64 * 64)
    corners = [img.getpixel((W // 2, int(H * f))) for f in (0.12, 0.3, 0.5, 0.7)]; page_bg = max(set(corners), key=corners.count)
    r = {'image': os.path.basename(path), 'pixels': [W, H], 'scale': scale, 'scale_basis': 'guessed from width' if guessed else 'given', 'points': [pt(W), pt(H)],
         'appearance': 'dark' if mean < 0.2 else 'light', 'ocr': OCR, 'contrast-text': [], 'small-text': [], 'target-touch': [], 'safe-area': [], 'content-cut-off': [], 'edge-near-miss': [], 'text-clipped': [], 'nav-structure': []}
    ind = home_indicator(img, scale) if platform != 'web' else None
    r['home_indicator'] = ({'found': True, 'top_px': ind['top'], 'basis': 'measured'} if ind else {'found': False, 'note': 'bottom safe area not assessed' if platform != 'web' else 'not applicable'})
    if not OCR:
        r['note'] = 'pytesseract or tesseract not available: text, target and alignment checks were not run'
        return r
    lines = text_lines(img); r['text_lines_read'] = len(lines)
    zone_top = (ind['top'] - 2 * ind['height_px']) if ind else None
    lefts = {}
    for L in lines:
        x0, y0, x1, y1 = L['box']; h = y1 - y0; size_pt = pt(h / 0.72)
        if zone_top is not None and y1 > zone_top:
            r['safe-area'].append({'text': L['text'], 'edge': 'bottom', 'overlap_px': y1 - zone_top, 'basis': 'measured (content inside the home-indicator zone found in the image)'})
        if sum(ch.isalnum() for ch in L['text']) < 3 or y1 < H * 0.055:
            continue                                  # an icon read as characters, or the system status bar: not text to judge
        cols = box_colours(img, L['box'])
        if cols:
            c = ratio(*cols); need = 3 if (size_pt >= 18) else 4.5
            if c < need:
                r['contrast-text'].append({'text': L['text'], 'ratio': round(c, 2), 'need': need, 'text_colour': '#%02x%02x%02x' % cols[0], 'background': '#%02x%02x%02x' % cols[1], 'box': L['box'], 'basis': 'measured from the pixels of the text box (anti-aliasing lowers the reading slightly)'})
        if size_pt < MIN_TEXT[platform] - 0.5:
            r['small-text'].append({'text': L['text'], 'line_height_px': h, 'approx_size': size_pt, 'minimum': MIN_TEXT[platform], 'basis': 'estimate (font size taken as line height / 0.72' + ('; scale guessed' if guessed else '') + ')'})
        if x0 <= 1 or x1 >= W - 2:
            r['content-cut-off'].append({'text': L['text'], 'box': L['box'], 'basis': 'measured (text touches the image edge)'})
        if L['text'].endswith(('…', '...')):
            r['text-clipped'].append({'text': L['text'], 'basis': 'measured (ends with an ellipsis: check that the full text can be reached)'})
        reg = filled_region(img, L['box'], page_bg)
        if reg:
            w_pt, h_pt = pt(reg[2] - reg[0]), pt(reg[3] - reg[1])
            if min(w_pt, h_pt) < MIN_TARGET[platform] - 0.5 and h_pt >= 14:
                r['target-touch'].append({'text': L['text'], 'shape_points': [w_pt, h_pt], 'minimum': MIN_TARGET[platform], 'basis': 'estimate (a filled shape around text is assumed to be a control; its touch area may be larger than what is drawn)'})
        lefts.setdefault(round(x0 / scale), []).append(L)
    common = [k for k, v in lefts.items() if len(v) >= 3]
    for k, v in lefts.items():
        if len(v) <= 2:
            near = [c for c in common if 2 <= abs(c - k) <= 6]
            if near:
                r['edge-near-miss'].append({'text': v[0]['text'], 'left_points': k, 'common_edge_points': near[0], 'basis': 'estimate (text edges from character recognition; confirm by eye)'})
    bar = [L for L in lines if L['box'][1] > H * 0.88 and (zone_top is None or L['box'][3] <= zone_top + 4)]
    rows = {}
    for L in bar:
        rows.setdefault(round(L['box'][1] / (8 * scale)), []).append(L)
    if rows:
        best = max(rows.values(), key=len)
        if len(best) > 5:
            r['nav-structure'].append({'labels_in_bottom_bar': [L['text'] for L in best], 'count': len(best), 'basis': 'estimate (text items found in one row at the bottom of the screen)'})
    return r


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Checks that can be made from screenshots alone.')
    ap.add_argument('images', nargs='+'); ap.add_argument('--platform', choices=['ios', 'android', 'web'], required=True)
    ap.add_argument('--scale', type=float); ap.add_argument('--out'); ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    files = [f for pat in a.images for f in (sorted(glob.glob(pat)) or [pat])]
    for f in files:
        if not os.path.exists(f):
            sys.exit(f'shotcheck: file not found: {f}')
    res = {'tool': 'shotcheck 1', 'platform': a.platform, 'images': [check(f, a.platform, a.scale) for f in files]}
    res['run_id'] = hashlib.sha1(json.dumps(res, sort_keys=True).encode()).hexdigest()[:8]
    if a.out:
        os.makedirs(a.out, exist_ok=True); json.dump(res, open(os.path.join(a.out, 'shotcheck.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    KEYS = ['contrast-text', 'small-text', 'target-touch', 'safe-area', 'content-cut-off', 'text-clipped', 'edge-near-miss', 'nav-structure']
    for r in res['images']:
        print(f"# shotcheck run {res['run_id']}: {r['image']}  {r['pixels'][0]}x{r['pixels'][1]}px = {r['points'][0]}x{r['points'][1]} points at scale {r['scale']} ({r['scale_basis']})  appearance: {r['appearance']}")
        print(f"home indicator: {'found at y=' + str(r['home_indicator']['top_px']) + 'px (measured)' if r['home_indicator']['found'] else r['home_indicator']['note']} | text lines read: {r.get('text_lines_read', 'none: ' + r.get('note', ''))}")
        print('candidates: ' + (' | '.join(f"{k} {len(r[k])}" for k in KEYS if r[k]) or 'none'))
        if not a.quiet:
            for k in KEYS:
                for it in r[k][:6]:
                    print(f"- [{k}] " + json.dumps({x: y for x, y in it.items() if x != 'box'}, ensure_ascii=False))
                if len(r[k]) > 6:
                    print(f"- [{k}] ... {len(r[k]) - 6} more in shotcheck.json")
        print()
    print('Not visible in an image: what is tappable, hover and focus behaviour, accessible names, text scaling, off-screen content. List these under Verify.')
    print(f"Quote in the report header: shotcheck run {res['run_id']}")
