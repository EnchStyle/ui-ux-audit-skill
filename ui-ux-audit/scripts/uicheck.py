#!/usr/bin/env python3
"""Measured UI checks for a local HTML file or URL at 360, 768 and 1280 px (ui-ux-audit skill).

Prints counts per width, then the candidate items (merged across widths). Candidates are not
findings: confirm each on the screenshots and group items with one cause.

Usage:
  python3 uicheck.py PAGE [--json out.json] [--shots DIR] [--widths 360,768,1280]
                          [--dark] [--height 900]

PAGE is a local .html file or an http(s) URL. Needs Python Playwright with Chromium.

What it measures (per viewport unless noted):
  overflow        page wider than the viewport (horizontal scroll)
  contrast        text below WCAG AA (4.5:1, 3:1 for large text) against the nearest
                  opaque background; text over gradients or images is listed as
                  'unknown' so it can be checked by eye or by pixel sampling
  targets         interactive elements under 44px (and under 24px, the hard floor)
  names           controls with no accessible name; clickable div/span not reachable
  media           img/video/iframe/svg-img with no width+height or aspect-ratio
  headings        skipped heading levels
  small_text      text under 12px
  widows          headings, titles and short text whose last line is a single word;
                  button labels that wrap
  grid_orphans    grid or wrapping rows whose last row holds a single item
  card_rows       sibling cards in one row whose matching inner parts (title, chips,
                  price, button) do not share a vertical position
  baselines       sibling tiles whose main value (largest text) is not on one line
  control_heights inputs, selects and buttons side by side at different heights
  nested_radius   inner corners that do not follow the outer corner (inner radius
                  should be about outer radius minus the inset)
  near_miss_edges left edges within 1 to 6px of a common alignment line
  pad_asymmetry   boxes whose bottom space is visibly larger or smaller than the top
                  because of a first or last child's margin
  ratios          sibling media in one set with different aspect ratios
  icon_sizes      icons in sibling controls at different sizes
  heading_prox    headings that sit closer to the previous block than to their own
                  content
  census          distinct radii, shadows, font sizes, font families and section
                  paddings (for token drift; not failures by themselves)
  focus_invisible (widest viewport) focusable elements whose look does not change on
                  keyboard focus
  gutters         distinct horizontal gaps between sibling cards (drift when one level differs)
  chip_heights    small repeated components (chips, badges, pills) at different heights
  table_align     table headers aligned differently from their column, numeric columns not right-aligned
  table_sticky    tables with more than 15 body rows and no sticky header
"""
import json, os, argparse
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const out = {contrast: [], contrast_unknown: 0, targets: [], names: [], media: [], headings: [], small_text: [],
    widows: [], grid_orphans: [], card_rows: [], baselines: [], control_heights: [], nested_radius: [],
    near_miss_edges: [], pad_asymmetry: [], ratios: [], icon_sizes: [], heading_prox: [], census: {}};
  const cs = el => getComputedStyle(el);
  const vis = el => { if (!el || !el.getBoundingClientRect) return false; const s = cs(el); const r = el.getBoundingClientRect();
    return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05 && r.width > 0 && r.height > 0; };
  const sel = el => { if (el.id) return '#' + el.id; let s = el.tagName.toLowerCase();
    if (el.classList.length) s += '.' + [...el.classList].slice(0,2).join('.');
    let p = el.parentElement, hops = 0; while (p && !p.id && hops < 3) { p = p.parentElement; hops++; }
    if (p && p.id) s = '#' + p.id + ' ' + s; return s; };
  const txt = el => (el.innerText || el.textContent || '').trim().replace(/\s+/g,' ').slice(0, 50);
  const parse = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b); };
  const blend = (fg, bg) => ({r: fg.r*fg.a + bg.r*(1-fg.a), g: fg.g*fg.a + bg.g*(1-fg.a), b: fg.b*fg.a + bg.b*(1-fg.a), a: 1});
  const bgOf = el => { const layers = []; let e = el;
    while (e && e.nodeType === 1) { const s = cs(e);
      if (s.backgroundImage && s.backgroundImage !== 'none') return {unknown: true};
      const c = parse(s.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= 0.99) break; }
      e = e.parentElement; }
    let base = {r:255, g:255, b:255, a:1};
    const rootBg = parse(cs(document.documentElement).backgroundColor);
    if (rootBg && rootBg.a > 0.99 && layers.length === 0) base = rootBg;
    for (let i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return base; };
  const hasBox = el => { const s = cs(el); const bg = parse(s.backgroundColor);
    return (bg && bg.a > 0.05) || (s.backgroundImage !== 'none') || parseFloat(s.borderTopWidth) > 0 || s.boxShadow !== 'none'; };
  const isInteractive = el => el.matches('a[href], button, input, select, textarea, [role=button], [onclick], [tabindex]:not([tabindex="-1"])');

  // ---- text: contrast, small text
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) { const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const el = t.parentElement; if (!el || seen.has(el) || !vis(el)) continue; seen.add(el);
    if (['SCRIPT','STYLE','NOSCRIPT','TITLE'].includes(el.tagName)) continue;
    const s = cs(el); const size = parseFloat(s.fontSize); const weight = parseInt(s.fontWeight) || 400;
    if (size < 12) out.small_text.push({sel: sel(el), px: size, text: t.textContent.trim().slice(0,40)});
    const fg = parse(s.color); if (!fg) continue; const bg = bgOf(el);
    if (bg.unknown) { out.contrast_unknown++; continue; }
    let op = 1, e2 = el; while (e2 && e2.nodeType === 1) { op *= parseFloat(cs(e2).opacity); e2 = e2.parentElement; }
    const f = blend({...fg, a: fg.a * op}, bg);
    const L1 = lum(f), L2 = lum(bg); const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need) out.contrast.push({sel: sel(el), ratio: +ratio.toFixed(2), need, px: size, text: t.textContent.trim().slice(0,40)});
  }

  // ---- interactive: targets + names
  const inter = [...document.querySelectorAll('a[href], button, input, select, textarea, [role=button], [onclick], [tabindex]:not([tabindex="-1"])')];
  for (const el of inter) { if (!vis(el) || el.type === 'hidden') continue; const r = el.getBoundingClientRect();
    const inline = el.tagName === 'A' && cs(el).display === 'inline' && el.closest('p, li, td, figcaption, small');
    if (!inline && (r.width < 44 || r.height < 44)) out.targets.push({sel: sel(el), w: Math.round(r.width), h: Math.round(r.height), hard: (r.width < 24 || r.height < 24)});
    let name = (el.getAttribute('aria-label') || el.getAttribute('title') || '').trim();
    if (!name && el.getAttribute('aria-labelledby')) name = el.getAttribute('aria-labelledby').split(' ').map(id => (document.getElementById(id)||{}).textContent || '').join(' ');
    if (!name && ['INPUT','SELECT','TEXTAREA'].includes(el.tagName)) { if (el.id) { const l = document.querySelector(`label[for="${el.id}"]`); if (l) name = l.textContent; }
      if (!name && el.closest('label')) name = el.closest('label').textContent; }
    else if (!name) name = (el.innerText || el.value || '').trim() || [...el.querySelectorAll('img[alt], svg[aria-label]')].map(i => i.getAttribute('alt') || i.getAttribute('aria-label')).join(' ');
    if (!String(name).trim()) out.names.push({sel: sel(el), tag: el.tagName.toLowerCase(), placeholder: el.getAttribute('placeholder') || null});
    if ((el.tagName === 'DIV' || el.tagName === 'SPAN' || el.tagName === 'LI') && el.hasAttribute('onclick') && !el.hasAttribute('tabindex'))
      out.names.push({sel: sel(el), issue: 'clickable ' + el.tagName.toLowerCase() + ' not reachable by keyboard'});
  }

  // ---- media, headings
  for (const m of document.querySelectorAll('img, video, iframe')) { const s = cs(m);
    const hasAttr = m.getAttribute('width') && m.getAttribute('height'); const ar = s.aspectRatio && s.aspectRatio !== 'auto';
    if (!hasAttr && !ar) out.media.push({sel: sel(m)}); }
  let prev = 0; for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) { if (!vis(h)) continue; const l = +h.tagName[1];
    if (prev && l > prev + 1) out.headings.push({sel: sel(h), from: prev, to: l, text: txt(h)}); prev = l; }

  // ---- widows and wrapping labels
  const lineTops = el => { const tops = []; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) { const n = w.currentNode; const re = /\S+/g; let m;
      while ((m = re.exec(n.textContent))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const rects = rg.getClientRects(); if (!rects.length) continue; tops.push({t: Math.round(rects[0].top), w: m[0]}); } }
    const lines = []; for (const x of tops) { const L = lines.find(l => Math.abs(l.t - x.t) <= 4); if (L) L.words.push(x.w); else lines.push({t: x.t, words: [x.w]}); }
    lines.sort((a,b) => a.t - b.t); return lines; };
  const widowCands = new Set([...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[class*=title],[class*=headline],[class*=lede],figcaption,blockquote,dt,th,legend,label')]);
  for (const el of document.querySelectorAll('p, li, span, div')) { if (el.children.length === 0 && vis(el)) { const s = cs(el); const t = txt(el);
      if (t.length > 0 && t.length < 160 && parseFloat(s.fontSize) >= 17) widowCands.add(el); } }
  for (const el of widowCands) { if (!vis(el) || el.closest('th, td, nav, svg')) continue; const lines = lineTops(el);
    if (lines.length >= 2 && lines.length <= 4) { const last = lines[lines.length - 1], before = lines[lines.length - 2];
      if (last.words.length === 1 && before.words.length >= 2 && !/^\(.*\)$/.test(last.words[0]))
        out.widows.push({sel: sel(el), lines: lines.length, last_line: last.words.join(' '), text: txt(el)}); } }
  for (const el of document.querySelectorAll('button, a[class*=btn], a[class*=button], a[class*=cta], [role=button]')) { if (!vis(el)) continue;
    const lines = lineTops(el); if (lines.length >= 2) out.widows.push({sel: sel(el), lines: lines.length, issue: 'control label wraps', text: txt(el)}); }

  // ---- sibling groups (same parent, same class) and rows
  const groups = [];
  for (const parent of document.querySelectorAll('body *')) { if (!vis(parent)) continue;
    const kids = [...parent.children].filter(vis); if (kids.length < 2) continue;
    const byClass = {}; for (const k of kids) { const c = k.tagName + '.' + [...k.classList].sort().join('.'); (byClass[c] = byClass[c] || []).push(k); }
    for (const els of Object.values(byClass)) if (els.length >= 2) groups.push({parent, els}); }
  const rowsOf = els => { const rows = []; for (const e of els) { const t = e.getBoundingClientRect().top; const R = rows.find(r => Math.abs(r.t - t) <= 3); if (R) R.els.push(e); else rows.push({t, els: [e]}); }
    return rows.sort((a,b) => a.t - b.t); };

  for (const {parent, els} of groups) {
    const ps = cs(parent); const layoutParent = ps.display.includes('grid') || (ps.display.includes('flex') && ps.flexWrap === 'wrap');
    const rows = rowsOf(els);
    // grid orphans
    if (layoutParent && els.length >= 3 && rows.length >= 2) { const first = rows[0].els.length, last = rows[rows.length-1].els.length;
      if (last === 1 && first >= 3) out.grid_orphans.push({sel: sel(parent), items: els.length, per_row: first, last_row: last}); }
    for (const row of rows) { if (row.els.length < 2) continue; const cards = row.els;
      const boxy = cards.every(c => hasBox(c) || c.children.length >= 2);
      // inner row alignment: compare matching children by structure
      const sig = c => [...c.querySelectorAll('*')].filter(vis).filter(d => d.tagName === 'svg' || !d.closest('svg')).filter(d => d.children.length === 0 || isInteractive(d) || d.tagName === 'IMG' || d.tagName === 'svg')
                        .map(d => ({d, k: d.tagName + '.' + [...d.classList].sort().join('.')}));
      if (boxy && cards.length >= 2 && cards[0].getBoundingClientRect().height > 60) {
        const sigs = cards.map(sig); const common = sigs[0].map(x => x.k).filter(k => sigs.every(s => s.some(y => y.k === k)));
        const maxLen = Math.max(...sigs.map(s => new Set(s.map(y => y.k)).size));
        if (new Set(common).size < 2 || new Set(common).size / maxLen < 0.6) continue;
        const seenK = new Set(); let worst = null;
        for (const k of common) { if (seenK.has(k)) continue; seenK.add(k);
          const tops = sigs.map(s => { const hit = s.filter(y => y.k === k); return hit[hit.length - 1].d.getBoundingClientRect().top; });
          const cardTops = cards.map(c => c.getBoundingClientRect().top);
          const rel = tops.map((t, i) => t - cardTops[i]); const spread = Math.max(...rel) - Math.min(...rel);
          if (spread > 4 && (!worst || spread > worst.spread)) worst = {part: k.toLowerCase(), spread: Math.round(spread)}; }
        if (worst) out.card_rows.push({sel: sel(cards[0]), cards: cards.length, part: worst.part, spread_px: worst.spread}); }
      // baselines of main values
      if (boxy && cards.length >= 2) { const bigs = cards.map(c => { let best = null, bs = 0; for (const d of c.querySelectorAll('*')) { if (!vis(d) || ![...d.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
          const f = parseFloat(cs(d).fontSize); if (f > bs && txt(d)) { bs = f; best = d; } } return best ? {d: best, f: bs} : null; });
        if (bigs.every(Boolean) && bigs.every(b => Math.abs(b.f - bigs[0].f) < 0.5) && bigs[0].f >= 20) {
          const bots = bigs.map(b => b.d.getBoundingClientRect().bottom); const sp = Math.max(...bots) - Math.min(...bots);
          if (sp > 3) out.baselines.push({sel: sel(cards[0]), tiles: cards.length, value_px: bigs[0].f, spread_px: Math.round(sp)}); } }
      // ratios of media in the set
      const med = cards.map(c => [...c.querySelectorAll('img, video, picture, svg, canvas, [class*=media], [class*=thumb], [class*=image]')].filter(vis)[0]).filter(Boolean);
      if (med.length === cards.length) { const rs = med.map(m => { const r = m.getBoundingClientRect(); return r.width / r.height; });
        const mn = Math.min(...rs), mx = Math.max(...rs); if (mn > 0 && mx / mn > 1.03 && med[0].getBoundingClientRect().width > 40)
          out.ratios.push({sel: sel(med[0]), set: med.length, ratios: rs.map(x => +x.toFixed(2))}); }
      // icon sizes in sibling controls
      const icons = cards.map(c => c.querySelector('svg, i, img[class*=icon]')).filter(i => i && vis(i));
      if (icons.length === cards.length && icons.length >= 2) { const ws = icons.map(i => Math.round(i.getBoundingClientRect().width));
        if (Math.max(...ws) - Math.min(...ws) > 1 && Math.max(...ws) <= 64) out.icon_sizes.push({sel: sel(cards[0]), sizes: ws}); }
    }
  }

  // ---- control heights side by side
  const ctrls = [...document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=hidden]), select, button, a[class*=btn], a[class*=button], a[class*=cta]')].filter(vis);
  for (let i = 0; i < ctrls.length; i++) for (let j = i + 1; j < ctrls.length; j++) { const a = ctrls[i].getBoundingClientRect(), b = ctrls[j].getBoundingClientRect();
    const gap = Math.max(b.left - a.right, a.left - b.right); const vOverlap = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (gap >= -1 && gap <= 24 && vOverlap > Math.min(a.height, b.height) * 0.5 && Math.abs(a.height - b.height) > 2)
      out.control_heights.push({a: sel(ctrls[i]), b: sel(ctrls[j]), h: [Math.round(a.height), Math.round(b.height)]}); }

  // ---- nested radius
  const rad = el => parseFloat(cs(el).borderTopLeftRadius) || 0;
  for (const outer of document.querySelectorAll('body *')) { if (!vis(outer) || !hasBox(outer)) continue; const R = rad(outer); if (R < 6) continue;
    const ro = outer.getBoundingClientRect();
    for (const inner of outer.querySelectorAll('*')) { if (inner === outer || !vis(inner)) continue; if (!(hasBox(inner) || inner.tagName === 'IMG')) continue;
      const ri = inner.getBoundingClientRect(); const dx = ri.left - ro.left, dy = ri.top - ro.top;
      if (dx < 1 || dy < 1 || dx > 28 || dy > 28 || Math.abs(dx - dy) > 3) continue;
      if (ri.width < ro.width * 0.5 || ri.height < ro.height * 0.3) continue;
      const r = rad(inner); if (r === 0) continue; const expected = Math.max(0, R - dx);
      if (r > expected + 4 && r >= R * 0.75) out.nested_radius.push({outer: sel(outer), inner: sel(inner), outer_r: R, inset: Math.round(dx), inner_r: r, expected: Math.round(expected)});
      break; } }

  // ---- near-miss left edges
  const blocks = [...document.querySelectorAll('h1,h2,h3,h4,p,ul,ol,table,figure,img,svg,form,section > div, main > div, article, [class*=card], [class*=tile], [class*=panel]')]
    .filter(vis).filter(e => { const r = e.getBoundingClientRect(); const s = cs(e); return r.width >= 120 && !(s.textAlign === 'center' && /^(H\d|P)$/.test(e.tagName)) && !e.closest('nav, header nav, footer'); });
  const edges = {}; for (const b of blocks) { const x = Math.round(b.getBoundingClientRect().left); (edges[x] = edges[x] || []).push(b); }
  const keys = Object.keys(edges).map(Number);
  for (const x of keys) { if (edges[x].length > 2) continue;
    const near = keys.filter(y => y !== x && Math.abs(y - x) >= 2 && Math.abs(y - x) <= 6 && edges[y].length >= 3);
    if (near.length) out.near_miss_edges.push({sel: sel(edges[x][0]), x, common_edge: near[0], off_by: Math.abs(near[0] - x), common_count: edges[near[0]].length}); }

  // ---- padding asymmetry caused by first/last child margins
  const enclosed = el => { const s = cs(el); const bg = parse(s.backgroundColor); const pbg = el.parentElement ? bgOf(el.parentElement) : null;
    const bgDiff = bg && bg.a > 0.05 && pbg && !pbg.unknown && (Math.abs(bg.r - pbg.r) + Math.abs(bg.g - pbg.g) + Math.abs(bg.b - pbg.b) > 6);
    const allBorders = ['Top','Right','Bottom','Left'].every(k => parseFloat(s['border' + k + 'Width']) > 0);
    return bgDiff || allBorders || s.boxShadow !== 'none'; };
  for (const box of document.querySelectorAll('body *')) { if (!vis(box) || !enclosed(box)) continue; const kids = [...box.children].filter(vis); if (kids.length < 2) continue;
    const s = cs(box); if (s.display.includes('grid') || (s.display.includes('flex') && s.flexDirection.startsWith('row'))) continue;
    const r = box.getBoundingClientRect(); if (r.height > 900 || r.height < 40) continue;
    const bt = parseFloat(s.borderTopWidth), bb = parseFloat(s.borderBottomWidth);
    const first = kids[0], last = kids[kids.length - 1];
    const top = first.getBoundingClientRect().top - r.top - bt, bottom = r.bottom - bb - last.getBoundingClientRect().bottom;
    const mb = parseFloat(cs(last).marginBottom), mt = parseFloat(cs(first).marginTop);
    if (Math.min(top, bottom) >= 4 && ((bottom - top > 8 && mb > 0) || (top - bottom > 8 && mt > 0))) out.pad_asymmetry.push({sel: sel(box), top: Math.round(top), bottom: Math.round(bottom), cause: bottom > top ? 'last child margin-bottom ' + mb + 'px' : 'first child margin-top ' + mt + 'px'}); }

  // ---- heading proximity
  for (const h of document.querySelectorAll('h2, h3')) { if (!vis(h)) continue; const p = h.previousElementSibling, n = h.nextElementSibling;
    if (!p || !n || !vis(p) || !vis(n)) continue; const r = h.getBoundingClientRect();
    if (parseFloat(cs(p).fontSize) < parseFloat(cs(h).fontSize) * 0.8 && txt(p).length < 60 && p.getBoundingClientRect().height < 40) continue;
    const above = r.top - p.getBoundingClientRect().bottom, below = n.getBoundingClientRect().top - r.bottom;
    if (above >= 0 && below > above) out.heading_prox.push({sel: sel(h), above: Math.round(above), below: Math.round(below), text: txt(h)}); }

  // ---- gutters between sibling cards (measured), chip height drift, table header alignment
  out.gutters = []; out.chip_heights = []; out.table_align = [];
  const gapVals = {};
  for (const {parent, els} of groups) { const rows = rowsOf(els);
    for (const row of rows) { if (row.els.length < 2 || !row.els.every(hasBox) || row.els.some(e => /^(TR|TD|TH|LI|BUTTON|A|INPUT|SELECT)$/.test(e.tagName))) continue;
      const xs = row.els.map(e => e.getBoundingClientRect()).sort((a,b) => a.left - b.left);
      if (xs.some(r => r.height < 60 || r.width < 120)) continue;
      for (let i = 1; i < xs.length; i++) { const g = Math.round(xs[i].left - xs[i-1].right); if (g < 0 || g > 80) continue;
        (gapVals[g] = gapVals[g] || new Set()).add(sel(parent)); } } }
  const gk = Object.keys(gapVals).map(Number).sort((a,b) => a-b);
  if (gk.length > 1) out.gutters.push({horizontal_gaps_px: gk, where: Object.fromEntries(gk.map(k => [k, [...gapVals[k]].slice(0,4)]))});
  const chips = {};
  for (const el of document.querySelectorAll('body *')) { if (!vis(el) || !hasBox(el) || !el.classList.length) continue;
    const r = el.getBoundingClientRect(); const t = txt(el); if (r.height > 40 || r.height < 12 || !t || t.length > 32) continue;
    const k = el.classList[0]; (chips[k] = chips[k] || []).push({h: Math.round(r.height * 2) / 2, sel: sel(el), t}); }
  for (const [k, list] of Object.entries(chips)) { if (list.length < 3) continue; const hs = [...new Set(list.map(x => x.h))];
    if (Math.max(...hs) - Math.min(...hs) > 1.5) out.chip_heights.push({component: '.' + k, heights: hs.sort((a,b)=>a-b), examples: list.slice(0,3).map(x => x.t)}); }
  for (const tb of document.querySelectorAll('table')) { if (!vis(tb)) continue; const head = tb.tHead && tb.tHead.rows[0]; if (!head) continue;
    const body = tb.tBodies[0]; if (!body || body.rows.length < 2) continue;
    [...head.cells].forEach((th, ci) => { if (!vis(th)) return; const tds = [...body.rows].slice(0, 12).map(r => r.cells[ci]).filter(Boolean).filter(vis); if (!tds.length) return;
      const al = e => { const a = cs(e).textAlign; return a === 'end' || a === 'right' ? 'right' : a === 'center' ? 'center' : 'left'; };
      const counts = {}; tds.forEach(td => counts[al(td)] = (counts[al(td)] || 0) + 1);
      const major = Object.entries(counts).sort((a,b) => b[1]-a[1])[0][0];
      const numeric = tds.filter(td => /^[\s\(\-−+]*[£$€]?\s?[\d.,\s]+%?\)?\s*[A-Za-z€%]{0,4}$/.test(txt(td))).length >= tds.length * 0.6;
      if (al(th) !== major) out.table_align.push({table: sel(tb), column: txt(th), header: al(th), cells: major, numeric});
      else if (numeric && major !== 'right') out.table_align.push({table: sel(tb), column: txt(th), header: al(th), cells: major, numeric, issue: 'numeric column not right-aligned'}); }); }

  // ---- long tables without a sticky header
  out.table_sticky = [];
  for (const tb of document.querySelectorAll('table')) { if (!vis(tb)) continue; const rows = tb.tBodies[0] ? tb.tBodies[0].rows.length : 0;
    if (rows <= 15) continue; const head = tb.tHead || tb.querySelector('tr');
    const sticky = head && ([head, ...head.querySelectorAll('th, td, tr')].some(e => cs(e).position === 'sticky'));
    if (!sticky) out.table_sticky.push({table: sel(tb), body_rows: rows}); }

  // ---- census
  const radii = {}, shadows = {}, sizes = {}, fams = {}, pads = [];
  for (const el of document.querySelectorAll('body *')) { if (!vis(el)) continue; const s = cs(el);
    if (hasBox(el)) { const r = s.borderTopLeftRadius; if (r !== '0px') radii[r] = (radii[r] || 0) + 1; if (s.boxShadow !== 'none') shadows[s.boxShadow] = (shadows[s.boxShadow] || 0) + 1; }
    if (el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { sizes[s.fontSize] = (sizes[s.fontSize] || 0) + 1; fams[s.fontFamily.split(',')[0]] = (fams[s.fontFamily.split(',')[0]] || 0) + 1; } }
  for (const sec of document.querySelectorAll('body > section, main > section, body > header, body > footer, main > div, body > main > *')) { if (!vis(sec)) continue; const s = cs(sec);
    pads.push({sel: sel(sec), top: s.paddingTop, bottom: s.paddingBottom}); }
  out.census = {radii, shadows: Object.keys(shadows).length, shadow_values: shadows, font_sizes: sizes, font_families: fams, section_padding: pads};
  return out;
}
"""

FOCUS_PREP = r"""
() => [...document.querySelectorAll('a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])')]
  .filter(e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.disabled; })
  .slice(0, 40).map((e, i) => { e.setAttribute('data-uichk', i); return i; })
"""


def focus_check(pg):
    idx = pg.evaluate(FOCUS_PREP)
    invisible = []
    for i in idx:
        loc = pg.locator(f'[data-uichk="{i}"]')
        try:
            loc.scroll_into_view_if_needed(timeout=2000)
            pg.mouse.move(0, 0)
            pg.wait_for_timeout(30)
            # visually hidden inputs (custom radios, toggles) show focus on their label: measure that
            pg.evaluate(f'''(() => {{ const e = document.querySelector('[data-uichk="{i}"]'); const r = e.getBoundingClientRect();
                const s = getComputedStyle(e); const hidden = r.width * r.height < 16 || parseFloat(s.opacity) < 0.05 || s.clip !== 'auto' && s.clip !== '';
                let t = null; if (hidden) {{ t = e.closest('label') || (e.id && document.querySelector('label[for="' + e.id + '"]')) || e.parentElement; }}
                document.querySelectorAll('[data-uichk-box]').forEach(x => x.removeAttribute('data-uichk-box'));
                (t || e).setAttribute('data-uichk-box', '1'); }})()''')
            box = pg.locator('[data-uichk-box="1"]').bounding_box()
            if not box:
                continue
            vw = pg.viewport_size
            clip = {'x': max(0, box['x'] - 8), 'y': max(0, box['y'] - 8)}
            clip['width'] = min(vw['width'] - clip['x'], box['width'] + 16)
            clip['height'] = min(vw['height'] - clip['y'], box['height'] + 16)
            if clip['width'] <= 0 or clip['height'] <= 0:
                continue
            a = pg.screenshot(clip=clip)
            pg.evaluate(f'document.querySelector(\'[data-uichk="{i}"]\').focus({{focusVisible: true}})')
            pg.wait_for_timeout(120)
            box2 = pg.locator('[data-uichk-box="1"]').bounding_box()
            if box2 and abs(box2['y'] - box['y']) > 1:
                clip['y'] = max(0, box2['y'] - 8)
                pg.evaluate(f'document.activeElement.blur()')
                pg.wait_for_timeout(60)
                a = pg.screenshot(clip=clip)
                pg.evaluate(f'document.querySelector(\'[data-uichk="{i}"]\').focus({{focusVisible: true}})')
                pg.wait_for_timeout(120)
            b = pg.screenshot(clip=clip)
            if a == b:
                invisible.append(pg.evaluate(f'''(() => {{ const e = document.querySelector('[data-uichk="{i}"]');
                    return (e.id ? '#' + e.id : e.tagName.toLowerCase() + (e.classList.length ? '.' + [...e.classList].slice(0,2).join('.') : '')) + ' "' + (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0,30) + '"'; }})()'''))
            pg.evaluate('document.activeElement && document.activeElement.blur()')
        except Exception:
            pass
    return invisible


def run(page, shots=None, widths=(360, 768, 1280), dark=False, height=900):
    url = page if page.startswith('http') else 'file://' + os.path.abspath(page)
    res = {'page': page, 'scheme': 'dark' if dark else 'light', 'viewports': {}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in widths:
            ctx = b.new_context(viewport={'width': w, 'height': height}, color_scheme='dark' if dark else 'light', reduced_motion='reduce')
            pg = ctx.new_page()
            pg.goto(url)
            pg.wait_for_timeout(500)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            r = pg.evaluate(JS)
            r['overflow'] = {'scrollWidth': sw, 'viewport': w, 'overflow_px': max(0, sw - w)}
            if shots:
                os.makedirs(shots, exist_ok=True)
                name = os.path.basename(page.rstrip('/')) or 'page'
                pg.screenshot(path=f"{shots}/{name}_{w}{'_dark' if dark else ''}.png", full_page=True)
            if w == max(widths):
                r['focus_invisible'] = focus_check(pg)
            res['viewports'][w] = r
            ctx.close()
        b.close()
    return res


KEYS = ['contrast', 'targets', 'names', 'media', 'headings', 'small_text', 'widows', 'grid_orphans', 'card_rows', 'baselines',
        'control_heights', 'nested_radius', 'near_miss_edges', 'pad_asymmetry', 'ratios', 'icon_sizes', 'heading_prox',
        'gutters', 'chip_heights', 'table_align', 'table_sticky']


def details(res, limit=6):
    """Candidate items per check, merged across widths (same item at several widths listed once)."""
    out, seen = [], {}
    for w, r in res['viewports'].items():
        for k in KEYS + ['focus_invisible']:
            for item in (r.get(k) or [])[:40]:
                sig = k + json.dumps(item, sort_keys=True, ensure_ascii=False)
                seen.setdefault(sig, {})
                seen[sig][w] = seen[sig].get(w, 0) + 1
    by_key = {}
    for sig, ws in seen.items():
        for k in KEYS + ['focus_invisible']:
            if sig.startswith(k + '{') or sig.startswith(k + '"') or sig.startswith(k + '['):
                by_key.setdefault(k, []).append((sig[len(k):], ws)); break
    for k, items in by_key.items():
        if k == 'targets':
            items = [i for i in items if '"hard": true' in i[0]] + [i for i in items if '"hard": true' not in i[0]]
        out.append(f"### {k} ({len(items)})")
        for sig, ws in items[:limit]:
            n = max(ws.values())
            out.append(f"- {sig}  @{','.join(str(x) for x in ws)}" + (f"  (x{n})" if n > 1 else ''))
        if len(items) > limit:
            out.append(f"- ... {len(items) - limit} more in the JSON")
    return '\n'.join(out)


def summary(res):
    lines = [f"# {res['page']} ({res['scheme']})"]
    for w, r in res['viewports'].items():
        o = r['overflow']
        parts = [f"overflow {o['overflow_px']}px"]
        for k in KEYS:
            n = len(r[k])
            if k == 'targets':
                parts.append(f"targets<44 {n} (<24: {sum(t['hard'] for t in r[k])})")
            elif n:
                parts.append(f"{k} {n}")
        if r.get('contrast_unknown'):
            parts.append(f"text over gradient/image {r['contrast_unknown']} (check by eye)")
        if 'focus_invisible' in r:
            parts.append(f"focus_invisible {len(r['focus_invisible'])}")
        c = r['census']
        pads = sorted({x['top'] for x in c['section_padding']} | {x['bottom'] for x in c['section_padding']}, key=lambda v: float(v[:-2]) if v.endswith('px') else 0)
        parts.append(f"census: {len(c['radii'])} radii {sorted(c['radii'])}, {c['shadows']} shadows, {len(c['font_sizes'])} font sizes, {len(c['font_families'])} families, section paddings {pads}")
        lines.append(f"## {w}px: " + ' | '.join(parts))
    return '\n'.join(lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('page'); ap.add_argument('--json'); ap.add_argument('--shots')
    ap.add_argument('--widths', default='360,768,1280'); ap.add_argument('--dark', action='store_true'); ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--quiet', action='store_true', help='counts only, no item details')
    a = ap.parse_args()
    res = run(a.page, a.shots, tuple(int(x) for x in a.widths.split(',')), a.dark, a.height)
    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, ensure_ascii=False)
    print(summary(res))
    if not a.quiet:
        print('\n' + details(res))
