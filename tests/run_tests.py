#!/usr/bin/env python3
"""Acceptance tests for the fit and scrolling checks of ui-ux-audit/scripts/uicheck.py. For maintaining the script:
the folder is not part of the installed skill.    python3 tests/run_tests.py

1  fixture-a          the switch outgrows its padded box once the missing house font is replaced by a wider one
2  fixture-b          a fixed panel scrolls by accident; the hidden texts are named as the cause; the nested scroller is listed
3  fixture-b-fixed    the repaired panel: no unexpected scroll, no nested scroll
4  --baseline         the switch is reported as having left its box since the run before the padded box was added
5  fixture-b-clipped  overflow: hidden alone still leaves a stretched panel, and it is reported
"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); UIC = os.path.join(HERE, '..', 'ui-ux-audit', 'scripts', 'uicheck.py'); TMP = tempfile.mkdtemp(prefix='uicheck-tests-')


def run(page, name, *extra):
    js = os.path.join(TMP, name + '.json')
    p = subprocess.run([sys.executable, UIC, os.path.join(HERE, page), '--widths', '1280', '--height', '917', '--no-walk', '--quiet', '--json', js, *extra], capture_output=True, text=True)
    if not os.path.exists(js):
        sys.exit('uicheck did not run: ' + (p.stderr or p.stdout)[-300:])
    return json.load(open(js, encoding='utf-8'))


def items(res, check):
    return [(name, i) for rec in res['pages'].values() for name, r in rec['passes'].items() for i in r.get(check, [])]


results = []
def test(n, title, ok, detail):
    results.append(ok); print(f"{'PASS' if ok else 'FAIL' if ok is False else 'SKIP'}  {n}  {title}: {detail}")


a = run('fixture-a.html', 'a'); fit = next(iter(a['pages'].values()))['fit']; hits = [(n, i) for n, i in items(a, 'control-overflow') + items(a, 'content-cut-off') if 'seg' in i.get('sel', '')]
if 'Arial Nova' not in fit['fonts_not_available']:
    test(1, 'switch outgrows its box with the real font', None, 'Arial Nova is installed on this machine, so the main pass already measures the real font')
elif not any(fit['font_pass'].values()) and not hits:
    test(1, 'switch outgrows its box with the real font', None, 'no wide font (DejaVu Sans, Verdana) is installed here to stand in for Arial Nova')
else:
    test(1, 'switch outgrows its box with the real font', bool(hits), '; '.join(f"{n}: {i['over_px'] if 'over_px' in i else i['cut_px']}px past {i.get('box') or i.get('cut_by')}" for n, i in hits) or 'not reported')

b = run('fixture-b.html', 'b'); su = [i for _, i in items(b, 'scroll-unexpected') if 'side' in i['sel']]; sn = [i for _, i in items(b, 'scroll-nested')]
test(2, 'accidental scroll of the fixed panel', bool(su) and any('sr-only' in c for i in su for c in i.get('stretched_by_unseen_elements', [])) and bool(sn),
     (f"{su[0]['sel']} scrolls {su[0]['scroll_height']}px in {su[0]['client_height']}px, stretched by {su[0]['stretched_by_unseen_elements']}; nested: {[(i['inner'], i['outer']) for i in sn]}" if su else 'not reported'))

f = run('fixture-b-fixed.html', 'b-fixed'); left = items(f, 'scroll-unexpected') + items(f, 'scroll-nested')
test(3, 'repaired panel is clean', not left, 'no unexpected scroll, no nested scroll' if not left else str(left)[:200])

run('fixture-a-before.html', 'a-before'); r = run('fixture-a.html', 'a-after', '--baseline', os.path.join(TMP, 'a-before.json')); g = next(iter(r['regression'].values()))
moved = [c for c in g.get('control_left_its_box', []) if 'Gautoms' in c['control']]
test(4, 'regression pass sees the switch leave its box', (bool(moved) if any(fit['font_pass'].values()) or hits else None),
     (f"{moved[0]['now']} (before: {moved[0]['before']}) in {moved[0]['passes']}" if moved else 'not reported' if any(fit['font_pass'].values()) else 'needs the wide-font pass, which could not run here'))

c = run('fixture-b-clipped.html', 'b-clipped'); st = [i for _, i in items(c, 'scroll-unexpected') if 'side' in i['sel']]
test(5, 'clipped panel that is still stretched', bool(st), (f"{st[0]['sel']}: {st[0].get('stray_px')}px stretched by {st[0]['stretched_by_unseen_elements']}" if st else 'not reported'))

bad = [r for r in results if r is False]
print(f"{len([r for r in results if r])} passed, {len(bad)} failed, {len([r for r in results if r is None])} skipped"); sys.exit(1 if bad else 0)
