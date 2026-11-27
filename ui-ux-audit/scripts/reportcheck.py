#!/usr/bin/env python3
"""Check a full-audit report before it is sent (ui-ux-audit skill): format, codes, severities and arithmetic.

  python3 reportcheck.py - [--checks out/checks.json] [--score-only] < draft     (the draft on standard input)
  python3 reportcheck.py draft-file [--checks out/checks.json] [--score-only]

It reads references/severity-registry.md beside this script, so the codes and the severities each code may take are
never out of step with the skill. Fix every line it prints, run it again, and send the report only when it prints OK.
--score-only prints the score line and verdict computed from the findings in the report (use it instead of mental arithmetic).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = ['Blockers', 'Critical', 'Warnings', 'Polish', 'Task walk', 'Visual quality', 'Verify', 'Wiring to confirm', 'Clean', 'Durable fixes', 'Questions']
LEVEL = {'B': 'Blocker', 'C': 'Critical', 'W': 'Warning', 'P': 'Polish'}
HEADER = ['**Score:**', '**Verdict:**', '**Profile:**', '**Style:**', '**Checked:**', '**Visual quality:**', '**Top 3:**']
RATINGS = ['Exceptional', 'Distinctive with slips', 'Competent but forgettable', 'Generic template', 'Inconsistent']
WORD_LIMIT, WORD_LIMIT_FLOW = 1200, 1500


def registry():
    codes = {}
    path = os.path.join(HERE, '..', 'references', 'severity-registry.md')
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\|\s*`([a-z-]+)`\s*\|(.*?)\|(.*?)\|(.*?)\|\s*$', line)
        if m:
            allowed = {lv for lv in LEVEL.values() if re.search(r'\b' + lv + r'\b', m.group(3) + ' ' + m.group(4))}
            codes[m.group(1)] = allowed
    codes['other'] = {'Blocker', 'Critical', 'Warning', 'Polish'}
    return codes


def verdict(score, blockers):
    if blockers:
        return 'Do not ship'
    return 'Ready to ship' if score >= 90 else 'Ship after fixing the top findings' if score >= 70 else 'Significant rework' if score >= 40 else 'Do not ship'


def parse(text):
    finds = [{'id': a + b, 'level': LEVEL[a], 'code': c, 'title': t.strip()} for a, b, c, t in re.findall(r'^\s*(?:[-*]\s+)?\*\*([BCWP])(\d+)\s*\[([a-z-]+)\]\s*(.*?)\*\*', text, re.M)]
    loose = re.findall(r'^\s*(?:[-*]\s+)?\*\*([BCWP]\d+)[.:]?\s+(?!\[)', text, re.M)
    return finds, loose


def score_line(finds):
    n = {k: sum(1 for f in finds if f['id'][0] == k) for k in 'BCWP'}
    s = max(0, 100 - 12 * n['B'] - 8 * n['C'] - 4 * n['W'] - min(5, n['P']))
    return n, s, f"100 − ({n['B']}×12) − ({n['C']}×8) − ({n['W']}×4) − min(5, {n['P']}) = {s}/100"


def check(text, checks_path=None):
    issues = []; codes = registry(); finds, loose = parse(text)
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines or not lines[0].startswith('# UI audit:'):
        issues.append('The report must start with the line "# UI audit: <page>" (no text before it).')
    head = '\n'.join(lines[:12]); pos = -1
    for h in HEADER:
        p = head.find(h)
        if p < 0: issues.append(f'Header field {h} is missing (fields, in order: {" ".join(HEADER)}).')
        elif p < pos: issues.append(f'Header field {h} is out of order.')
        pos = max(pos, p)
    for fid in loose:
        issues.append(f'{fid}: write the registry code in square brackets after the ID, for example "**{fid} [contrast-text] Title**".')
    seen = {}
    for f in finds:
        if f['code'] not in codes:
            issues.append(f"{f['id']}: [{f['code']}] is not a code in severity-registry.md (use the exact code, or [other]).")
        elif f['level'] not in codes[f['code']]:
            issues.append(f"{f['id']}: [{f['code']}] cannot be {f['level']}; the registry allows {', '.join(sorted(codes[f['code']]))}.")
        if f['code'] != 'other' and f['code'] in seen:
            issues.append(f"{f['id']} and {seen[f['code']]} both use [{f['code']}]: one finding per code; merge them and list every place.")
        seen.setdefault(f['code'], f['id'])
    for k in 'BCWP':
        nums = [int(f['id'][1:]) for f in finds if f['id'][0] == k]
        if nums != list(range(1, len(nums) + 1)):
            issues.append(f'{LEVEL[k]} IDs must run {k}1, {k}2, ... in order with no gaps (found {nums}).')
    n, s, line = score_line(finds)
    m = re.search(r'\*\*Score:\*\*\s*(.*)', text)
    if m:
        got = re.sub(r'\s+', '', m.group(1)).replace('-', '−').replace('x', '×').replace('*', '×').rstrip('.')
        if not got.startswith(re.sub(r'\s+', '', line)):
            issues.append(f'Score line must read exactly: **Score:** {line}   (computed from the findings listed in the report).')
    v = re.search(r'\*\*Verdict:\*\*\s*([^\n*]+)', text)
    if v and not v.group(1).strip().lower().startswith(verdict(s, n['B']).lower()[:12]):
        issues.append(f'Verdict must be "{verdict(s, n["B"])}" for this score' + (' (any Blocker means Do not ship).' if n['B'] else '.'))
    r = re.search(r'\*\*Visual quality:\*\*\s*([^\n]+)', text)
    if r and not any(r.group(1).strip().lower().startswith(x.lower()) for x in RATINGS):
        issues.append('Visual quality must start with one of: ' + '; '.join(RATINGS) + '.')
    ck = re.search(r'\*\*Checked:\*\*\s*([^\n]+)', text); run = re.search(r'uicheck run ([0-9a-f]{8})', ck.group(1)) if ck else None; shot = re.search(r'shotcheck run ([0-9a-f]{8})', ck.group(1)) if ck else None
    if ck and not run and not shot and 'no browser' not in ck.group(1).lower():
        issues.append('Checked must quote the run id the script printed ("uicheck run 1a2b3c4d" or "shotcheck run ..."), or say "no browser: estimates only".')
    if checks_path and run:
        try:
            if json.load(open(checks_path, encoding='utf-8')).get('run_id') != run.group(1):
                issues.append(f'The run id in the header ({run.group(1)}) is not the run id inside {checks_path}. Quote the id of the run you actually used.')
        except Exception as e:
            issues.append(f'Could not read {checks_path}: {e}')
    heads = [h.strip() for h in re.findall(r'^##\s+(.+)$', text, re.M)]; order = []
    for h in heads:
        name = next((x for x in SECTIONS if h.lower().startswith(x.lower())), None)
        if not name:
            issues.append(f'Section "## {h[:40]}" is not in the template. Allowed, in this order: {", ".join(SECTIONS)}.'); continue
        order.append(SECTIONS.index(name))
        if name in ('Blockers', 'Critical', 'Warnings', 'Polish'):
            k = name[0]; c = re.search(r'\((\d+)\)', h)
            if not c or int(c.group(1)) != n[k]:
                issues.append(f'Heading must read "## {name} ({n[k]})": it has to match the number of {k} findings.')
    if order != sorted(order):
        issues.append('Sections are out of order. Order: ' + ', '.join(SECTIONS) + '.')
    for k, name in (('B', 'Blockers'), ('C', 'Critical'), ('W', 'Warnings'), ('P', 'Polish')):
        if n[k] and name not in [SECTIONS[i] for i in order]:
            issues.append(f'There are {k} findings but no "## {name} ({n[k]})" section.')
    if 'Task walk' not in [SECTIONS[i] for i in order]:
        issues.append('The "## Task walk" section is missing (task, completed or not, steps, hesitations).')
    blocks = re.split(r'^\s*(?:[-*]\s+)?\*\*(?=[BCW]\d+\s*\[)', text, flags=re.M)[1:]
    for b in blocks:
        fid = re.match(r'([BCW]\d+)', b).group(1); body = re.split(r'\n\s*(?:[-*]\s+)?\*\*[BCWP]\d+|\n## ', b)[0]
        miss = [x for x in ('**Found:**', '**Why:**', '**Fix:**') if x not in body]
        if miss:
            issues.append(f'{fid} needs {", ".join(miss)} (each on its own line, one or two lines long).')
    t3 = re.search(r'\*\*Top 3:\*\*([^\n]*)', text)
    if t3:
        ids = {f['id'] for f in finds}
        for t in re.findall(r'\b([BCWP]\d+)\b', t3.group(1)):
            if t not in ids: issues.append(f'Top 3 names {t}, which is not a finding in the report.')
    words = len(re.findall(r'\S+', text)); flow = bool(re.search(r'\*\*Profile:\*\*[^\n]*\b(flow|screens)\b', text, re.I)); lim = (WORD_LIMIT_FLOW if flow else WORD_LIMIT) + 40 * max(0, len(finds) - 10)   # room grows with the findings, so none is dropped to save words
    if words > lim * 1.1:
        issues.append(f'{words} words; the limit is about {lim}. Shorten Why and Fix to one line each; never drop a finding to save words.')
    return issues, {'counts': n, 'score': s, 'score_line': line, 'verdict': verdict(s, n['B']), 'words': words, 'findings': finds}


if __name__ == '__main__':
    if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
        print(__doc__.strip()); sys.exit(0)
    src = next((a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and sys.argv[i - 1] != '--checks'), '-')
    if src == '-' and sys.stdin.isatty():
        sys.exit(__doc__)
    if src != '-' and not os.path.isfile(src):
        sys.exit(f'reportcheck: no such file: {src}. Pass the draft on standard input with "-" instead.')
    text = sys.stdin.read() if src == '-' else open(src, encoding='utf-8').read()
    checks = sys.argv[sys.argv.index('--checks') + 1] if '--checks' in sys.argv else None
    issues, info = check(text, checks)
    if '--score-only' in sys.argv:
        print(f"**Score:** {info['score_line']}\n**Verdict:** {info['verdict']}"); sys.exit(0)
    if '--json' in sys.argv:
        print(json.dumps({'ok': not issues, 'issues': issues, **info}, ensure_ascii=False)); sys.exit(0 if not issues else 1)
    if issues:
        print(f'{len(issues)} thing(s) to fix before sending:'); [print(' - ' + i) for i in issues]
        print(f"\nComputed from the findings in the report:\n**Score:** {info['score_line']}\n**Verdict:** {info['verdict']}"); sys.exit(1)
    print(f"OK. {info['score_line']}. Verdict: {info['verdict']}. {info['words']} words.")
