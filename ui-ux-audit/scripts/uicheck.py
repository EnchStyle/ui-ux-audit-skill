#!/usr/bin/env python3
"""Measure a rendered page (ui-ux-audit skill). Every check is named after its row in references/severity-registry.md.

  python3 uicheck.py PAGE [PAGE ...] --out out/            web page: 360, 768 and 1280 px, first-screen and full shots
  python3 uicheck.py s1.html s2.html --device iphone --out out/   phone screens (iphone 390x844, android 412x915)

PAGE is a local .html file or an http(s) address. Needs Python Playwright with Chromium; Pillow is optional (pixel
sampling of text over images and gradients, and the strength of focus indicators).

Options
  --out DIR          write checks.json and screenshots there (or use --json FILE and --shots DIR separately)
  --widths 320,360,768,1280,1440   widths to render (build mode uses all five)
  --device iphone|android          phone emulation: touch, device pixel ratio, safe-area insets, platform target size
  --insets T,R,B,L   safe-area insets to inject with --device (default iphone 59,0,34,0; android 24,0,24,0).
                     These are test values, not platform constants: the check is whether the layout honours them.
  --dark             also measure with the dark colour scheme (done automatically when the page has dark styles)
  --attr NAME=VALUE  also measure with this attribute set on <html> (themes switched by attribute, e.g. data-theme=dark)
  --states a,b       also measure PAGE?state=a ... (the build-mode convention for loading, empty and error states)
  --print            also render with print styles
  --no-walk          skip the keyboard walk and the click census
  --fail-on a,b      exit with status 1 when any of these checks has items (for automated runs); "all" = every check
  --baseline FILE    checks.json of an earlier run of the same page: lists every control that has left its box since,
                     every scroll area that grew by more than a fifth, and every control whose type or padding changed

Besides the widths asked for, the script draws the page again with stand-ins for fonts that are not installed (a font of
the same widths where one exists, a wide font as an upper bound otherwise: what the real font may push out of its box) and with real scrollbars (Playwright hides them; desktop browsers on Windows
and Linux take their width from the layout). What only those passes list is marked _font-check and _scrollbars.
  --quiet            counts only

Candidates are not findings: confirm each one on the screenshots or in the code, then report it under its registry code.
"""
import argparse, hashlib, io, json, os, pathlib, re, sys, time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit('uicheck: Python Playwright is not installed (pip install playwright; playwright install chromium). '
             'Without it nothing can be measured: follow the "no browser" path in SKILL.md.')
try:
    from PIL import Image
except ImportError:
    Image = None

JS = r"""
(opts) => {
  const VW = document.documentElement.clientWidth || innerWidth, VH = opts.vh || innerHeight, out = {};   // layout viewport: phones zoom out on pages that overflow
  const cs = el => getComputedStyle(el), rc = el => el.getBoundingClientRect();
  const SVGNS = 'http://www.w3.org/2000/svg';
  const hidCache = new WeakMap();
  const selfHidden = el => { const s = cs(el), r = rc(el);
    if (s.visibility === 'hidden' || s.visibility === 'collapse' || s.display === 'none' || parseFloat(s.opacity) <= 0.05) return true;
    if (el.namespaceURI !== SVGNS && s.position === 'absolute' && (r.width <= 2 || r.height <= 2) && s.overflow !== 'visible') return true;   // visually hidden helper
    if (/inset\((50|100)%\)/.test(s.clipPath) || (s.clip && /rect\(0(px)?[, ]+0(px)?[, ]+0(px)?[, ]+0(px)?\)/.test(s.clip))) return true;
    return false; };
  const hidden = el => { if (!el || el.nodeType !== 1) return false; if (hidCache.has(el)) return hidCache.get(el);
    const h = selfHidden(el) || hidden(el.parentElement); hidCache.set(el, h); return h; };
  const vis = el => { if (!el || !el.getBoundingClientRect) return false; if (el.checkVisibility && !el.checkVisibility()) return false; const r = rc(el); return r.width > 0 && r.height > 0 && !hidden(el); };   // checkVisibility: closed <details>, content-visibility
  const deco = el => !!el.closest('[aria-hidden="true"], [role="presentation"], [role="none"]');
  const sel = el => { if (el.id) return '#' + el.id; let s = el.tagName.toLowerCase();
    if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.');
    let p = el.parentElement, hops = 0; while (p && !p.id && hops < 3) { p = p.parentElement; hops++; }
    if (p && p.id) s = '#' + p.id + ' ' + s; return s; };
  const txt = el => (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', {willReadFrequently: true});
  const colCache = new Map();
  const parse = c => { if (!c || c === 'none') return null; if (colCache.has(c)) return colCache.get(c); let r = null;
    const m = c.match(/^rgba?\(([^)]+)\)$/);
    if (m) { const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); r = {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; }
    else if (!/^url\(/.test(c)) { try { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; r = {r: d[0], g: d[1], b: d[2], a: d[3] / 255}; } catch (e) { r = null; } }
    colCache.set(c, r); return r; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const blend = (fg, bg) => ({r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1});
  const ratio = (a, b) => { const L1 = lum(a), L2 = lum(b); return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05); };
  const bgOf = el => { const layers = []; let e = el;
    while (e && e.nodeType === 1) { const s = cs(e);
      if (s.backgroundImage && s.backgroundImage !== 'none') return {unknown: true};
      const c = parse(s.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= 0.99) break; }
      e = e.parentElement; }
    let base = {r: 255, g: 255, b: 255, a: 1};
    for (let i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return base; };
  const hasBox = el => { const s = cs(el), bg = parse(s.backgroundColor);
    return (bg && bg.a > 0.05) || s.backgroundImage !== 'none' || parseFloat(s.borderTopWidth) > 0 || s.boxShadow !== 'none'; };
  const FOCUSABLE = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [tabindex]:not([tabindex="-1"])';
  const INTER = FOCUSABLE + ', [role=button], [role=link], [role=tab], [role=checkbox], [role=switch], [role=menuitem], [onclick]';
  const isInter = el => el.matches(INTER);
  const push = (k, v) => (out[k] = out[k] || []).push(v);
  ['contrast-text', 'small-text', 'target-small', 'target-touch', 'name-missing', 'label-placeholder', 'alt-missing', 'media-unsized', 'heading-order',
   'widow', 'label-wrap', 'grid-lone-item', 'card-rows', 'tile-baseline', 'control-heights', 'segment-widths', 'radius-nested', 'edge-near-miss', 'pad-asymmetry',
   'media-ratios', 'icon-sizes', 'heading-proximity', 'gutter-drift', 'chip-heights', 'table-align', 'table-sticky', 'table-total', 'text-clipped',
   'text-spill', 'text-overlap', 'content-cut-off', 'line-length', 'placeholder-content', 'motion-reduce', 'hover-only', 'control-obscured',
   'safe-area', 'input-zoom', 'zoom-blocked', 'false-feedback', 'lang-missing', 'type-scale-drift', 'page-overflow', 'section-rhythm', 'radius-drift', 'shadow-drift', 'nav-hidden'].forEach(k => out[k] = []);
  out._sample = []; out._pointer = [];

  // ---- document basics
  const mv = document.querySelector('meta[name=viewport]'); const mvc = mv ? (mv.getAttribute('content') || '').toLowerCase() : null;
  out._doc = {lang: document.documentElement.getAttribute('lang'), title: document.title, viewport_meta: mvc, h1: document.querySelectorAll('h1').length,
    main: !!document.querySelector('main, [role=main]'), viewport_fit_cover: !!(mvc && /viewport-fit\s*=\s*cover/.test(mvc)), canvases: document.querySelectorAll('canvas').length};
  if (!out._doc.lang) out['lang-missing'].push({issue: 'html element has no lang attribute'});
  if (mvc === null) out['zoom-blocked'].push({issue: 'no viewport meta tag: phones lay the page out about 980px wide and shrink it'});
  else { const ms = mvc.match(/maximum-scale\s*=\s*([\d.]+)/);
    if (/user-scalable\s*=\s*(no|0)/.test(mvc) || (ms && parseFloat(ms[1]) < 2)) out['zoom-blocked'].push({issue: 'viewport meta stops pinch zoom', content: mvc}); }
  const sw = document.documentElement.scrollWidth;
  if (sw > VW + 1) { const off = []; for (const e of document.querySelectorAll('body *')) { if (!vis(e)) continue; const r = rc(e);
      if (r.right > VW + 1 && r.width <= sw && ![...e.children].some(c => vis(c) && rc(c).right > VW + 1)) { off.push({sel: sel(e), right: Math.round(r.right), width: Math.round(r.width)}); if (off.length >= 5) break; } }
    out['page-overflow'].push({overflow_px: sw - VW, scroll_width: sw, viewport: VW, widest_elements: off}); }
  else { const cut = []; for (const e of document.querySelectorAll('body *')) { if (!vis(e) || deco(e)) continue; const r = rc(e);       // cut off without scroll
      if (r.right > VW + 4 && r.left < VW && r.width > 8 && (isInter(e) || [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))) {
        // the edge that cuts is the nearest clipping ancestor, which can lie inside the screen: measure what is hidden against it
        let a = e.parentElement, scroller = false, edge = VW; while (a && a !== document.body) { const s = cs(a); if (/(auto|scroll)/.test(s.overflowX) && a.scrollWidth > a.clientWidth) { scroller = true; break; } if (/(hidden|clip)/.test(s.overflowX)) edge = Math.min(edge, rc(a).right); a = a.parentElement; }
        if (!scroller) { cut.push({sel: sel(e), text: txt(e), cut_px: Math.round(r.right - edge), hidden_pct: Math.round(100 * Math.min(1, (r.right - Math.max(edge, r.left)) / r.width)), interactive: isInter(e)}); if (cut.length >= 40) break; } } }
    cut.sort((x, y) => (y.interactive - x.interactive) || (y.hidden_pct - x.hidden_pct)); out['content-cut-off'] = cut.slice(0, 12); }

  // ---- text: contrast, size, placeholder content
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); const seen = new Set(); let sidx = 0;
  const PH = /lorem ipsum|dolor sit amet|your (headline|title|text|heading) here|placeholder text|\bjohn doe\b|\bjane doe\b|\bacme (inc|corp)|\bTODO\b|\bxxx+\b/i;
  const sizes = {}, fams = {}, weights = {}, textCols = {};
  while (walker.nextNode()) { const t = walker.currentNode; const raw = t.textContent.trim(); if (!raw) continue;
    const el = t.parentElement; if (!el || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TITLE', 'OPTION'].includes(el.tagName) || !vis(el) || deco(el)) continue;
    if (PH.test(raw)) out['placeholder-content'].push({sel: sel(el), text: raw.slice(0, 60)});
    if (seen.has(el)) continue; seen.add(el);
    const s = cs(el), svg = el.namespaceURI === SVGNS; let size = parseFloat(s.fontSize); const weight = parseInt(s.fontWeight) || 400;
    if (svg && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) size = size * Math.hypot(m.a, m.b); }
    const k = Math.round(size * 2) / 2; sizes[k] = (sizes[k] || 0) + 1; const fam = s.fontFamily.split(',')[0].trim().replace(/["']/g, ''); fams[fam] = (fams[fam] || 0) + 1; weights[weight] = (weights[weight] || 0) + 1;
    if (size < 11.9) out['small-text'].push({sel: sel(el), px: +size.toFixed(1), text: raw.slice(0, 40), svg});
    if (el.closest(':disabled, [aria-disabled="true"]')) continue;
    const fg = parse(svg ? s.fill : s.color); if (!fg || fg.a === 0) continue; textCols[[fg.r, fg.g, fg.b].join(',')] = 1;
    const large = size >= 24 || (size >= 18.66 && weight >= 700), need = large ? 3 : 4.5;
    const role = el.closest('a, button, [role=button], label, summary, select, th') ? 'control or label' : 'text';
    let op = 1, e2 = el; while (e2 && e2.nodeType === 1) { op *= parseFloat(cs(e2).opacity); e2 = e2.parentElement; }
    const bg = bgOf(svg ? (el.ownerSVGElement || el) : el);
    if (bg.unknown) { if (out._sample.length < 40) { el.setAttribute('data-uic-s', sidx); out._sample.push({i: sidx++, sel: sel(el), fg: {r: fg.r, g: fg.g, b: fg.b, a: fg.a * op}, need, px: +size.toFixed(1), role, text: raw.slice(0, 40)}); } continue; }
    const f = blend({...fg, a: fg.a * op}, bg), R = ratio(f, bg);
    if (R < need) out['contrast-text'].push({sel: sel(el), ratio: +R.toFixed(2), need, px: +size.toFixed(1), role, text: raw.slice(0, 40)}); }
  for (const el of document.querySelectorAll('input[placeholder], textarea[placeholder]')) { if (!vis(el) || el.value || el.disabled) continue;
    const fg = parse(getComputedStyle(el, '::placeholder').color), bg = bgOf(el); if (!fg || bg.unknown) continue; const R = ratio(blend(fg, bg), bg);
    if (R < 4.5) out['contrast-text'].push({sel: sel(el), ratio: +R.toFixed(2), need: 4.5, px: parseFloat(cs(el).fontSize), role: 'placeholder', text: el.getAttribute('placeholder').slice(0, 40)}); }

  // ---- interactive: names, labels, targets
  const inter = [...document.querySelectorAll(INTER)].filter(el => vis(el));
  { const seenC = new Set(); out._controls = [];
    for (const el of inter) { const nm = ((el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('title') || (el.labels && el.labels[0] && el.labels[0].innerText) || '') + '').replace(/\s+/g, ' ').trim().slice(0, 50);
      if (!nm || nm.length < 2) continue; const k = el.tagName + '|' + nm.toLowerCase(); if (seenC.has(k)) continue; seenC.add(k);
      out._controls.push({name: nm, tag: el.tagName.toLowerCase(), href: el.getAttribute('href') || null, toggle: el.hasAttribute('aria-expanded') || el.hasAttribute('aria-controls') || el.tagName === 'SUMMARY', options: el.tagName === 'SELECT' ? [...el.options].map(o => o.textContent.trim().toLowerCase()).slice(0, 30) : null}); if (out._controls.length >= 200) break; } }
  const hitRect = el => { let r = rc(el); if (el.tagName === 'INPUT' && /^(checkbox|radio)$/.test(el.type)) { const l = el.closest('label') || (el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`));
      if (l && vis(l)) { const q = rc(l); r = {left: Math.min(r.left, q.left), top: Math.min(r.top, q.top), right: Math.max(r.right, q.right), bottom: Math.max(r.bottom, q.bottom)}; r.width = r.right - r.left; r.height = r.bottom - r.top; } } return r; };
  const tg = [];
  for (const el of inter) { const r = hitRect(el);
    const inline = el.tagName === 'A' && cs(el).display.startsWith('inline') && el.closest('p, li, td, dd, figcaption, small, blockquote') && el.parentElement && [...el.parentElement.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!inline && !(el.tagName === 'LABEL')) tg.push({el, r, small: r.width < 24 || r.height < 24});
    let name = (el.getAttribute('aria-label') || '').trim();
    if (!name && el.getAttribute('aria-labelledby')) name = el.getAttribute('aria-labelledby').split(/\s+/).map(id => (document.getElementById(id) || {}).textContent || '').join(' ').trim();
    const field = ['SELECT', 'TEXTAREA'].includes(el.tagName) || (el.tagName === 'INPUT' && !/^(submit|button|reset|image)$/.test(el.type));
    if (field) { let lab = ''; if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l) lab = l.textContent.trim(); }
      if (!lab && el.closest('label')) lab = el.closest('label').textContent.trim();
      const visibleLabel = !!lab; const ph = el.getAttribute('placeholder');
      if (!lab && !name && !(el.getAttribute('title') || '').trim()) { if (ph) out['label-placeholder'].push({sel: sel(el), placeholder: ph, accessible_name: 'none'}); else out['name-missing'].push({sel: sel(el), tag: el.tagName.toLowerCase(), type: el.type || null}); }
      else if (!visibleLabel && ph && !/^(search)$/.test(el.type) && !el.closest('[role=search]')) out['label-placeholder'].push({sel: sel(el), placeholder: ph, accessible_name: 'aria-label or title only, no visible label'});
    } else { if (!name) name = (el.tagName === 'INPUT' ? (el.value || el.getAttribute('alt') || '') : (el.innerText || '')).trim();
      if (!name) name = [...el.querySelectorAll('img[alt], svg[aria-label], svg title, [aria-label]')].map(i => i.getAttribute('alt') || i.getAttribute('aria-label') || i.textContent || '').join(' ').trim();
      if (!name) name = (el.getAttribute('title') || '').trim();
      if (!name && !(el.tagName === 'A' && !el.getAttribute('href'))) out['name-missing'].push({sel: sel(el), tag: el.tagName.toLowerCase(), icon_only: !!el.querySelector('svg, img, i')}); } }
  for (const t of tg) { if (!t.small) continue; const cxp = (t.r.left + t.r.right) / 2, cyp = (t.r.top + t.r.bottom) / 2; let near = null;
    for (const o of tg) { if (o === t || o.el.contains(t.el) || t.el.contains(o.el)) continue;
      if (o.small) { const ox = (o.r.left + o.r.right) / 2, oy = (o.r.top + o.r.bottom) / 2; if (Math.hypot(ox - cxp, oy - cyp) < 24) { near = o; break; } }
      else { const dx = Math.max(o.r.left - cxp, 0, cxp - o.r.right), dy = Math.max(o.r.top - cyp, 0, cyp - o.r.bottom); if (Math.hypot(dx, dy) < 12) { near = o; break; } } }
    if (near) out['target-small'].push({sel: sel(t.el), w: Math.round(t.r.width), h: Math.round(t.r.height), too_close_to: sel(near.el), text: txt(t.el)}); }
  if (opts.touchMin) { const g = {}; for (const t of tg) { const m = Math.min(t.r.width, t.r.height); if (m >= opts.touchMin - 0.5) continue;
      const k = t.el.tagName + '.' + [...t.el.classList].sort().join('.'); (g[k] = g[k] || {sel: sel(t.el), count: 0, w: Math.round(t.r.width), h: Math.round(t.r.height), min_required: opts.touchMin, examples: []}).count++; if (g[k].examples.length < 3) g[k].examples.push(txt(t.el) || t.el.getAttribute('aria-label') || ''); }
    out['target-touch'] = Object.values(g); }
  // pointer cursor on elements the keyboard cannot reach (listeners are confirmed from Python)
  let pidx = 0;
  for (const el of document.querySelectorAll('body *')) { if (!vis(el) || el.matches(FOCUSABLE) || el.closest(FOCUSABLE) || el.querySelector(FOCUSABLE) || /^(LABEL|OPTION|HTML|BODY)$/.test(el.tagName)) continue;
    const ptr = cs(el).cursor === 'pointer', attr = el.hasAttribute('onclick'); if (!ptr && !attr) continue;
    if (el.parentElement && cs(el.parentElement).cursor === 'pointer' && !attr) continue;
    if (pidx < 40) { el.setAttribute('data-uic-k', pidx); out._pointer.push({i: pidx++, sel: sel(el), text: txt(el), onclick_attribute: attr, role: el.getAttribute('role')}); } }
  if (opts.device === 'iphone') for (const el of document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=hidden]):not([type=submit]):not([type=button]), select, textarea')) { if (!vis(el)) continue; const f = parseFloat(cs(el).fontSize);
      if (f < 16) out['input-zoom'].push({sel: sel(el), font_px: f}); }

  // ---- media, alt, headings
  for (const m of document.querySelectorAll('img, video')) { if (!vis(m)) continue; const r = rc(m); if (r.width < 2 || r.height < 2) continue;
    if (m.tagName === 'IMG' && !m.hasAttribute('alt') && !deco(m)) out['alt-missing'].push({sel: sel(m), src: (m.getAttribute('src') || '').slice(-40)});
    const c = m.cloneNode(false); c.removeAttribute('src'); c.removeAttribute('srcset'); c.removeAttribute('poster'); c.removeAttribute('alt'); c.removeAttribute('id'); m.after(c); const q = rc(c); c.remove();
    if (q.height < r.height * 0.8 || q.width < r.width * 0.8) out['media-unsized'].push({sel: sel(m), rendered: Math.round(r.width) + 'x' + Math.round(r.height), first_screen: r.top < VH, src: (m.getAttribute('src') || '').slice(-40)}); }
  { let prev = 0; const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis);
    for (const h of hs) { const l = +h.tagName[1]; if (prev && l > prev + 1) out['heading-order'].push({sel: sel(h), from: prev, to: l, text: txt(h)}); prev = l; }
    const h1s = hs.filter(h => h.tagName === 'H1').length; if (hs.length && h1s !== 1) out['heading-order'].push({issue: h1s ? h1s + ' h1 elements' : 'no h1', first_heading: hs[0].tagName.toLowerCase()}); }

  // ---- widows, wrapping labels, line length
  const lineTops = el => { const tops = []; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) { const n = w.currentNode; const re = /\S+/g; let m;
      while ((m = re.exec(n.textContent))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const rects = rg.getClientRects(); if (!rects.length) continue; tops.push({t: Math.round(rects[0].top), w: m[0]}); } }
    const lines = []; for (const x of tops) { const L = lines.find(l => Math.abs(l.t - x.t) <= 4); if (L) L.words.push(x.w); else lines.push({t: x.t, words: [x.w]}); }
    lines.sort((a, b) => a.t - b.t); return lines; };
  const widowC = new Set([...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[class*=title],[class*=headline],[class*=lede],figcaption,blockquote,dt,legend')]);
  for (const el of document.querySelectorAll('p, li, span, div')) { if (el.children.length === 0 && vis(el)) { const s = cs(el), t = txt(el); if (t.length > 0 && t.length < 160 && parseFloat(s.fontSize) >= 17) widowC.add(el); } }
  for (const el of widowC) { if (!vis(el) || deco(el) || el.closest('th, td, nav, svg')) continue; const lines = lineTops(el);
    if (lines.length >= 2 && lines.length <= 4) { const last = lines[lines.length - 1], before = lines[lines.length - 2];
      if (last.words.length === 1 && before.words.length >= 2 && !/^\(.*\)$/.test(last.words[0])) out['widow'].push({sel: sel(el), lines: lines.length, last_line: last.words[0], text: txt(el)}); } }
  for (const el of document.querySelectorAll('button, a[class*=btn], a[class*=button], a[class*=cta], [role=button]')) { if (!vis(el)) continue;
    if (cs(el).flexDirection.startsWith('column') || [...el.children].some(c => cs(c).display === 'block' || c.tagName === 'BR' || c.tagName === 'SMALL')) continue;   // a deliberate second line
    const lines = lineTops(el); if (lines.length >= 2) out['label-wrap'].push({sel: sel(el), lines: lines.length, text: txt(el)}); }
  for (const p of document.querySelectorAll('p')) { if (!vis(p) || p.closest('nav, footer, td, th, li, figure, [aria-hidden="true"]')) continue; const s = cs(p); if (parseFloat(s.fontSize) < 14) continue;
    const lines = lineTops(p); if (lines.length < 3) continue; const chars = p.textContent.trim().replace(/\s+/g, ' ').length; const cpl = chars / lines.length;
    if (cpl > 90) out['line-length'].push({sel: sel(p), characters_per_line: Math.round(cpl), width_px: Math.round(rc(p).width), text: txt(p).slice(0, 40)}); }

  // ---- clipped, spilling and overlapping text
  for (const el of document.querySelectorAll('body *')) { if (!vis(el) || deco(el) || el.namespaceURI === SVGNS) continue; const s = cs(el);
    const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (direct && /(hidden|clip)/.test(s.overflowX + s.overflowY) && s.textOverflow !== 'ellipsis' && !(s.webkitLineClamp && s.webkitLineClamp !== 'none')) {
      const dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
      if ((dy > 3 && /(hidden|clip)/.test(s.overflowY)) || (dx > 3 && /(hidden|clip)/.test(s.overflowX))) out['text-clipped'].push({sel: sel(el), hidden_px: {x: Math.max(0, dx), y: Math.max(0, dy)}, text: txt(el)}); }
    if (direct && (isInter(el) || hasBox(el)) && s.overflowX === 'visible' && s.display !== 'inline') { const r = rc(el); const rg = document.createRange(); rg.selectNodeContents(el); const q = rg.getBoundingClientRect();
      if (q.width > 0 && (q.right > r.right + 2 || q.left < r.left - 2) && q.width > r.width + 2) out['text-spill'].push({sel: sel(el), box_px: Math.round(r.width), text_px: Math.round(q.width), text: txt(el)}); } }
  // a message marked hidden in the markup but displayed all the same (a display rule beats the hidden attribute)
  for (const el of document.querySelectorAll('[hidden]:not([hidden="until-found"])')) { const s = cs(el), r = rc(el); if (s.display !== 'none' && s.visibility !== 'hidden' && r.width > 1 && r.height > 1 && txt(el)) out['false-feedback'].push({sel: sel(el), text: txt(el).slice(0, 60), note: 'marked hidden in the markup but displayed: a display rule overrides the hidden attribute'}); }
  const clippedAt = (el, x, y) => { let a = el.parentElement; while (a && a !== document.documentElement) { const s = cs(a); if (/(auto|scroll|hidden|clip)/.test(s.overflowY + ' ' + s.overflowX)) { const q = a.getBoundingClientRect(); if (x < q.left - 1 || x > q.right + 1 || y < q.top - 1 || y > q.bottom + 1) return true; } a = a.parentElement; } return false; };
  { const leaves = []; for (const el of seen) { if (el.namespaceURI === SVGNS || !el.isConnected) continue; const rg = document.createRange(); const tn = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()); if (!tn.length) continue;
      rg.selectNodeContents(tn[0]); for (const r of rg.getClientRects()) { if (r.width > 4 && r.height > 4 && !clippedAt(el, r.left + r.width / 2, r.top + r.height / 2)) leaves.push({el, r}); } if (leaves.length > 900) break; }
    leaves.sort((a, b) => a.r.top - b.r.top); const seenPair = new Set();
    for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length && leaves[j].r.top < leaves[i].r.bottom; j++) { const a = leaves[i], b = leaves[j]; if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
        const w = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), h = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top); if (w <= 2 || h <= 2) continue;
        const frac = (w * h) / Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
        const pk = sel(a.el) + '|' + sel(b.el); if (seenPair.has(pk)) continue;
        if (frac > 0.25 && out['text-overlap'].length < 12) seenPair.add(pk), out['text-overlap'].push({a: sel(a.el), b: sel(b.el), overlap_share: +frac.toFixed(2), text_a: txt(a.el).slice(0, 30), text_b: txt(b.el).slice(0, 30)}); } }

  // ---- sibling groups and rows
  const groups = [];
  for (const parent of document.querySelectorAll('body *')) { if (!vis(parent) || parent.namespaceURI === SVGNS) continue; const kids = [...parent.children].filter(vis); if (kids.length < 2) continue;
    const by = {}; for (const k of kids) { const c = k.tagName + '.' + [...k.classList].sort().join('.'); (by[c] = by[c] || []).push(k); }
    for (const els of Object.values(by)) if (els.length >= 2) groups.push({parent, els}); }
  const rowsOf = els => { const rows = []; for (const e of els) { const t = rc(e).top; const R = rows.find(r => Math.abs(r.t - t) <= 3); if (R) R.els.push(e); else rows.push({t, els: [e]}); } return rows.sort((a, b) => a.t - b.t); };
  const gapVals = [];
  for (const {parent, els} of groups) { const ps = cs(parent); const layoutParent = ps.display.includes('grid') || (ps.display.includes('flex') && ps.flexWrap === 'wrap'); const rows = rowsOf(els);
    if (layoutParent && els.length >= 3 && rows.length >= 2) { const first = rows[0].els, last = rows[rows.length - 1].els;
      if (last.length === 1 && first.length >= 2) { const w0 = rc(first[0]).width, wl = rc(last[0]).width, lr = rc(last[0]);
        const shares = [...parent.children].some(k => k !== last[0] && vis(k) && rc(k).top < lr.bottom - 4 && rc(k).bottom > lr.top + 4);   // another child of any kind fills the row
        if (wl < w0 * 1.3 && !shares) out['grid-lone-item'].push({sel: sel(parent), items: els.length, per_row: first.length, item: txt(last[0]).slice(0, 30)}); } }
    for (const row of rows) { if (row.els.length < 2) continue; const cards = row.els; const boxy = cards.every(c => hasBox(c) || c.children.length >= 2);
      if (boxy && rc(cards[0]).height > 60) {
        const sig = c => [...c.querySelectorAll('*')].filter(vis).filter(d => d.tagName === 'svg' || !d.closest('svg')).filter(d => d.children.length === 0 || isInter(d) || d.tagName === 'IMG' || d.tagName === 'svg').map(d => ({d, k: d.tagName + '.' + [...d.classList].sort().join('.')}));
        const sigs = cards.map(sig); const once = k => sigs.every(s => s.filter(y => y.k === k).length === 1);
        const common = [...new Set(sigs[0].map(x => x.k))].filter(once); let worst = null; const tops0 = cards.map(c => rc(c).top);
        for (const k of common) { const rel = sigs.map((s, i) => rc(s.find(y => y.k === k).d).top - tops0[i]); const spread = Math.max(...rel) - Math.min(...rel);
          if (spread > 4 && (!worst || spread > worst.spread)) worst = {part: k.toLowerCase(), spread: Math.round(spread), sample: txt(sigs[0].find(y => y.k === k).d).slice(0, 24)}; }
        const bigs = cards.map(c => { let best = null, bs = 0; for (const d of c.querySelectorAll('*')) { if (!vis(d) || ![...d.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue; const f = parseFloat(cs(d).fontSize); if (f > bs) { bs = f; best = d; } } return best ? {d: best, f: bs} : null; });
        if (bigs.every(Boolean) && bigs.every(b => Math.abs(b.f - bigs[0].f) < 0.5 && /\d/.test(b.d.textContent) && b.d.textContent.trim().length <= 14) && bigs[0].f >= 20) { const bots = bigs.map(b => rc(b.d).bottom), sp = Math.max(...bots) - Math.min(...bots);
          if (sp > 3) { out['tile-baseline'].push({sel: sel(cards[0]), tiles: cards.length, value_px: bigs[0].f, spread_px: Math.round(sp), values: bigs.map(b => b.d.textContent.trim()).slice(0, 6)}); worst = null; } }
        const barLike = common.some(k => { const ds = sigs.map(s => s.find(y => y.k === k).d); if (ds.some(d => txt(d) || d.tagName === 'IMG' || d.tagName === 'svg')) return false; const hs = ds.map(d => rc(d).height); return Math.max(...hs) > 30 && Math.max(...hs) > 2 * Math.max(4, Math.min(...hs)); });   // an empty box whose height differs from card to card is a bar: this is a column chart
        const kidsH = cards.map(c => [...c.children].map(k => ({h: rc(k).height, drawn: !/(rgba\(0, 0, 0, 0\)|transparent)/.test(cs(k).backgroundColor)})));
        const colChart = cards.every(c => rc(c).width <= 120) && kidsH[0].some((k0, i) => { const ks = kidsH.map(k => k[i]).filter(Boolean); if (ks.length < cards.length || !ks.every(k => k.drawn)) return false; const hs = ks.map(k => k.h); return Math.max(...hs) > 30 && Math.max(...hs) > 2 * Math.max(4, Math.min(...hs)); });   // narrow columns holding a filled box of varying height: a column chart with its labels
        if (barLike || colChart) worst = null;
        if (worst && common.length >= 2) out['card-rows'].push({sel: sel(cards[0]), cards: cards.length, part: worst.part, part_text: worst.sample, spread_px: worst.spread}); }
      const med = cards.map(c => [...c.querySelectorAll('img, video, picture, canvas, [class*=media], [class*=thumb], [class*=image]')].filter(vis)[0]).filter(Boolean);
      if (med.length === cards.length) { const rs = med.map(m => { const r = rc(m); return r.width / r.height; }); const mn = Math.min(...rs), mx = Math.max(...rs);
        if (mn > 0 && mx / mn > 1.03 && rc(med[0]).width > 40) out['media-ratios'].push({sel: sel(med[0]), set: med.length, ratios: rs.map(x => +x.toFixed(2))}); }
      const icons = cards.map(c => c.querySelector('svg, img[class*=icon], i:empty')).filter(i => i && vis(i));
      if (icons.length === cards.length && icons.length >= 2) { const ws = icons.map(i => Math.round(rc(i).width)); if (Math.max(...ws) - Math.min(...ws) > 1 && Math.max(...ws) <= 64) out['icon-sizes'].push({sel: sel(cards[0]), sizes: ws}); }
      if (row.els.every(hasBox) && !row.els.some(e => /^(TR|TD|TH|LI|BUTTON|A|INPUT|SELECT|LABEL)$/.test(e.tagName))) { const xs = row.els.map(rc).sort((a, b) => a.left - b.left);
        if (!xs.some(r => r.height < 60 || r.width < 120)) for (let i = 1; i < xs.length; i++) { const g = xs[i].left - xs[i - 1].right; if (g >= 0 && g <= 80) gapVals.push({g, where: sel(parent)}); } } } }
  { gapVals.sort((a, b) => a.g - b.g); const cl = []; for (const v of gapVals) { const c = cl[cl.length - 1]; if (c && v.g - c.max <= 1.5) { c.max = v.g; c.n++; c.where.add(v.where); } else cl.push({min: v.g, max: v.g, n: 1, where: new Set([v.where])}); }
    if (cl.length > 1) out['gutter-drift'].push({gaps: cl.map(c => ({px: Math.round((c.min + c.max) / 2), count: c.n, where: [...c.where].slice(0, 3)}))}); }

  { const byParent = {}; for (const ic of document.querySelectorAll('svg, img[class*=icon]')) { if (!vis(ic) || ic.closest('svg svg')) continue; const r = rc(ic); if (r.width > 40 || r.width < 8 || Math.abs(r.width - r.height) > 2) continue; const par = ic.parentElement; if (!par) continue;
      const k = par.tagName.toLowerCase() + '.' + [...par.classList].sort().join('.'); (byParent[k] = byParent[k] || []).push(Math.round(r.width));
      if (ic.tagName.toLowerCase() === 'svg') { let f = 0, o = 0; for (const sh of ic.querySelectorAll('path, circle, rect, polygon, ellipse, line, polyline')) { const c = cs(sh); const hasFill = c.fill && c.fill !== 'none' && !/rgba\(0, 0, 0, 0\)/.test(c.fill), hasStroke = c.stroke && c.stroke !== 'none' && parseFloat(c.strokeWidth) > 0; if (hasFill && !hasStroke) f++; else if (hasStroke && !hasFill) o++; }
        if (f + o) { const st = f > o ? 'filled' : 'outlined'; ((byParent['__style'] = byParent['__style'] || {})[k] = byParent['__style'][k] || {filled: 0, outlined: 0})[st]++; } } }
    const styles = byParent['__style'] || {}; delete byParent['__style'];
    for (const [k, ws] of Object.entries(byParent)) { const u = [...new Set(ws)].sort((a, b) => a - b); if (ws.length >= 3 && u[u.length - 1] - u[0] > 1 && !out['icon-sizes'].some(x => x.parent === k)) out['icon-sizes'].push({parent: k, icons: ws.length, sizes: u}); }
    for (const [k, st] of Object.entries(styles)) if (st.filled >= 1 && st.outlined >= 1 && st.filled + st.outlined >= 3) out['icon-sizes'].push({parent: k, filled_icons: st.filled, outlined_icons: st.outlined, note: 'filled and outlined icons mixed in one set'}); }
  // ---- control heights (neighbours only)
  { const ctrls = [...document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=hidden]), select, button, a[class*=btn], a[class*=button], a[class*=cta]')].filter(vis).map(e => ({e, r: rc(e)})).sort((a, b) => a.r.top - b.r.top || a.r.left - b.r.left);
    for (let i = 0; i < ctrls.length; i++) for (let j = i + 1; j < Math.min(ctrls.length, i + 8); j++) { const a = ctrls[i].r, b = ctrls[j].r; if (b.top > a.bottom) break;
        const gap = Math.max(b.left - a.right, a.left - b.right), vo = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (gap >= -1 && gap <= 24 && vo > Math.min(a.height, b.height) * 0.5 && Math.abs(a.height - b.height) > 2 && out['control-heights'].length < 20) out['control-heights'].push({a: sel(ctrls[i].e), b: sel(ctrls[j].e), heights: [Math.round(a.height), Math.round(b.height)]}); } }
  // ---- segment widths: the options of one switch (two to five choices in one shared box, exactly one filled as the selected one)
  { for (const p of document.querySelectorAll('body *')) { if (out['segment-widths'].length >= 8) break;
      if (!vis(p) || !hasBox(p) || p.matches('header, nav, footer, form, ul[class*=pag], ol[class*=pag], [class*=pagination]') || p.closest('nav, [role=navigation], svg')) continue;
      const kids = [...p.children].filter(k => vis(k) && !(k.matches('input') && rc(k).width <= 2)); if (kids.length < 2 || kids.length > 5) continue;
      const face = k => k.matches('button, a, label, [role=tab], [role=radio], [role=button], [role=option]') ? k : (k.children.length === 1 && k.firstElementChild.matches('button, a, label, [role=tab], [role=radio], [role=button]') ? k.firstElementChild : null);
      const faces = kids.map(face); if (faces.some(f => !f)) continue;
      const rs = faces.map(rc), pr = rc(p);
      if (rs.some(r => Math.abs(r.top - rs[0].top) > 3 || Math.abs(r.height - rs[0].height) > 3)) continue;                       // one row, one height
      if (rs.slice(1).some((r, i) => r.left - rs[i].right > 12 || r.left - rs[i].right < -2)) continue;                             // the options touch or nearly touch
      if (pr.width - (rs[rs.length - 1].right - rs[0].left) > 24) continue;                                                        // the box wraps the options and nothing else
      if (faces.filter(hasBox).length !== 1) continue;                                                                             // one option is filled: the selected one
      const ws = rs.map(r => Math.round(r.width)), mx = Math.max(...ws), mn = Math.min(...ws);
      if (mx - mn > 8 && mx / mn > 1.1) out['segment-widths'].push({sel: sel(p), options: faces.map(f => txt(f).slice(0, 28)), widths: ws, widest_to_narrowest: Math.round(mx / mn * 100) / 100}); } }

  // ---- nested radius (only when the inset is smaller than the outer radius)
  const rad = el => parseFloat(cs(el).borderTopLeftRadius) || 0;
  for (const outer of document.querySelectorAll('body *')) { if (!vis(outer) || !hasBox(outer)) continue; const R = rad(outer); if (R < 6) continue; const ro = rc(outer);
    for (const inner of outer.querySelectorAll('*')) { if (!vis(inner) || !(hasBox(inner) || inner.tagName === 'IMG')) continue; const ri = rc(inner), dx = ri.left - ro.left, dy = ri.top - ro.top;
      if (dx < 1 || dy < 1 || dx >= R || Math.abs(dx - dy) > 3) continue; if (ri.width < ro.width * 0.5 || ri.height < ro.height * 0.3) continue;
      const r = rad(inner); if (r === 0) continue; const expected = R - dx;
      if (r > expected + 3) out['radius-nested'].push({outer: sel(outer), inner: sel(inner), outer_radius: R, inset: Math.round(dx), inner_radius: r, concentric_would_be: Math.round(expected)});
      break; } }

  // ---- near-miss left edges, padding asymmetry, heading proximity
  { const blocks = [...document.querySelectorAll('h1,h2,h3,h4,p,ul,ol,table,figure,img,form,section > div, main > div, article, [class*=card], [class*=tile], [class*=panel]')].filter(vis)
      .filter(e => { const r = rc(e), s = cs(e); return r.width >= 120 && !(s.textAlign === 'center' && /^(H\d|P)$/.test(e.tagName)) && !e.closest('nav, footer, table, li'); });
    // an edge is compared only with edges inside the same box, or inside boxes that start at the same left edge:
    // content of two differently padded boxes is nesting, not a line that was missed
    const boxLeft = b => { let up = b.parentElement; while (up && up !== document.body && !hasBox(up)) up = up.parentElement; return up && up !== document.body ? Math.round(rc(up).left) : 0; };
    const groups = {}; for (const b of blocks) { const g = boxLeft(b); (groups[g] = groups[g] || []).push(b); }
    for (const grp of Object.values(groups)) { const edges = {}; for (const b of grp) { const x = Math.round(rc(b).left); (edges[x] = edges[x] || []).push(b); } const keys = Object.keys(edges).map(Number);
      for (const x of keys) { if (edges[x].length > 2) continue; const near = keys.filter(y => y !== x && Math.abs(y - x) >= 2 && Math.abs(y - x) <= 6 && edges[y].length >= 3);
        if (near.length) out['edge-near-miss'].push({sel: sel(edges[x][0]), left: x, common_edge: near[0], off_by_px: Math.abs(near[0] - x), text: txt(edges[x][0]).slice(0, 30)}); } } }
  { const enclosed = el => { const s = cs(el), bg = parse(s.backgroundColor), pbg = el.parentElement ? bgOf(el.parentElement) : null;
      const diff = bg && bg.a > 0.05 && pbg && !pbg.unknown && (Math.abs(bg.r - pbg.r) + Math.abs(bg.g - pbg.g) + Math.abs(bg.b - pbg.b) > 6);
      return diff || ['Top', 'Right', 'Bottom', 'Left'].every(k => parseFloat(s['border' + k + 'Width']) > 0) || s.boxShadow !== 'none'; };
    for (const box of document.querySelectorAll('body *')) { if (!vis(box) || box.namespaceURI === SVGNS || !enclosed(box)) continue; const kids = [...box.children].filter(vis); if (kids.length < 2) continue;
      const s = cs(box); if (s.display.includes('grid') || (s.display.includes('flex') && s.flexDirection.startsWith('row'))) continue; const r = rc(box); if (r.height > 900 || r.height < 40) continue;
      const first = kids[0], last = kids[kids.length - 1]; const top = rc(first).top - r.top - parseFloat(s.borderTopWidth), bottom = r.bottom - parseFloat(s.borderBottomWidth) - rc(last).bottom;
      const mb = parseFloat(cs(last).marginBottom), mt = parseFloat(cs(first).marginTop);
      if (Math.min(top, bottom) >= 4 && ((bottom - top > 8 && mb > 0) || (top - bottom > 8 && mt > 0))) out['pad-asymmetry'].push({sel: sel(box), top: Math.round(top), bottom: Math.round(bottom), cause: bottom > top ? 'last child margin-bottom ' + mb + 'px' : 'first child margin-top ' + mt + 'px'}); } }
  for (const h of document.querySelectorAll('h2, h3')) { if (!vis(h)) continue; const p = h.previousElementSibling, n = h.nextElementSibling; if (!p || !n || !vis(p) || !vis(n)) continue; const r = rc(h);
    if (parseFloat(cs(p).fontSize) < parseFloat(cs(h).fontSize) * 0.8 && txt(p).length < 60 && rc(p).height < 40) continue;
    const above = r.top - rc(p).bottom, below = rc(n).top - r.bottom; if (above >= 0 && below > above) out['heading-proximity'].push({sel: sel(h), above: Math.round(above), below: Math.round(below), text: txt(h)}); }
  // a heading pressed against the full-width band above it (the first heading of a section that has no top space)
  { const bandsAbove = [...document.querySelectorAll('header, section, div, nav, aside')].filter(e => vis(e) && hasBox(e)).filter(e => { const r = rc(e); return r.width >= innerWidth * 0.9 && r.height >= 40; });
    for (const h of document.querySelectorAll('h1, h2, h3')) { if (!vis(h) || out['heading-proximity'].some(x => x.sel === sel(h))) continue; const r = rc(h);
      const b = bandsAbove.find(e => !e.contains(h) && !h.contains(e) && rc(e).bottom <= r.top + 1 && r.top - rc(e).bottom < 16 && parse(cs(e).backgroundColor) && bgOf(h.parentElement || h) && ratio(parse(cs(e).backgroundColor), bgOf(h.parentElement || h)) >= 1.5);
      if (b) out['heading-proximity'].push({sel: sel(h), above: Math.round(r.top - rc(b).bottom), band_above: sel(b), text: txt(h), note: 'heading sits against the band above it'}); } }

  // ---- chips, tables
  { const chips = {}; for (const el of document.querySelectorAll('body *')) { if (!vis(el) || !hasBox(el) || !el.classList.length || el.namespaceURI === SVGNS) continue; const r = rc(el), t = txt(el);
      if (r.height > 40 || r.height < 12 || !t || t.length > 32) continue; const k = el.tagName.toLowerCase() + '.' + [...el.classList].sort().join('.'); (chips[k] = chips[k] || []).push({h: Math.round(r.height * 2) / 2, t}); }
    for (const [k, list] of Object.entries(chips)) { if (list.length < 3) continue; const hs = [...new Set(list.map(x => x.h))]; if (Math.max(...hs) - Math.min(...hs) > 1.5) out['chip-heights'].push({component: k, heights: hs.sort((a, b) => a - b), examples: list.slice(0, 3).map(x => x.t)}); } }
  const num = s => { let t = s.replace(/[\s  ]/g, '').replace(/[£$€%]/g, '').replace(/^\((.*)\)$/, '-$1').replace('−', '-'); if (!/^[-+]?[\d.,]+$/.test(t)) return null;
    if (/,\d{1,2}$/.test(t) && !/\.\d/.test(t)) t = t.replace(/\./g, '').replace(',', '.'); else t = t.replace(/,/g, ''); const v = parseFloat(t); return isFinite(v) ? v : null; };
  for (const tb of document.querySelectorAll('table')) { if (!vis(tb)) continue; const head = tb.tHead && tb.tHead.rows[0]; const body = tb.tBodies[0]; if (!body) continue; const rows = [...tb.querySelectorAll('tbody tr')]; if (rows.length && cs(rows[0]).display !== 'table-row') continue;   // rows restyled as stacked cards: column rules do not apply
    if (head && rows.length >= 2) [...head.cells].forEach((th, ci) => { if (!vis(th)) return; const tds = rows.slice(0, 12).map(r => r.cells[ci]).filter(Boolean).filter(vis); if (!tds.length) return;
      const al = e => { const a = cs(e).textAlign; return a === 'end' || a === 'right' || a === '-webkit-right' ? 'right' : a === 'center' || a === '-webkit-center' ? 'center' : 'left'; };
      const counts = {}; tds.forEach(td => counts[al(td)] = (counts[al(td)] || 0) + 1); const major = Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
      const vals = tds.map(td => txt(td)); const numeric = vals.filter(v => /^[\s(\-−+]*[£$€]?\s?[\d.,\s  ]+%?\)?\s*[A-Za-z€%£$/]{0,5}$/.test(v) && /\d/.test(v)).length >= tds.length * 0.6;
      const ident = /(^|\b)(id|no\.?|number|nr|year|code|ref|reference|postcode|zip|phone|sku|order|invoice|job|#)(\b|$)/i.test(txt(th)) || (numeric && vals.every(v => /^\d{4,}$/.test(v)));
      if (al(th) !== major) out['table-align'].push({table: sel(tb), column: txt(th), header: al(th), cells: major, numeric});
      else if (numeric && !ident && major !== 'right') out['table-align'].push({table: sel(tb), column: txt(th), header: al(th), cells: major, numeric, issue: 'numeric column not right-aligned'}); });
    if (rows.length > 15) { const hd = tb.tHead || tb.querySelector('tr'); const sticky = hd && [hd, ...hd.querySelectorAll('th, td, tr')].some(e => cs(e).position === 'sticky'); if (!sticky) out['table-sticky'].push({table: sel(tb), body_rows: rows.length}); }
    const all = [...tb.querySelectorAll('tbody tr, tfoot tr')]; const tot = (tb.tFoot && tb.tFoot.rows[0]) || all.find(r => /\b(total|sum|all|overall|iš viso|suma|gesamt|totale?)\b/i.test(r.cells[0] ? r.cells[0].textContent : ''));
    if (tot) { const dataRows = [...tb.querySelectorAll('tbody tr')].filter(r => r !== tot && vis(r)); [...tot.cells].forEach((c, ci) => { if (ci === 0) return; const tv = num(c.textContent.trim()); if (tv === null) return; const isPct = /%/.test(c.textContent) || /%|share|rate|average|avg|mean|per /i.test(head && head.cells[ci] ? head.cells[ci].textContent : '');
        const vs = dataRows.map(r => r.cells[ci] ? num(r.cells[ci].textContent.trim()) : null); if (vs.some(v => v === null) || vs.length < 2) return; const sum = vs.reduce((a, b) => a + b, 0);
        const isSum = vs.every(v => v >= 0) && tv > Math.max(...vs);      // an average or rate never exceeds its largest row
        if (!isPct && isSum && Math.abs(sum - tv) > Math.max(0.51, Math.abs(tv) * 0.0005)) out['table-total'].push({table: sel(tb), column: head && head.cells[ci] ? txt(head.cells[ci]) : 'column ' + (ci + 1), total_shown: c.textContent.trim(), sum_of_rows: +sum.toFixed(2)}); }); } }

  // ---- motion under the reduced-motion setting, hover-only controls
  try { for (const a of document.getAnimations()) { const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : {}; if (a.playState === 'running' && (t.iterations === Infinity || t.duration > 1500) && a.effect && a.effect.target && vis(a.effect.target)) out['motion-reduce'].push({sel: sel(a.effect.target), iterations: String(t.iterations), duration_ms: t.duration}); } } catch (e) {}
  { const seenH = new Set(), focusRules = []; const hov = [];
    const scan = rules => { for (const r of rules) { if (r.cssRules && !(r.selectorText)) { try { scan(r.cssRules); } catch (e) {} continue; } if (!r.selectorText) continue;
        if (/:focus(-within|-visible)?/.test(r.selectorText)) focusRules.push(r.selectorText); if (r.selectorText.includes(':hover') && /(opacity|visibility|display|transform|max-height|height|clip)/.test(r.style.cssText)) hov.push(r.selectorText); } };
    for (const ss of document.styleSheets) { try { scan(ss.cssRules); } catch (e) {} }
    for (const st of hov) for (const part of st.split(',')) { if (!part.includes(':hover')) continue; const base = part.replace(/:hover/g, '').trim(); let els = []; try { els = [...document.querySelectorAll(base)]; } catch (e) { continue; }
        for (const el of els) { if (seenH.has(el)) continue; const s = cs(el), r = rc(el); const hid = parseFloat(s.opacity) <= 0.05 || s.visibility === 'hidden' || s.display === 'none' || r.height === 0; if (!hid) continue;
          if (s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0.05 && el.parentElement && rc(el.parentElement).height === 0 && rc(el.parentElement).width === 0) continue;   // inside a block that is not displayed at this width
          if (/:hover[^\s>+~]*$/.test(part.trim()) && (s.display === 'none' || s.visibility === 'hidden' || r.height === 0)) continue;   // the rule hovers the element itself, which cannot be hovered while it is not there
          if (!(el.matches(INTER) || el.querySelector(INTER))) continue; seenH.add(el);
          const fbase = focusRules.some(f => f.split(',').some(p => { const b = p.replace(/:focus(-within|-visible)?/g, '').trim(); try { return el.matches(b) || !!el.closest(b); } catch (e) { return false; } }));
          out['hover-only'].push({sel: sel(el), controls: [...(el.matches(INTER) ? [el] : el.querySelectorAll(INTER))].slice(0, 3).map(c => (c.innerText || c.getAttribute('aria-label') || c.tagName).trim().slice(0, 20)), shown_by: part.trim().slice(0, 60), a_focus_rule_also_matches: fbase}); } } }

  // ---- controls that stay covered by fixed bars; safe areas
  const skipLink = el => el.tagName === 'A' && /^#/.test(el.getAttribute('href') || '') && /^skip\b/i.test(txt(el));
  if (opts.obscured) { const y0 = scrollY; for (const el of inter.slice(0, 120)) { if (cs(el).position === 'fixed' || el.closest('[data-uic-fixed]') || skipLink(el)) continue; let fx = el.parentElement, isFixed = false; while (fx && fx !== document.body) { if (/(fixed|sticky)/.test(cs(fx).position)) { isFixed = true; break; } fx = fx.parentElement; } if (isFixed) continue;
      el.scrollIntoView({block: 'center', inline: 'nearest', behavior: 'instant'}); const r = rc(el); if (r.width < 2 || r.height < 2) continue; const px = Math.min(VW - 1, Math.max(0, r.left + r.width / 2)), py = r.top + r.height / 2; if (py < 0 || py > VH) continue;
      const hit = document.elementFromPoint(px, py); if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue; if (hit.closest('label') && hit.closest('label').contains(el)) continue;
      let f = hit; while (f && f !== document.body && !/(fixed|sticky)/.test(cs(f).position)) f = f.parentElement;
      if (f && f !== document.body) out['control-obscured'].push({sel: sel(el), text: txt(el).slice(0, 30), covered_by: sel(f), note: 'still covered when scrolled as far as the page allows'}); }
    scrollTo(0, document.documentElement.scrollHeight); let n = 0;
    for (const el of seen) { if (!el.isConnected || n >= 4) continue; const r = rc(el); if (r.bottom <= 0 || r.top >= VH || r.width < 4) continue; let fx = el; while (fx && fx !== document.body && !/(fixed|sticky)/.test(cs(fx).position)) fx = fx.parentElement; if (fx && fx !== document.body) continue;
      const hit = document.elementFromPoint(Math.min(VW - 1, Math.max(0, r.left + Math.min(r.width, 40) / 2)), r.top + r.height / 2); if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
      let f = hit; while (f && f !== document.body && !/(fixed|sticky)/.test(cs(f).position)) f = f.parentElement;
      if (f && f !== document.body && rc(f).top > VH / 2 && !clippedAt(el, r.left + Math.min(r.width, 40) / 2, r.top + r.height / 2)) { n++; out['control-obscured'].push({sel: sel(el), text: txt(el).slice(0, 30), covered_by: sel(f), kind: 'text', note: 'covered at the end of the scroll: the page has no room below its last content'}); } }
    scrollTo(0, y0); }
  if (opts.insets && out._doc.viewport_fit_cover) { const [it, , ib] = opts.insets; const fixed = [...document.querySelectorAll('body *')].filter(e => vis(e) && /(fixed|sticky)/.test(cs(e).position));
    const chk = (e, edge) => { const items = [...(isInter(e) ? [e] : []), ...e.querySelectorAll(INTER)].filter(vis).filter(c => !skipLink(c)); for (const c of items) { const r = rc(c); const ov = edge === 'bottom' ? r.bottom - (VH - ib) : it - r.top; if (ov > 2) { out['safe-area'].push({sel: sel(c), edge, inside_unsafe_zone_px: Math.round(ov), bar: sel(e), text: txt(c).slice(0, 20) || c.getAttribute('aria-label')}); return; } } };
    for (const e of fixed) { const r = rc(e); if (ib && r.bottom > VH - ib + 2 && r.top > VH / 2) chk(e, 'bottom'); if (it && r.top < it - 2 && r.bottom < VH / 2) chk(e, 'top'); }
    if (it && scrollY === 0) for (const el of seen) { if (!el.isConnected) continue; const r = rc(el); if (r.top < it - 2 && r.bottom > 0 && r.height < 200 && !el.closest('[data-uic-skip]') && !skipLink(el) && !clippedAt(el, r.left + Math.min(r.width, 40) / 2, r.top + r.height / 2)) { let f = el; while (f && f !== document.body && !/(fixed|sticky)/.test(cs(f).position)) f = f.parentElement; if (f && f !== document.body) continue; out['safe-area'].push({sel: sel(el), edge: 'top', inside_unsafe_zone_px: Math.round(it - r.top), text: txt(el).slice(0, 30)}); break; } } }

  // ---- census (tokens and design signals)
  const radii = {}, radKind = {}, shadows = {}, pads = [], bgCols = {}, strokes = {}; let gradients = 0, blurs = 0, glows = 0, pills = 0, eyebrows = 0, centred = 0, blocksN = 0;
  for (const el of document.querySelectorAll('body *')) { if (!vis(el) || el.namespaceURI === SVGNS) continue; const s = cs(el), r = rc(el);
    if (hasBox(el)) { const rr = s.borderTopLeftRadius; const rv = parseFloat(rr); if (rr !== '0px') { const pill = rr.endsWith('%') || rv >= Math.min(r.height, r.width) / 2 - 0.5; const key = pill ? 'pill or circle' : rr; radii[key] = (radii[key] || 0) + 1;
        // one radius for cards and panels (boxes of 160 by 60px or more that are not inside another rounded box); a control radius beside a card radius is a system, not drift
        if (!pill) { let up = el.parentElement, nested = false; while (up && up !== document.body) { if (hasBox(up) && cs(up).borderTopLeftRadius !== '0px') { nested = true; break; } up = up.parentElement; }
          const kind = !nested && r.width >= 160 && r.height >= 60 ? 'cards and panels' : null; if (kind) { radKind[kind] = radKind[kind] || {}; radKind[kind][rr] = (radKind[kind][rr] || 0) + 1; } } }
      if (s.boxShadow !== 'none') { shadows[s.boxShadow] = (shadows[s.boxShadow] || 0) + 1; const m = s.boxShadow.match(/rgba?\(([^)]+)\)[^,]*?(-?[\d.]+)px (-?[\d.]+)px ([\d.]+)px/); if (m) { const p = m[1].split(/[ ,\/]+/).map(Number); if (parseFloat(m[4]) >= 24 && Math.max(p[0], p[1], p[2]) - Math.min(p[0], p[1], p[2]) > 60 && (p.length < 4 || p[3] > 0.2)) glows++; } }
      const bg = parse(s.backgroundColor); if (bg && bg.a > 0.5 && r.width * r.height > 2000) bgCols[[bg.r, bg.g, bg.b].join(',')] = 1;
      if (/gradient\(/.test(s.backgroundImage) && r.width * r.height > 12000) gradients++;
      const t = txt(el); if (!isInter(el) && !el.closest(INTER) && r.height <= 32 && r.height >= 14 && t && t.length <= 24 && el.children.length <= 1 && parseFloat(rr) >= r.height / 2 - 1) pills++; }
    if (s.backdropFilter && s.backdropFilter !== 'none') blurs++;
    if (s.textTransform === 'uppercase' && parseFloat(s.fontSize) <= 13 && parseFloat(s.letterSpacing) > 0 && el.children.length === 0 && txt(el).length <= 40 && !isInter(el) && !el.closest('th, ' + INTER)) eyebrows++;
    if (/^(H\d|P)$/.test(el.tagName)) { blocksN++; if (s.textAlign === 'center') centred++; } }
  for (const sv of document.querySelectorAll('svg')) { if (!vis(sv)) continue; const r = rc(sv); if (r.width > 40) continue; const w = cs(sv).strokeWidth; const k = parseFloat(w) * (r.width / (sv.viewBox && sv.viewBox.baseVal && sv.viewBox.baseVal.width || r.width)); if (cs(sv).stroke !== 'none' || sv.getAttribute('stroke')) strokes[(Math.round(k * 4) / 4) + 'px at ' + Math.round(r.width) + 'px'] = 1; }
  for (const sec of document.querySelectorAll('body > section, main > section, body > header, body > footer, main > div, body > main > *')) { if (!vis(sec)) continue; const s = cs(sec); pads.push({sel: sel(sec), top: s.paddingTop, bottom: s.paddingBottom}); }
  { const sp = pads.filter(x => /section/i.test(x.sel) || true).flatMap(x => [parseFloat(x.top), parseFloat(x.bottom)]).filter(v => v >= 24).sort((a, b) => a - b); const steps = []; for (const v of sp) { if (!steps.length || v - steps[steps.length - 1] >= 8) steps.push(v); }
    if (steps.length > 2) out['section-rhythm'].push({distinct_vertical_paddings_px: steps, sections: pads.length});
    const rs = Object.keys(radii).filter(k => k !== 'pill or circle').map(parseFloat).sort((a, b) => a - b);
    if (rs.length > 3) out['radius-drift'].push({radius_steps_px: rs, all_within_4px_of_a_neighbour: rs.every((v, i) => (i > 0 && v - rs[i - 1] <= 4) || (i < rs.length - 1 && rs[i + 1] - v <= 4))});
    else for (const [kind, m] of Object.entries(radKind)) { const v = Object.keys(m).map(parseFloat).sort((a, b) => a - b); if (v.length >= 2 && v.some((x, i) => i > 0 && x - v[i - 1] <= 4)) { out['radius-drift'].push({same_kind_of_component: kind, radius_steps_px: v, all_within_4px_of_a_neighbour: true}); break; } }
    if (Object.keys(shadows).length > 2) out['shadow-drift'].push({shadow_styles: Object.keys(shadows).length, values: Object.keys(shadows).slice(0, 4)}); }
  let emoji = 0; try { const re = /\p{Extended_Pictographic}/u; for (const el of document.querySelectorAll('button, a, h1, h2, h3, h4, nav *, label, th, li, [class*=icon], [class*=badge]')) { if (!vis(el)) continue; if ([...el.childNodes].some(n => n.nodeType === 3 && re.test(n.textContent))) emoji++; } } catch (e) {}
  const szKeys = Object.keys(sizes).map(Number).sort((a, b) => a - b); const near = []; for (let i = 1; i < szKeys.length; i++) if (szKeys[i] - szKeys[i - 1] < 1 && sizes[szKeys[i]] >= 2 && sizes[szKeys[i - 1]] >= 2) near.push([szKeys[i - 1], szKeys[i]]);
  if (szKeys.length > 9 || near.length) out['type-scale-drift'].push({distinct_sizes: szKeys.length, sizes_px: szKeys, near_duplicates: near});
  const first = []; for (const el of seen) { if (!el.isConnected) continue; const r = rc(el); if (r.top >= 0 && r.top < VH && r.width > 0) first.push({px: parseFloat(cs(el).fontSize), text: txt(el).slice(0, 40)}); } first.sort((a, b) => b.px - a.px);
  const prim = []; for (const el of inter) { const r = rc(el); if (r.top >= VH || r.bottom <= 0 || !/^(A|BUTTON|INPUT)$/.test(el.tagName)) continue; const bg = parse(cs(el).backgroundColor); if (!bg || bg.a < 0.9) continue; const pb = bgOf(el.parentElement || el); if (pb.unknown) continue;
    const sat = Math.max(bg.r, bg.g, bg.b) - Math.min(bg.r, bg.g, bg.b); if (ratio(bg, pb) >= 3 && (sat > 40 || lum(bg) < 0.08) && r.height >= 28 && txt(el)) prim.push({text: txt(el).slice(0, 30), color: `rgb(${bg.r},${bg.g},${bg.b})`, w: Math.round(r.width), h: Math.round(r.height)}); }
  const h1 = document.querySelector('h1'); const navs = [...document.querySelectorAll('nav')].filter(vis).map(n => ({items: [...n.querySelectorAll('a, button')].filter(vis).length, current_marked: !!n.querySelector('[aria-current]')}));
  out._census = {radii, shadows: Object.keys(shadows).length, shadow_values: Object.keys(shadows).slice(0, 6), font_sizes: sizes, font_families: fams, font_weights: weights, text_colours: Object.keys(textCols).length, surface_colours: Object.keys(bgCols).length,
    section_padding: pads, icon_strokes: Object.keys(strokes),
    decoration: {large_gradients: gradients, blur_surfaces: blurs, glow_shadows: glows, pill_badges: pills, uppercase_eyebrow_labels: eyebrows, emoji_in_interface: emoji, centred_text_share: blocksN ? +(centred / blocksN).toFixed(2) : 0},
    first_screen: {height: VH, h1_inside: h1 ? rc(h1).bottom <= VH : null, largest_text: first.slice(0, 3), filled_buttons: prim.slice(0, 8), interactive_elements: inter.filter(e => { const r = rc(e); return r.top < VH && r.bottom > 0; }).length}, navigation: navs};
  // dark styles present?
  let dark = false; const sd = rules => { for (const r of rules) { if (r.conditionText && /prefers-color-scheme:\s*dark/.test(r.conditionText)) dark = true; if (r.cssRules) { try { sd(r.cssRules); } catch (e) {} } } };
  for (const ss of document.styleSheets) { try { sd(ss.cssRules); } catch (e) {} } out._doc.dark_styles = dark;
  // fonts requested and available
  const probe = document.createElement('span'); probe.textContent = 'mmmmmmmmmlliWWW 0123456789'; probe.style.cssText = 'position:absolute;left:-9999px;top:0;font-size:72px;white-space:nowrap;visibility:hidden'; document.body.appendChild(probe);
  const wOf = f => { probe.style.fontFamily = f; return probe.getBoundingClientRect().width; }; const bm = wOf('monospace'), bs = wOf('serif'), bsa = wOf('sans-serif'); const fonts = [];
  const GENERIC = /^(serif|sans-serif|monospace|system-ui|ui-sans-serif|ui-serif|ui-monospace|ui-rounded|cursive|fantasy|emoji|math|-apple-system|blinkmacsystemfont)$/i; const stacks = new Set();
  for (const el of seen) { if (el.isConnected) stacks.add(cs(el).fontFamily); if (stacks.size > 12) break; }
  for (const st of stacks) { const names = st.split(',').map(x => x.trim().replace(/["']/g, '')); let used = null; const missing = [];
    for (const n of names) { if (GENERIC.test(n)) { used = used || n + ' (generic)'; break; } const ok = wOf(`"${n}", monospace`) !== bm || wOf(`"${n}", serif`) !== bs || wOf(`"${n}", sans-serif`) !== bsa; if (ok) { used = n; break; } missing.push(n); }
    fonts.push({stack: st.slice(0, 90), rendered_with: used, not_available_here: missing, generic: names.filter(n => GENERIC.test(n)).pop() || null}); }
  probe.remove(); out._fonts = fonts;
  // figures for cross-checking
  const figs = []; for (const el of seen) { if (!el.isConnected || el.namespaceURI === SVGNS) continue; const t = el.textContent.trim(); if (!/\d/.test(t) || t.length > 28) continue; const f = parseFloat(cs(el).fontSize); const inTotal = el.closest('tr') && /total|sum/i.test(el.closest('tr').textContent);
    if (f >= 20 || inTotal) { let lab = ''; const card = el.parentElement; if (card) lab = [...card.children].filter(c => c !== el).map(c => txt(c)).filter(Boolean)[0] || ''; if (inTotal) lab = 'table total row' + (el.closest('table').tHead && el.cellIndex != null ? ': ' + txt(el.closest('table').tHead.rows[0].cells[el.cellIndex] || el) : ''); figs.push({value: t, label: lab.slice(0, 50), sel: sel(el)}); } if (figs.length >= 40) break; }
  // the same label beside another number elsewhere in the text ("Open jobs 128" against "of 131 open jobs")
  { const norm = v => v.replace(/[\s\u00a0\u202f,]/g, ''); const texts = []; for (const el of seen) { if (!el.isConnected || el.namespaceURI === SVGNS) continue; for (const n of el.childNodes) if (n.nodeType === 3 && /\d/.test(n.textContent) && n.textContent.trim().length <= 160) texts.push({el, t: n.textContent.replace(/\s+/g, ' ').trim()}); }
    for (const f of figs) { const lab = f.label.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim(); if (lab.length < 8 || !/ /.test(lab) || /^table total/.test(lab)) continue; const own = norm((f.value.match(/\d[\d\s\u00a0\u202f,.]*/) || [''])[0]).replace(/\.$/, ''); if (!own) continue; const hits = [];
      for (const x of texts) { const low = x.t.toLowerCase(); const at = low.indexOf(lab); if (at < 0 || sel(x.el) === f.sel) continue; const before = (x.t.slice(Math.max(0, at - 14), at).match(/(\d[\d\s\u00a0\u202f,.]*)\s*$/) || [])[1], after = (x.t.slice(at + lab.length, at + lab.length + 14).match(/^[\s:]*(\d[\d\s\u00a0\u202f,.]*)/) || [])[1];
        const other = norm(before || after || '').replace(/\.$/, ''); if (other && other !== own && hits.length < 3) hits.push(x.t.slice(0, 80)); }
      if (hits.length) f.elsewhere = hits; } }
  out._figures = figs;
  return out;
}
"""

SNAP = r"""
() => { const vis = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect(); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05 && r.width > 0 && r.height > 0; };
  const texts = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let i = 0;
  while (w.nextNode()) { const n = w.currentNode, t = n.textContent.trim(); if (!t) continue; const p = n.parentElement; if (!p || ['SCRIPT', 'STYLE'].includes(p.tagName) || !vis(p)) continue;
    let path = '', e = p, d = 0; while (e && e !== document.body && d < 6) { path = e.tagName + (e.id ? '#' + e.id : '') + ':' + [...(e.parentElement ? e.parentElement.children : [])].indexOf(e) + '/' + path; e = e.parentElement; d++; }
    texts[path + (i++ % 1 === 0 ? [...p.childNodes].indexOf(n) : '')] = t.slice(0, 80); }
  const lists = [...document.querySelectorAll('tbody, ul, ol, [role=list], [class*=grid], [class*=list]')].slice(0, 60).map(c => ({k: c.tagName + '.' + c.className, n: [...c.children].filter(vis).length, s: vis(c.closest('section, article, figure, form, [class*=card], [class*=panel]') || c.parentElement || c),
    w: [...new Set((((c.closest('section, article, figure, form, [class*=card], [class*=panel]') || c.parentElement || c).innerText || '').toLowerCase().match(/[a-z\u00c0-\u024f]{3,}/g) || []))].slice(0, 400)}));
  const styles = [...document.querySelectorAll('input, select, textarea')].filter(vis).slice(0, 30).map(e => getComputedStyle(e).borderTopColor + getComputedStyle(e).outlineColor + getComputedStyle(e).boxShadow);
  const bs = getComputedStyle(document.body), de = document.documentElement;
  const root = de.className + '|' + [...de.attributes].map(a => a.name + '=' + a.value).join(';') + '|' + document.body.className + '|' + bs.backgroundColor + bs.color;
  let store = ''; try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); store += k + ':' + localStorage.getItem(k).length + ':' + localStorage.getItem(k).slice(-24) + ';'; } } catch (e) {}
  const values = [...document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=hidden]), textarea, output, progress, meter')].slice(0, 60).map(e => String(e.value)).join('\u0001');
  const cur = document.querySelector('[data-uic-cur]'), grp = cur ? (cur.parentElement || cur) : null; let cls = 0, cn = 0;
  for (const e of document.querySelectorAll('body *')) { if (cn++ > 5000) break; if (grp && grp.contains(e)) continue; const t = (typeof e.className === 'string' ? e.className : '') + (e.getAttribute('aria-expanded') || '') + (e.getAttribute('aria-hidden') || '') + (e.hidden ? 'h' : '') + (e.getAttribute('style') || '').length; for (let i = 0; i < t.length; i++) cls = (cls * 31 + t.charCodeAt(i)) | 0; }
  const own = cur ? (cur.getAttribute('aria-pressed') || '') + (cur.getAttribute('aria-checked') || '') + (cur.getAttribute('aria-selected') || '') + (typeof cur.className === 'string' ? cur.className : '') : '';
  return {cls, own, values, root, store, printed: window.__uic_print || 0, anims: document.getAnimations ? document.getAnimations().filter(a => a.playState === 'running').length : 0, texts, lists, styles, hash: location.hash, path: location.pathname, y: Math.round(scrollY), dialogs: [...document.querySelectorAll('dialog[open], [role=dialog], [role=alertdialog]')].filter(vis).length,
          active: document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null, visible: document.querySelectorAll('body *').length}; }
"""

CONTROLS = r"""
() => { const vis = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect(); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05 && r.width > 0 && r.height > 0; };
  const seen = {}, out = []; let i = 0;
  for (const e of document.querySelectorAll('button, select, summary, input[type=checkbox], input[type=radio], input[type=submit], [role=button], [role=tab], [role=switch], a[href]')) { if (!vis(e) || e.disabled) continue;
    const href = e.tagName === 'A' ? e.getAttribute('href') : null; if (href && /^(https?:|mailto:|tel:)/.test(href)) continue;
    const label = (e.innerText || e.value || e.getAttribute('aria-label') || e.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    const on = e.getAttribute('aria-pressed') === 'true' || e.getAttribute('aria-selected') === 'true' || e.hasAttribute('aria-current') || (e.type === 'radio' && e.checked) || /(^|[\s_-])(active|selected|current|is-on)([\s_-]|$)/.test(e.className && e.className.toString ? e.className.toString() : '');
    const kind = e.tagName === 'SELECT' ? 'select' : e.tagName === 'A' ? 'link' : e.type === 'checkbox' || e.type === 'radio' ? e.type : e.tagName === 'SUMMARY' ? 'summary' : 'button';
    const key = kind + '|' + label + '|' + (href || '') + '|' + [...e.classList].sort().join('.'); if (kind === 'link' && href && href.startsWith('#') && seen[key]) continue; if (seen[key] >= 1 && kind !== 'select') { seen[key]++; continue; } seen[key] = 1;
    e.setAttribute('data-uic-w', i); const target = href && href.startsWith('#') && href.length > 1 ? document.getElementById(decodeURIComponent(href.slice(1))) : null;
    const th = target ? (target.matches('h1,h2,h3,h4') ? target : target.querySelector('h1,h2,h3,h4,legend,label')) : null;
    out.push({i: i++, kind, label, href, already_chosen: on, in_form: !!e.closest('form'), submit: (e.type === 'submit' || (e.tagName === 'BUTTON' && e.closest('form') && e.type !== 'button' && e.type !== 'reset')),
      target_exists: href && href.startsWith('#') && href.length > 1 ? !!target : null, target_heading: th ? (th.innerText || '').trim().slice(0, 50) : null, target_id: target ? target.id : null,
      options: kind === 'select' ? [...e.options].map(o => o.text.trim()).slice(0, 6) : null}); if (out.length >= 45) break; }
  return out; }
"""

FIT = r"""
(opts) => {
  // Fit and scrolling: does every control and text run stay inside its box, and does anything scroll that nobody asked to scroll.
  const de = document.documentElement, VW = de.clientWidth || innerWidth, VH = opts.vh || innerHeight, out = {};
  const cs = e => getComputedStyle(e), rc = e => e.getBoundingClientRect(), px = v => parseFloat(v) || 0, SVGNS = 'http://www.w3.org/2000/svg';
  const helper = e => { const s = cs(e); if (!/(absolute|fixed)/.test(s.position)) return false; const r = rc(e);    // text kept for screen readers only
    return ((r.width <= 2 || r.height <= 2) && s.overflow !== 'visible') || /inset\((50|100)%\)/.test(s.clipPath) || /rect\(0(px)?[, ]+0(px)?[, ]+0(px)?[, ]+0(px)?\)/.test(s.clip || ''); };
  const selfHidden = e => { const s = cs(e); return s.visibility === 'hidden' || s.visibility === 'collapse' || s.display === 'none' || px(s.opacity) <= 0.05 || helper(e); };
  const hc = new WeakMap(); const hidden = e => { if (!e || e.nodeType !== 1) return false; if (hc.has(e)) return hc.get(e); const h = selfHidden(e) || hidden(e.parentElement); hc.set(e, h); return h; };
  const vis = e => { if (e.checkVisibility && !e.checkVisibility()) return false; const r = rc(e); return r.width > 0 && r.height > 0 && !hidden(e); };
  const sel = el => { if (el === de) return 'html'; if (el === document.body) return 'body'; if (el.id) return '#' + el.id; let s = el.tagName.toLowerCase();
    if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.');
    let p = el.parentElement, hops = 0; while (p && !p.id && hops < 3) { p = p.parentElement; hops++; }
    if (p && p.id) s = '#' + p.id + ' ' + s; return s; };
  const txt = el => (el.innerText || el.value || el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
  const boxy = e => { const s = cs(e); const bg = s.backgroundColor;      // a box of its own: background, border, shadow, padding or clipping
    return (bg && bg !== 'transparent' && !/rgba\(\d+, \d+, \d+, 0\)/.test(bg)) || s.backgroundImage !== 'none' || s.boxShadow !== 'none' || s.overflowX !== 'visible' || s.overflowY !== 'visible' ||
      ['Top', 'Right', 'Bottom', 'Left'].some(k => (px(s['border' + k + 'Width']) > 0 && s['border' + k + 'Style'] !== 'none') || px(s['padding' + k]) > 0); };
  const all = [...document.querySelectorAll('body *')].filter(e => e.namespaceURI !== SVGNS && !/^(SCRIPT|STYLE|BR|COL|COLGROUP|OPTION|OPTGROUP|TEMPLATE|NOSCRIPT)$/.test(e.tagName));

  // ---- where vertical scrolling was asked for (style sheets and inline styles)
  const asked = new Map(); let unread = 0;
  const yOf = st => { const o = st.overflow || ''; if (/var\(/.test(o) || /var\(/.test(st.overflowY || '')) return 'auto'; return st.overflowY || st.overflowBlock || ''; };
  const walk = rules => { for (const r of rules) { if (r.cssRules && r.cssRules.length) { try { walk(r.cssRules); } catch (e) {} }
      if (!r.style || !r.selectorText) continue; const v = yOf(r.style); if (!v) continue; let m = []; try { m = document.querySelectorAll(r.selectorText); } catch (e) { continue; }
      for (const el of m) { if (!asked.has(el)) asked.set(el, []); asked.get(el).push(v); } } };
  for (const ss of document.styleSheets) { try { walk(ss.cssRules); } catch (e) { unread++; } }
  const askedY = e => { if (unread) return true; const a = (asked.get(e) || []).slice(); const v = e.style ? yOf(e.style) : ''; if (v) a.push(v); return a.some(x => /(auto|scroll|overlay)/.test(x)); };
  const NATIVE = e => /^(TEXTAREA|SELECT|INPUT|IFRAME|DIALOG|OBJECT|EMBED)$/.test(e.tagName) || e.hasAttribute('popover');
  const OVERLAY = e => !!e.closest('dialog, [role=dialog], [role=alertdialog], [role=listbox], [role=menu], [role=combobox], [role=tooltip], [popover]');
  const overY = e => e.scrollHeight - e.clientHeight, overX = e => e.scrollWidth - e.clientWidth;
  const scrollsY = e => /(auto|scroll)/.test(cs(e).overflowY) && overY(e) > 2, scrollsX = e => /(auto|scroll)/.test(cs(e).overflowX) && overX(e) > 2;
  const pageScrolls = de.scrollHeight > VH + 2 && !/(hidden|clip)/.test(cs(de).overflowY) && !/(hidden|clip)/.test(cs(document.body).overflowY);
  const pinned = e => { for (let a = e; a && a !== document.body; a = a.parentElement) if (/(fixed|sticky)/.test(cs(a).position)) return a; return null; };

  // ---- scroll areas stretched by elements nobody can see: hide those elements for a moment and see what shrinks
  const boxes = all.filter(e => { if (NATIVE(e)) return false; const s = cs(e); return /(auto|scroll|hidden)/.test(s.overflowY) && overY(e) > 8 && vis(e); });
  const ghosts = all.filter(e => { const s = cs(e); return s.display !== 'none' && (helper(e) || (/(absolute|fixed)/.test(s.position) && (s.visibility === 'hidden' || px(s.opacity) <= 0.05))); });
  const before = boxes.map(e => e.scrollHeight), pageBefore = de.scrollHeight; const stray = new Map(); let pageStray = 0;
  if (ghosts.length && (boxes.length || pageScrolls)) { const keep = ghosts.map(g => [g.style.getPropertyValue('display'), g.style.getPropertyPriority('display')]);
    ghosts.forEach(g => g.style.setProperty('display', 'none', 'important'));
    boxes.forEach((e, i) => { const d = before[i] - e.scrollHeight; if (d > 8) stray.set(e, d); }); pageStray = pageBefore - de.scrollHeight;
    ghosts.forEach((g, i) => { if (keep[i][0]) g.style.setProperty('display', keep[i][0], keep[i][1]); else g.style.removeProperty('display'); }); }
  const culprits = (box, limit) => { const top0 = box === de ? -scrollY : rc(box).top + px(cs(box).borderTopWidth) - box.scrollTop, lim = box === de ? VH : box.clientHeight, n = {};
    for (const g of ghosts) { if (box !== de && !box.contains(g)) continue; if (rc(g).bottom - top0 > lim + 1) { const k = sel(g); n[k] = (n[k] || 0) + 1; } }
    return Object.entries(n).sort((a, b) => b[1] - a[1]).slice(0, limit).map(([k, v]) => v > 1 ? `${k} x${v}` : k); };
  const describe = e => { const s = cs(e), share = Math.round(100 * e.clientHeight / VH), pin = /(fixed|sticky)/.test(s.position);
    return {sel: sel(e), position: s.position, overflow: `${s.overflowX} ${s.overflowY}`, client_height: e.clientHeight, scroll_height: e.scrollHeight, extra_px: overY(e), share_of_screen_height_pct: share,
      panel: pin ? 'fixed or sticky panel' : share >= 60 ? 'page-level panel' : 'smaller box'}; };
  out['scroll-unexpected'] = [];
  for (const e of all) { if (NATIVE(e) || !vis(e)) continue; const s = cs(e); const st = stray.get(e);
    if (scrollsY(e) && !askedY(e)) { const d = describe(e); d.why = 'scrolls vertically although no rule asks it to: overflow-y became auto because only overflow-x was set'; d.stretched_by_unseen_elements = st ? culprits(e, 4) : [];
      if (!st) { const top0 = rc(e).top + px(s.borderTopWidth) - e.scrollTop; d.content_past_the_edge = [...e.querySelectorAll('*')].filter(k => vis(k) && rc(k).bottom - top0 > e.clientHeight + 1 && ![...k.children].some(c => vis(c) && rc(c).bottom - top0 > e.clientHeight + 1)).slice(0, 3).map(sel); }
      out['scroll-unexpected'].push(d); }
    else if (st) { const d = describe(e); d.stray_px = st; d.stretched_by_unseen_elements = culprits(e, 4);
      d.why = /hidden/.test(s.overflowY) ? 'no scrollbar, yet the box can still be scrolled: hidden elements stretch it, and it jumps when one of them takes focus' : 'scrolls into empty space: hidden elements stretch the scroll area';
      out['scroll-unexpected'].push(d); } }
  if (pageStray > 8 && pageScrolls) out['scroll-unexpected'].push({sel: 'page', why: 'the page scrolls past its content: hidden elements stretch it', stray_px: pageStray, scroll_height: pageBefore, stretched_by_unseen_elements: culprits(de, 4), panel: 'page'});
  out['scroll-unexpected'] = out['scroll-unexpected'].slice(0, 8);

  // ---- a scroll area inside another one that scrolls the same way
  out['scroll-nested'] = [];
  for (const e of all) { if (NATIVE(e) || !vis(e) || OVERLAY(e)) continue;
    if (scrollsY(e)) { let a = e.parentElement; while (a && a !== document.body && !(scrollsY(a) && !NATIVE(a))) a = a.parentElement; const outer = a && a !== document.body ? sel(a) : (pageScrolls && !pinned(e) ? 'the page' : null);
      if (outer) out['scroll-nested'].push({inner: sel(e), outer, direction: 'vertical', inner_height: e.clientHeight, share_of_screen_height_pct: Math.round(100 * e.clientHeight / VH), holds_table: !!e.querySelector('table')}); }
    if (scrollsX(e)) { let a = e.parentElement; while (a && a !== document.body && !(scrollsX(a) && !NATIVE(a))) a = a.parentElement; if (a && a !== document.body) out['scroll-nested'].push({inner: sel(e), outer: sel(a), direction: 'sideways', inner_width: e.clientWidth}); } }
  out['scroll-nested'] = out['scroll-nested'].slice(0, 8);

  // ---- controls, control groups and text runs against the box they sit in
  const INTER = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [role=tab], [role=checkbox], [role=radio], [role=switch], [role=menuitem], [role=option]';
  const controls = all.filter(e => e.matches(INTER) && vis(e) && !e.closest('[aria-hidden="true"]')); const cset = new Set(controls);
  const face = k => cset.has(k) ? k : (k.children.length === 1 && cset.has(k.firstElementChild) ? k.firstElementChild : null);
  const groups = all.filter(e => { if (cset.has(e) || !vis(e) || e.closest(INTER)) return false; const k = [...e.children].filter(vis); if (k.length < 2 || k.length > 8) return false; const f = k.map(face); if (f.some(x => !x)) return false; const t = rc(f[0]).top; return f.every(x => Math.abs(rc(x).top - t) < 6); });
  const subjects = [];
  for (const e of controls) if (!(e.parentElement && e.parentElement.closest(INTER))) subjects.push({e, kind: 'control', r: rc(e), from: e.parentElement});
  for (const e of groups) if (boxy(e)) subjects.push({e, kind: 'group', r: rc(e), from: e.parentElement});
  for (const e of all) { if (cset.has(e) || e.closest(INTER) || !vis(e) || e.closest('[aria-hidden="true"]')) continue; const tn = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()); if (!tn.length) continue; const s = cs(e);
    if (s.textOverflow === 'ellipsis' || (s.webkitLineClamp && s.webkitLineClamp !== 'none')) continue;
    const ownBox = s.backgroundImage !== 'none' || px(s.borderTopWidth) > 0 || s.boxShadow !== 'none' || !/rgba\(\d+, \d+, \d+, 0\)|transparent/.test(s.backgroundColor);
    if (ownBox && s.overflowX === 'visible' && s.display !== 'inline') continue;                       // text against its own box is text-spill
    const rg = document.createRange(); rg.setStartBefore(tn[0]); rg.setEndAfter(tn[tn.length - 1]); const r = rg.getBoundingClientRect(); if (r.width > 1 && r.height > 1) subjects.push({e, kind: 'text', r, from: e.parentElement}); }
  const edge = a => { const q = cs(a), ar = rc(a); const pad = {l: ar.left + px(q.borderLeftWidth), r: ar.right - px(q.borderRightWidth), t: ar.top + px(q.borderTopWidth), b: ar.bottom - px(q.borderBottomWidth)};
    return {pad, con: {l: pad.l + px(q.paddingLeft), r: pad.r - px(q.paddingRight)}, q}; };
  const shifted = (e, box) => { for (let p = e; p && p !== box; p = p.parentElement) { const s = cs(p);      // placed on purpose: out of the flow, pulled by a negative margin, moved or turned
      if (/(absolute|fixed|sticky)/.test(s.position) || s.float !== 'none' || s.transform !== 'none' || (s.translate && s.translate !== 'none') || px(s.marginLeft) < 0 || px(s.marginRight) < 0 || (s.position === 'relative' && (px(s.left) || px(s.right)))) return true; } return false; };
  const over = [], cut = []; const records = []; const seenKey = {};
  for (const {e, kind, r, from} of subjects) { let a = from; while (a && a !== document.body && a !== de && !boxy(a)) a = a.parentElement; if (!a || a === document.body || a === de) continue;
    if (hidden(a)) continue;
    const g = edge(a), sideScroll = /(auto|scroll)/.test(g.q.overflowX), moved = shifted(e, a);
    const ox = Math.max(r.right - g.con.r, g.con.l - r.left), lim = kind === 'text' ? 3 : 1;
    const oy = (kind === 'text' || cs(e).display === 'inline' || /(auto|scroll)/.test(g.q.overflowY)) ? 0 : Math.max(r.bottom - g.pad.b, g.pad.t - r.top);
    // the nearest edge that clips sideways, from the box upwards
    let clipR = Infinity, clipL = -Infinity, clipper = null; for (let p = a; p && p !== de; p = p.parentElement) { const q = cs(p); if (/(auto|scroll)/.test(q.overflowX) && p !== a && overX(p) > 2) break; if (/(hidden|clip)/.test(q.overflowX)) { const pr = rc(p); const R = pr.right - px(q.borderRightWidth), L = pr.left + px(q.borderLeftWidth); if (R < clipR) { clipR = R; clipper = p; } if (L > clipL) clipL = L; } }
    const cutPx = Math.max(r.right - clipR, clipL - r.left, 0), hiddenPct = r.width ? Math.round(100 * Math.min(1, cutPx / r.width)) : 0;
    if (kind !== 'text') { const label = txt(e) || e.getAttribute('name') || e.getAttribute('placeholder') || e.tagName.toLowerCase(), base = kind + '|' + label; seenKey[base] = (seenKey[base] || 0) + 1; const s = cs(e);
      if (records.length < 300) records.push({key: base + '|' + seenKey[base], sel: sel(e), box: sel(a), past_box_px: Math.round(Math.max(ox, oy)), cut_px: Math.round(cutPx), weight: s.fontWeight, size: s.fontSize, padding: s.padding, w: Math.round(r.width), h: Math.round(r.height)}); }
    if (moved || sideScroll) { if (!(oy > 1 && !moved)) continue; }
    const overX1 = !moved && !sideScroll && ox > lim && r.right <= VW + 1 && r.left >= -1;      // what leaves the screen is page-overflow or content-cut-off already
    if (overX1 && cutPx > 1 && hiddenPct < 97 && r.right <= VW + 4) { const sib = clipper ? [...(e.parentElement ? e.parentElement.children : [])].filter(k => k.tagName === e.tagName && vis(k)).length : 0;
      cut.push({sel: sel(e), text: txt(e), cut_px: Math.round(cutPx), hidden_pct: hiddenPct, interactive: kind !== 'text', cut_by: sel(clipper), where: 'inside the screen, at the edge of a box that clips', ...(sib >= 4 ? {note: 'one of a row of similar items: check whether buttons or dragging move the row'} : {})}); }
    else if (overX1 || oy > 1) { const past = Math.round(Math.max(r.right - g.pad.r, g.pad.l - r.left));
      over.push({sel: sel(e), kind, text: txt(e), box: sel(a), over_px: Math.round(overX1 ? ox : oy), direction: overX1 ? 'sideways' : 'up or down', reaches: overX1 ? (past > 1 ? 'outside the box by ' + past + 'px' : 'into the padding of the box') : 'outside the box', box_width: Math.round(g.con.r - g.con.l), own_width: Math.round(r.width)}); } }
  const rank = x => (x.kind === 'text' ? 0 : 1000) + x.over_px; over.sort((x, y) => rank(y) - rank(x)); out['control-overflow'] = over.slice(0, 12);
  cut.sort((x, y) => (y.interactive - x.interactive) || (y.hidden_pct - x.hidden_pct)); out._cut_inside = cut.slice(0, 8);

  // ---- records for the regression pass, the close-up crops and the end-of-scroll screenshots
  const page = r => ({x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height)});
  const scroll = [{key: 'page', sel: 'page', scroll_height: de.scrollHeight, client_height: VH, real: pageScrolls}]; const sk = {}; let si = 0; const ends = [];
  for (const e of all) { if (NATIVE(e) || !vis(e)) continue; const s = cs(e); const y = s.overflowY; if (!(/(auto|scroll)/.test(y) || (/hidden/.test(y) && (/(fixed|sticky)/.test(s.position) || e.clientHeight >= 0.6 * VH)))) continue;
    const k = sel(e); sk[k] = (sk[k] || 0) + 1; const real = scrollsY(e); if (scroll.length < 60) scroll.push({key: k + (sk[k] > 1 ? '#' + sk[k] : ''), sel: k, scroll_height: e.scrollHeight, client_height: e.clientHeight, real});
    if (real && e.clientHeight >= 160 && ends.length < 4 && !OVERLAY(e)) { e.setAttribute('data-uic-s', si); ends.push({i: si++, sel: k}); } }
  const crop = []; const add = (kind, e, r) => { if (r.width < 24 || r.height < 12 || crop.length >= 22) return; if (crop.some(c => Math.abs(c.x - (r.left + scrollX)) < 6 && Math.abs(c.y - (r.top + scrollY)) < 6 && Math.abs(c.w - r.width) < 12)) return; crop.push({kind, sel: sel(e), ...page(r)}); };
  for (const e of groups) add('controls', e, rc(e));
  for (const f of all.filter(e => e.matches('input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=submit]):not([type=button]), select, textarea') && vis(e))) { const lab = f.id ? document.querySelector('label[for="' + CSS.escape(f.id) + '"]') : null; const wrap = f.closest('label');
    let r = rc(f); if (wrap && vis(wrap)) r = rc(wrap); else if (lab && vis(lab)) { const a = rc(lab), b = rc(f); r = {left: Math.min(a.left, b.left), top: Math.min(a.top, b.top), width: Math.max(a.right, b.right) - Math.min(a.left, b.left), height: Math.max(a.bottom, b.bottom) - Math.min(a.top, b.top)}; }
    if (r.width <= 760 && r.height <= 260) add('form row', f, r); }
  const panels = []; for (const e of all) { if (panels.length >= 5 || !vis(e) || NATIVE(e)) continue; const s = cs(e), r = rc(e); if (r.width < 160 || r.height < 120 || r.width >= VW - 2 && !/(fixed|sticky)/.test(s.position)) continue;
    if (!(/(fixed|sticky)/.test(s.position) || /(hidden|clip|auto|scroll)/.test(s.overflowX))) continue; if (!e.querySelector(INTER)) continue; if (panels.some(p => p.el.contains(e))) continue; panels.push({el: e, sel: sel(e), ...page(r)}); }
  const sb = document.createElement('div'); sb.style.cssText = 'position:absolute;top:-9999px;left:-9999px;width:100px;height:100px;overflow:scroll'; document.body.appendChild(sb); const sbw = sb.offsetWidth - sb.clientWidth; sb.remove();
  out._fit = {controls: records, scrollers: scroll, ends, crops: crop, panels: panels.map(p => ({sel: p.sel, x: p.x, y: p.y, w: p.w, h: p.h})),
    env: {scrollbar_px: sbw, page_scrolls: pageScrolls, app_shell: !pageScrolls && scroll.some(s => s.real && s.key !== 'page'), style_sheets_not_readable: unread}};
  return out;
}
"""

STICKY = r"""
() => { // a header declared sticky that scrolls away all the same: move to the lower rows and look
  const cs = e => getComputedStyle(e), rc = e => e.getBoundingClientRect(), found = []; const y0 = scrollY;
  const sel = el => { if (el.id) return '#' + el.id; let s = el.tagName.toLowerCase(); if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.'); let p = el.parentElement, hops = 0; while (p && !p.id && hops < 3) { p = p.parentElement; hops++; } if (p && p.id) s = '#' + p.id + ' ' + s; return s; };
  for (const tb of document.querySelectorAll('table')) { const rows = [...tb.querySelectorAll('tbody tr')]; if (rows.length <= 15 || cs(rows[0]).display !== 'table-row' || !rc(tb).height) continue;
    const hd = tb.tHead || tb.querySelector('tr'); if (!hd) continue; const cell = hd.querySelector('th, td') || hd; if (![hd, ...hd.querySelectorAll('th, td, tr')].some(e => cs(e).position === 'sticky')) continue;
    let sc = tb.parentElement, blocker = null; while (sc && sc !== document.body) { const s = cs(sc); if (/(auto|scroll)/.test(s.overflowY) && sc.scrollHeight > sc.clientHeight + 2) break; if (!blocker && (/(auto|scroll|hidden)/.test(s.overflowX) || /(auto|scroll|hidden)/.test(s.overflowY))) blocker = sc; sc = sc.parentElement; }
    const inner = sc && sc !== document.body ? sc : null, row = rows[rows.length - 2], keep = inner ? inner.scrollTop : 0;
    if (inner) { inner.scrollIntoView({block: 'start'}); inner.scrollTop += rc(row).top - (rc(inner).top + inner.clientHeight / 2); } else scrollTo(0, rc(row).top + scrollY - innerHeight / 2);
    const portTop = inner ? Math.max(0, rc(inner).top) : 0, portBottom = inner ? Math.min(innerHeight, rc(inner).bottom) : innerHeight, rr = rc(row), hr = rc(cell);
    if (rr.top >= portTop - 1 && rr.top < portBottom && hr.bottom <= portTop + 1) found.push({table: sel(tb), body_rows: rows.length, issue: 'the header is declared sticky but scrolls away', stopped_by: blocker ? sel(blocker) + ' (overflow is set on it, so the header sticks to that box and not to what scrolls)' : 'unknown'});
    if (inner) inner.scrollTop = keep; scrollTo(0, y0); }
  scrollTo(0, y0); return found; }
"""


def uri(page):
    if re.match(r'^https?://', page):
        return page
    p = pathlib.Path(page.split('?')[0]).resolve()
    if not p.exists():
        sys.exit(f'uicheck: file not found: {page}')
    return p.as_uri() + ('?' + page.split('?', 1)[1] if '?' in page else '')


def sample_contrast(pg, r):
    """Text over an image or gradient: hide the text, photograph what is behind it, report the worst and the typical ratio."""
    items = r.pop('_sample', [])
    if not items:
        return
    if Image is None:
        r['contrast-unmeasured'] = [{'count': len(items), 'reason': 'text over an image or gradient; install Pillow to measure', 'examples': [i['sel'] for i in items[:4]]}]
        return
    def L(c):
        f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
    for it in items[:24]:
        try:
            loc = pg.locator(f'[data-uic-s="{it["i"]}"]')
            loc.scroll_into_view_if_needed(timeout=1500)
            box = loc.bounding_box()
            if not box or box['width'] < 2 or box['height'] < 2:
                continue
            tag = pg.add_style_tag(content=f'[data-uic-s="{it["i"]}"]{{color:transparent!important;-webkit-text-fill-color:transparent!important;fill:transparent!important;text-shadow:none!important}}')
            vw = pg.viewport_size
            clip = {'x': max(0, box['x']), 'y': max(0, box['y']), 'width': min(box['width'], vw['width'] - max(0, box['x'])), 'height': min(box['height'], vw['height'] - max(0, box['y']))}
            if clip['width'] < 2 or clip['height'] < 2:
                tag.evaluate('e => e.remove()'); continue
            img = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); tag.evaluate('e => e.remove()')
            img.thumbnail((120, 120)); raw = img.tobytes(); px = [raw[i:i + 3] for i in range(0, len(raw), 3)]; fg = it['fg']
            rs = []
            for p in px:
                f = tuple(fg[k] * fg['a'] + p[i] * (1 - fg['a']) for i, k in enumerate('rgb'))
                a, b = L(f), L(p); rs.append((max(a, b) + 0.05) / (min(a, b) + 0.05))
            rs.sort(); worst = rs[int(len(rs) * 0.05)]; typical = rs[len(rs) // 2]
            if worst < it['need']:
                r['contrast-text'].append({'sel': it['sel'], 'ratio': round(worst, 2), 'typical_ratio': round(typical, 2), 'need': it['need'], 'px': it['px'], 'role': it['role'], 'text': it['text'], 'measured': 'pixels behind the text (image or gradient)'})
        except Exception as e:
            r.setdefault('_errors', []).append('contrast sample: ' + str(e)[:80])
    pg.evaluate('window.scrollTo(0,0)')


def confirm_listeners(pg, cdp, r):
    """Elements with a pointer cursor that the keyboard cannot reach: confirm a click listener through the debugger."""
    out = []
    for it in r.pop('_pointer', []):
        has = it['onclick_attribute']
        if not has:
            try:
                o = cdp.send('Runtime.evaluate', {'expression': f'document.querySelector(\'[data-uic-k="{it["i"]}"]\')'})
                ls = cdp.send('DOMDebugger.getEventListeners', {'objectId': o['result']['objectId']})
                has = any(l['type'] in ('click', 'mousedown', 'mouseup', 'pointerdown', 'pointerup', 'touchstart', 'touchend') for l in ls.get('listeners', []))
                it['listener'] = 'confirmed' if has else 'none on the element (a framework may listen higher up: check the code)'
            except Exception:
                it['listener'] = 'could not be read'
        else:
            it['listener'] = 'onclick attribute'
        it.pop('i'); it.pop('onclick_attribute')
        out.append(it)
    r['keyboard-unreachable'] = out


def focus_check(pg):
    """Every focusable element (up to 60, at least one of each look): does anything visible change on keyboard focus, and how strongly?"""
    total = pg.evaluate(r"""() => { const all = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [tabindex]:not([tabindex="-1"])')]
        .filter(e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.disabled; });
      const sig = e => e.tagName + '.' + [...e.classList].sort().join('.'); const seen = {}; const pick = [];
      for (const e of all) { const k = sig(e); seen[k] = (seen[k] || 0) + 1; if (seen[k] <= 2) pick.push(e); }
      for (const e of all) { if (pick.length >= 60) break; if (!pick.includes(e)) pick.push(e); }
      pick.slice(0, 60).forEach((e, i) => e.setAttribute('data-uichk', i)); return {total: all.length, tested: Math.min(60, pick.length), looks: Object.keys(seen).length}; }""")
    missing, weak, errors = [], [], 0
    for i in range(total['tested']):
        try:
            loc = pg.locator(f'[data-uichk="{i}"]'); loc.scroll_into_view_if_needed(timeout=1500); pg.mouse.move(0, 0); pg.wait_for_timeout(30)
            pg.evaluate(f'''(() => {{ const e = document.querySelector('[data-uichk="{i}"]'); const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
                const hid = r.width * r.height < 16 || parseFloat(s.opacity) < 0.05 || (s.clip !== 'auto' && s.clip !== ''); let t = null;
                if (hid) t = e.closest('label') || (e.id && document.querySelector('label[for="' + e.id + '"]')) || e.parentElement;
                document.querySelectorAll('[data-uichk-box]').forEach(x => x.removeAttribute('data-uichk-box')); (t || e).setAttribute('data-uichk-box', '1'); }})()''')
            box = pg.locator('[data-uichk-box="1"]').bounding_box()
            if not box:
                continue
            vw = pg.viewport_size
            clip = {'x': max(0, box['x'] - 8), 'y': max(0, box['y'] - 8)}
            clip['width'] = min(vw['width'] - clip['x'], box['width'] + 16); clip['height'] = min(vw['height'] - clip['y'], box['height'] + 16)
            if clip['width'] <= 0 or clip['height'] <= 0:
                continue
            a = pg.screenshot(clip=clip); r0 = loc.bounding_box()
            pg.evaluate(f'document.querySelector(\'[data-uichk="{i}"]\').focus({{focusVisible: true}})'); pg.wait_for_timeout(120)
            b = pg.screenshot(clip=clip); r1 = loc.bounding_box()
            if r0 and r1 and (abs(r0['x'] - r1['x']) > 4 or abs(r0['y'] - r1['y']) > 4):
                continue      # it moves into view when focused (a skip link): that is its visible focus change
            name = pg.evaluate(f'''(() => {{ const e = document.querySelector('[data-uichk="{i}"]'); return (e.id ? '#' + e.id : e.tagName.toLowerCase() + (e.classList.length ? '.' + [...e.classList].slice(0,2).join('.') : '')) + ' "' + (e.innerText || e.getAttribute('aria-label') || e.getAttribute('placeholder') || '').trim().slice(0,30) + '"'; }})()''')
            if a == b:
                missing.append(name)
            elif Image is not None:
                ia, ib = Image.open(io.BytesIO(a)).convert('RGB'), Image.open(io.BytesIO(b)).convert('RGB')
                if ia.size == ib.size:
                    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4
                    lum = lambda c: 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
                    best, n = 1.0, 0
                    ra, rb = ia.tobytes(), ib.tobytes()
                    for k in range(0, len(ra), 3):
                        p, q = ra[k:k + 3], rb[k:k + 3]
                        if p != q:
                            n += 1; l1, l2 = lum(p), lum(q); best = max(best, (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05))
                    if best < 3:
                        weak.append({'element': name, 'strongest_change_ratio': round(best, 2), 'changed_pixels': n})
            pg.evaluate('document.activeElement && document.activeElement.blur()')
        except Exception:
            errors += 1
    return {'focus-missing': missing, 'focus-weak': weak, '_focus': {'focusable': total['total'], 'tested': total['tested'], 'distinct_looks': total['looks'], 'errors': errors}}


def tab_walk(pg):
    """Press Tab through the page: order, stops that cannot be seen, loops."""
    seq, jumps, unseen = [], [], []
    n = min(pg.evaluate("document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [tabindex]:not([tabindex=\"-1\"])').length") + 3, 90)
    pg.evaluate("document.activeElement && document.activeElement.blur(); window.scrollTo(0,0); document.body.setAttribute('tabindex','-1'); document.body.focus(); document.body.removeAttribute('tabindex')")
    prev = None; repeats = 0; blanks = 0; parts_seen = 0
    for _ in range(n):
        pg.keyboard.press('Tab')
        cur = pg.evaluate(r"""() => { const e = document.activeElement; if (!e || e === document.body) return null; const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
            return {key: (e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + [...e.classList].join('.')) + '|' + (e.innerText || e.value || e.getAttribute('aria-label') || '').trim().slice(0, 24), y: Math.round(r.top + scrollY + (() => { let t = 0; for (let a = e.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) t += a.scrollTop || 0; return t; })()), x: Math.round(r.left),
                    parts: /^(date|time|datetime-local|month|week)$/.test(e.type || ''), pinned: (() => { for (let a = e; a && a !== document.body; a = a.parentElement) if (/(fixed|sticky)/.test(getComputedStyle(a).position)) return true; return false; })(),
                    scroller: (() => { for (let a = e.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) { if (/(auto|scroll)/.test(getComputedStyle(a).overflowY) && a.scrollHeight > a.clientHeight + 4) return a.tagName + '.' + a.className + '#' + a.id; } return ''; })(), seen: r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0.05}; }""")
        if cur is None:
            blanks += 1
            if seq or blanks > 2:
                break
            continue
        if prev and cur['key'] == prev['key'] and cur['y'] == prev['y'] and cur['x'] == prev['x']:
            if cur.get('parts') and parts_seen < 6:      # day, month, year and so on are separate stops inside one field
                parts_seen += 1; continue
            repeats += 1
            if repeats >= 2:
                break
        else:
            repeats = 0; parts_seen = 0
        if seq and cur['key'] == seq[0]['key'] and cur['y'] == seq[0]['y'] and cur['x'] == seq[0]['x'] and len(seq) > 1:
            break
        if not cur['seen']:
            unseen.append(cur['key'])
        if prev and cur['y'] < prev['y'] - 120 and not cur.get('pinned') and not prev.get('pinned') and cur.get('scroller') == prev.get('scroller'):      # same scrolling area, lower stop first
            jumps.append({'from': prev['key'], 'to': cur['key'], 'up_px': prev['y'] - cur['y']})
        seq.append(cur); prev = cur
    return {'stops': len(seq), 'order': [s['key'] for s in seq][:60], 'backward_jumps': jumps[:8], 'stops_not_visible': unseen[:8], 'stuck_on': prev['key'] if repeats >= 2 else None}


def click_census(ctx, url, quiet_wait=350):
    """Operate each distinct control once on a fresh copy of the page and record what changed."""
    res = []
    pg = ctx.new_page(); dialogs, downloads, requests = [], [], []
    pg.add_init_script("window.print = () => { window.__uic_print = (window.__uic_print || 0) + 1; };")
    pg.on('dialog', lambda d: (dialogs.append({'type': d.type, 'message': d.message[:80]}), d.accept()))
    pg.on('download', lambda d: downloads.append(d.suggested_filename))
    pg.on('request', lambda q: requests.append(q.method + ' ' + q.url[:60]) if q.method != 'GET' or q.resource_type in ('fetch', 'xhr') else None)
    def load():
        pg.goto(url); pg.wait_for_timeout(250)
        return pg.evaluate(CONTROLS)
    try:
        controls = load()
        saved = pg.evaluate("() => { try { const o = {}; for (let i = 0; i < localStorage.length; i++) o[localStorage.key(i)] = localStorage.getItem(localStorage.key(i)); return o; } catch (e) { return null; } }")
        if saved is not None:      # put the page's stored data back before every later load, so one control's effect does not hide the next control
            pg.add_init_script("try { if (window === window.top) { localStorage.clear(); const s = " + json.dumps(saved) + "; for (const k in s) localStorage.setItem(k, s[k]); sessionStorage.clear(); } } catch (e) {}")
    except Exception as e:
        pg.close(); return [{'error': str(e)[:100]}]
    DESTRUCT = re.compile(r'\b(delete|remove|clear|reset|discard|erase|empty)\b', re.I)
    NOT_YET = re.compile(r"\b(will|would|can|could|cannot|can't|not|before|if|unable|failed?|error|needs?|must|should|to be|required)\b|n't\b", re.I)
    SUCCESS = re.compile(r'\b(downloaded|sent|saved|copied|subscribed|submitted|received|success|thank you|thanks|done|added|updated|exported)\b', re.I)
    def diff(a, b, chosen=None):
        ch = [(k, a['texts'].get(k), v) for k, v in b['texts'].items() if a['texts'].get(k) != v]
        added = [v for k, o, v in ch if o is None]; changed = [(o, v) for k, o, v in ch if o is not None]; removed = [v for k, v in a['texts'].items() if k not in b['texts']]
        def keyed(ls):
            seen = {}; out = {}
            for x in ls:
                seen[x['k']] = seen.get(x['k'], 0) + 1; out[(x['k'], seen[x['k']])] = x
            return out
        ka, kb = keyed(a['lists']), keyed(b['lists'])
        lists = [{'list': k[0][:40], 'before': x['n'], 'after': kb[k]['n'], 'shown': kb[k].get('s', True), 'new_words': sorted(set(kb[k].get('w', [])) - set(x.get('w', [])))[:6]} for k, x in ka.items() if k in kb and x['n'] != kb[k]['n']]
        d = {'text_changed': len(changed), 'text_added': len(added), 'text_removed': len(removed), 'examples': ([f'{o} -> {v}'[:70] for o, v in changed[:3]] + ['+ ' + v[:60] for v in added[:3]])[:4],
             'lists_changed': lists[:4], 'hash': b['hash'] if b['hash'] != a['hash'] else None, 'scrolled': abs(b['y'] - a['y']) > 40, 'dialog_opened': b['dialogs'] > a['dialogs'], 'field_styles_changed': a['styles'] != b['styles'], 'focus_moved_to': b['active'] if b['active'] != a['active'] else None}
        d['nothing_changed'] = not (changed or added or removed or lists or d['hash'] or d['scrolled'] or d['dialog_opened'] or d['field_styles_changed'] or b['path'] != a['path']
                                    or b.get('cls') != a.get('cls') or b.get('values') != a.get('values') or b.get('root') != a.get('root') or b.get('store') != a.get('store') or b.get('printed') != a.get('printed') or b.get('anims', 0) > a.get('anims', 0))
        d['stored_data_changed'] = b.get('store') != a.get('store'); d['own_state_changed'] = b.get('own') != a.get('own')
        if chosen and (changed or added) and not lists:
            words = [w for w in re.findall(r'[A-Za-z0-9]+', chosen.lower()) if len(w) > 1]
            echo = [v for o, v in changed] + added
            d['only_echoes_the_choice'] = bool(words) and all(any(w in v.lower() for w in words) for v in echo)
        emptied = [l for l in lists if l['after'] == 0 and l['before'] > 0]
        if emptied:      # a list or table body went to zero rows and the block around it gained no new word; a block that was hidden and replaced by a sentence elsewhere is an empty state, not a finding
            sentence = any(len(v.split()) >= 3 for v in added)
            d['list_emptied_without_message'] = any(not l['new_words'] and (l['shown'] or not sentence) for l in emptied)
        msg = [v for v in added if SUCCESS.search(v) and '?' not in v and not NOT_YET.search(v)]
        d['asks_first'] = any('?' in v for v in added)
        if msg:
            d['claims_success'] = msg[0][:70]
        return d
    for c in controls:
        try:
            if res:
                load()
            dialogs.clear(); downloads.clear(); requests.clear()
            loc = pg.locator(f'[data-uic-w="{c["i"]}"]')
            rec = {'control': c['label'] or '(no label)', 'kind': c['kind']}
            if c['kind'] == 'link':
                if c['href'] and c['href'].startswith('#'):
                    if len(c['href']) == 1:
                        rec['effect'] = 'href="#" (inert)'; res.append(rec); continue
                    if not c['target_exists']:
                        rec['effect'] = f'target {c["href"]} does not exist'; rec['broken_anchor'] = True; res.append(rec); continue
                    rec['goes_to'] = c['href']; rec['target_heading'] = c['target_heading']
                    lw = set(re.findall(r'[a-z]{3,}', c['label'].lower())); tw = set(re.findall(r'[a-z]{3,}', ((c['target_heading'] or '') + ' ' + (c['target_id'] or '')).lower()))
                    if lw and tw and not (lw & tw) and not any(a[:4] == b[:4] for a in lw for b in tw) and not re.search(r'\b(skip|top|back|menu|close|more|next|previous)\b', c['label'].lower()) and (c['target_id'] or '').lower() not in ('top', 'main', 'content', 'home', 'start', 'page'):
                        rec['label_and_destination_share_no_word'] = True
                    res.append(rec); continue
                target = c['href'].split('#')[0].split('?')[0] if c['href'] else ''
                if target and url.startswith('file:'):
                    p = pathlib.Path(pathlib.PurePosixPath(re.sub(r'^file://', '', url.split('?')[0])).parent) / target
                    rec['goes_to'] = c['href']; rec['file_exists'] = p.exists()
                    if not p.exists(): rec['broken_link'] = True
                else:
                    rec['goes_to'] = c['href']
                res.append(rec); continue
            if DESTRUCT.search(c['label']):
                pg.evaluate("() => [...document.querySelectorAll('input[type=checkbox]')].filter(e => e.offsetParent && !e.checked).slice(0, 3).forEach(e => e.click())"); pg.wait_for_timeout(120)
            pg.evaluate("document.querySelectorAll('[data-uic-cur]').forEach(e => e.removeAttribute('data-uic-cur'))"); loc.evaluate("e => e.setAttribute('data-uic-cur', '1')")
            before = pg.evaluate(SNAP)
            if c['kind'] == 'select':
                effects = []
                cur = loc.evaluate('e => e.selectedIndex')
                for oi, opt in enumerate(c['options'] or []):
                    if oi == cur or len(effects) >= 6:
                        continue
                    b0 = pg.evaluate(SNAP); loc.select_option(index=oi); pg.wait_for_timeout(quiet_wait); d = diff(b0, pg.evaluate(SNAP), opt); d['option'] = opt
                    if c['in_form']: d['nothing_changed'] = False      # a field of a form is filled in, not operated: no visible effect is expected
                    effects.append(d)
                rec['options_tried'] = effects
            else:
                loc.scroll_into_view_if_needed(timeout=1500); loc.click(timeout=2500, force=False); pg.wait_for_timeout(quiet_wait)
                if not pg.url.startswith(url.split('?')[0].split('#')[0]):
                    rec['effect'] = 'navigated to ' + pg.url[-50:]; res.append(rec); continue
                d = diff(before, pg.evaluate(SNAP))
                if d['nothing_changed'] and not c.get('already_chosen'):
                    pg.wait_for_timeout(900); d2 = diff(before, pg.evaluate(SNAP))
                    if not d2['nothing_changed']:
                        d = d2; d['effect_after_a_pause'] = True
                rec.update(d)
                if c['in_form'] and rec.get('nothing_changed') and d.get('own_state_changed'):
                    rec['nothing_changed'] = False; rec['effect'] = 'a choice inside a form: only its own state changes'
                if c.get('already_chosen') and rec.get('nothing_changed'):
                    rec['nothing_changed'] = False; rec['effect'] = 'already the current choice: pressing it again changes nothing'
                if dialogs: rec['browser_dialog'] = dialogs[0]
                if downloads: rec['download_started'] = downloads[0]
                if requests: rec['network_requests'] = requests[:2]
                if d.get('claims_success') and not downloads and not requests and not d.get('stored_data_changed'):
                    rec['success_message_with_no_download_or_request'] = True
                gone = d['text_removed'] > 0 or any(l['after'] < l['before'] for l in d['lists_changed']) or d['text_changed'] >= 5 or any(re.search(r'\b(deleted|removed|cleared|emptied)\b', x, re.I) for x in d['examples'])
                if DESTRUCT.search(c['label']) and gone and not dialogs and not d['dialog_opened'] and not d.get('asks_first'):
                    pg.wait_for_timeout(50); undo = pg.evaluate("() => /\\bundo\\b/i.test(document.body.innerText)")
                    rec['removed_content_without_confirmation'] = True; rec['undo_offered'] = undo
                native = None
                if c['submit'] and c['in_form']:
                    native = pg.evaluate(f'''() => {{ const f = document.querySelector('[data-uic-w="{c["i"]}"]').closest('form'); return f ? {{novalidate: f.noValidate, valid: f.checkValidity(), required: f.querySelectorAll('[required]').length}} : null; }}''')
                    rec['form'] = native
                if d['field_styles_changed'] and d['text_added'] == 0 and d['text_changed'] == 0 and not d['dialog_opened'] and (not native or native['novalidate'] or native['valid']):
                    rec['error_shown_by_style_only'] = True     # fields changed their look and no text appeared
            res.append(rec)
        except Exception as e:
            res.append({'control': c.get('label'), 'kind': c.get('kind'), 'not_operated': str(e).splitlines()[0][:90]})
    pg.close()
    return res


VIEW_H = {320: 640, 360: 740, 390: 844, 412: 915, 768: 1024, 1280: 800, 1440: 900}
DEVICES = {'iphone': {'w': 390, 'h': 844, 'dpr': 3, 'touch': 44, 'insets': [59, 0, 34, 0]}, 'android': {'w': 412, 'h': 915, 'dpr': 2.625, 'touch': 48, 'insets': [24, 0, 24, 0]}}
SKIP = ('_census', '_doc', '_fonts', '_figures', '_focus', '_errors')
FIT_KEYS = ('page-overflow', 'content-cut-off', 'text-clipped', 'text-spill', 'text-overlap', 'control-overflow', 'scroll-unexpected', 'scroll-nested')
# Fonts with the same glyph widths (fontconfig, 30-metric-aliases.conf). Arial Nova is not in the list: its spacing differs from Arial's.
METRIC = {'arial': ['Arimo', 'Liberation Sans'], 'helvetica': ['TeX Gyre Heros', 'Nimbus Sans', 'Arimo', 'Liberation Sans'], 'arial narrow': ['Liberation Sans Narrow'],
          'times new roman': ['Tinos', 'Liberation Serif'], 'times': ['TeX Gyre Termes', 'Nimbus Roman', 'Tinos', 'Liberation Serif'], 'courier new': ['Cousine', 'Liberation Mono'],
          'georgia': ['Gelasio'], 'cambria': ['Caladea'], 'calibri': ['Carlito']}
# Wide fonts of each kind: an upper bound for a font that cannot be drawn here. A condensed or a fixed-width face is replaced by one of its own kind.
WIDE = {'sans': ['DejaVu Sans', 'Verdana', 'Bitstream Vera Sans'], 'serif': ['DejaVu Serif', 'Bitstream Vera Serif', 'Georgia'],
        'mono': ['DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier New'], 'condensed': ['DejaVu Sans Condensed']}


def font_kind(name, stack=''):
    n = name.lower(); st = stack.lower()
    if re.search(r'mono|code|courier|consolas|menlo|typewriter', n) or re.search(r'(^|[ ,])(ui-)?monospace', st):
        return 'mono'
    if re.search(r'condensed|narrow|compressed|\bcond\b', n):
        return 'condensed'
    return 'serif' if re.search(r'(^|[ ,"])serif', st.replace('sans-serif', '')) else 'sans'
HAVE = """(names) => { const p = document.createElement('span'); p.textContent = 'mmmmmmmmmlliWWW 0123456789'; p.style.cssText = 'position:absolute;left:-9999px;top:0;font-size:72px;white-space:nowrap';
  document.body.appendChild(p); const w = f => { p.style.fontFamily = f; return p.getBoundingClientRect().width; }; const bm = w('monospace'), bs = w('serif'), ba = w('sans-serif');
  const ok = names.filter(n => w('"' + n + '", monospace') !== bm || w('"' + n + '", serif') !== bs || w('"' + n + '", sans-serif') !== ba); p.remove(); return ok; }"""


def faces(name, target):
    loc = lambda *n: ','.join(f'local("{x}")' for x in n)
    f = lambda w, st, src: f'@font-face{{font-family:"{name}";font-weight:{w};font-style:{st};src:{src}}}'
    return (f(400, 'normal', loc(target, target + ' Regular')) + f(700, 'normal', loc(target + ' Bold', target)) +
            f(400, 'italic', loc(target + ' Italic', target + ' Oblique', target)) + f(700, 'italic', loc(target + ' Bold Italic', target + ' Bold Oblique', target + ' Bold', target)))


def font_plan(b, missing):
    """What can stand in for fonts that are not installed here: a font with the same widths, or else a wide font of the same kind as an upper bound.
    missing: {font name: the stack it leads}. Returns {font name: (stand-in, 'same widths' | 'wider, an upper bound') or None}."""
    pg = b.new_page(); pg.set_content('<body></body>')
    have = set(pg.evaluate(HAVE, sorted({c for m in missing for c in METRIC.get(m.lower(), [])} | {w for v in WIDE.values() for w in v}))); pg.close()
    plan = {}
    for m, stack in missing.items():
        same = next((c for c in METRIC.get(m.lower(), []) if c in have), None); wide = next((w for w in WIDE[font_kind(m, stack)] if w in have), None)
        plan[m] = (same, 'same widths') if same else ((wide, 'wider, an upper bound') if wide else None)
    return plan


def merge_fit(r, fit):
    for k in ('control-overflow', 'scroll-unexpected', 'scroll-nested'):
        r[k] = fit.get(k, [])
    have = {i.get('sel') for i in r.get('content-cut-off', [])}
    r.setdefault('content-cut-off', []).extend(i for i in fit.get('_cut_inside', []) if i['sel'] not in have)
    r['_fit'] = fit.get('_fit', {})


def fit_pass(b, url, w, h, css=None, device=None, insets=None):
    """One more rendering for fit and scrolling only: no screenshots, no pixel sampling, no walks."""
    kw = dict(viewport={'width': w, 'height': h}, reduced_motion='reduce')
    if device or w <= 480:
        kw.update(is_mobile=True, has_touch=True, device_scale_factor=(DEVICES[device]['dpr'] if device else 2))
    ctx = b.new_context(**kw); pg = ctx.new_page()
    try:
        pg.goto(url, wait_until='load', timeout=45000)
        if css:
            pg.add_style_tag(content=css); pg.evaluate('document.fonts.ready.then(() => 1)')
        pg.wait_for_timeout(450)
        opts = {'touchMin': (DEVICES[device]['touch'] if device else (44 if w <= 480 else 0)), 'device': device, 'obscured': bool(device) or w <= 480, 'insets': insets if device else None, 'vh': h}
        r = pg.evaluate(JS, opts); merge_fit(r, pg.evaluate(FIT, opts))
    except Exception as e:
        r = {'_errors': ['fit pass: ' + str(e).splitlines()[0][:100]]}
    ctx.close()
    return r


def only_new(extra, main, note):
    """Keep what this pass lists and the main pass at the same width does not."""
    sig = lambda k, i: k + '|' + str(i.get('sel') or i.get('table') or i.get('inner') or '')
    out = {}
    for k in FIT_KEYS:
        have = {sig(k, i) for i in main.get(k, [])}
        new = [dict(i, found=note) for i in extra.get(k, []) if sig(k, i) not in have]
        if new:
            out[k] = new
    out['_fit'] = extra.get('_fit') or {}
    if extra.get('_errors'):
        out['_errors'] = extra['_errors']
    return out


def scroll_end_shots(pg, r, shots, name, w, tag):
    """A scroll area shows its end only when scrolled there; a full-page screenshot of an app shell is one screen."""
    for s in (r.get('_fit') or {}).get('ends', []):
        q = f'document.querySelector(\'[data-uic-s="{s["i"]}"]\')'
        try:
            pg.evaluate(f'() => {{ const e = {q}; e.scrollIntoView({{block: "center"}}); e.scrollTop = e.scrollHeight; }}'); pg.wait_for_timeout(120)
            fn = f'{name}_{w}{tag}_scroll-end-{s["i"] + 1}.png'; pg.screenshot(path=f'{shots}/{fn}', full_page=False); r['_shots'].append(fn)
            pg.evaluate(f'() => {{ {q}.scrollTop = 0; scrollTo(0, 0); }}')
        except Exception:
            pass


def close_ups(pg, cdp, r, shots, name, w, vw, vh, dpr):
    """Crops at twice the size of every control group, form row and panel edge, plus one sheet of them per width."""
    import base64
    fit = r.get('_fit') or {}; items = [dict(c, pad=10) for c in fit.get('crops', [])]
    for p in fit.get('panels', []):
        items.append({'kind': 'right edge of', 'sel': p['sel'], 'x': p['x'] + p['w'] - 150, 'y': p['y'], 'w': 174, 'h': min(p['h'], 420), 'pad': 0})
        items.append({'kind': 'bottom edge of', 'sel': p['sel'], 'x': p['x'], 'y': p['y'] + p['h'] - 110, 'w': min(p['w'], 560), 'h': 134, 'pad': 0})
    if not items:
        return
    d = os.path.join(os.path.dirname(os.path.abspath(shots)), 'crops'); os.makedirs(d, exist_ok=True); done = []
    for i, c in enumerate(items[:30]):
        x, y = max(0, c['x'] - c['pad']), max(0, c['y'] - c['pad']); cw, ch = min(c['w'] + 2 * c['pad'], 900), min(c['h'] + 2 * c['pad'], 520)
        try:
            png = base64.b64decode(cdp.send('Page.captureScreenshot', {'format': 'png', 'clip': {'x': x, 'y': y, 'width': cw, 'height': ch, 'scale': 2 / dpr},
                                                                   'captureBeyondViewport': bool(y + ch > vh or x + cw > vw)})['data'])
        except Exception:
            continue
        fn = f'{name}_{w}_{i + 1:02d}.png'; open(os.path.join(d, fn), 'wb').write(png); done.append((fn, f"{i + 1:02d} {c['kind']} {c['sel']}"[:70], png))
    sheet = None
    if Image and done:
        from PIL import ImageDraw, ImageFont
        try:
            font = ImageFont.load_default(22)
        except TypeError:
            font = ImageFont.load_default()
        ims = [(lab, Image.open(io.BytesIO(png)).convert('RGB')) for _, lab, png in done]; W = 1800; x = y = 16; rowh = 0; pos = []
        for lab, im in ims:
            if im.width > W - 32:
                im = im.resize((W - 32, int(im.height * (W - 32) / im.width)))
            if x + im.width > W - 16 and x > 16:
                x = 16; y += rowh + 20; rowh = 0
            pos.append((lab, im, x, y)); rowh = max(rowh, im.height + 34); x += max(im.width, 360) + 24
        canvas = Image.new('RGB', (W, y + rowh + 16), '#ffffff'); dr = ImageDraw.Draw(canvas)
        for lab, im, x, y in pos:
            dr.text((x, y), lab, fill='#444444', font=font); canvas.paste(im, (x, y + 30)); dr.rectangle([x - 1, y + 29, x + im.width, y + 30 + im.height], outline='#bbbbbb')
        sheet = f'{name}_{w}_sheet.png'; canvas.save(os.path.join(d, sheet))
    r['_crops'] = {'folder': d, 'count': len(done), 'sheet': sheet}


def regression(res, base):
    """Compare with an earlier run of the same page: a control that has left its box, a scroll area that has grown, a control whose type changed."""
    out = {}; bp = base.get('pages', {}); bk = list(bp)
    for i, (page, rec) in enumerate(res['pages'].items()):
        old = bp.get(page) or next((bp[k] for k in bk if os.path.basename(k) == os.path.basename(page)), None) or (bp[bk[i]] if len(bk) == len(res['pages']) else None)
        if not old:
            out[page] = {'note': 'no page in the baseline to compare with'}; continue
        left, grew, style, compared = {}, {}, {}, 0
        for name, r in rec['passes'].items():
            o = old.get('passes', {}).get(name)
            if not o or not r.get('_fit') or not o.get('_fit'):
                continue
            compared += 1; oc = {c['key']: c for c in o['_fit'].get('controls', [])}
            for c in r['_fit'].get('controls', []):
                q = oc.get(c['key'])
                if not q:
                    continue
                label = c['key'].split('|')[1]
                if (c['past_box_px'] > 1 and q['past_box_px'] <= 1) or (c['cut_px'] > 1 and q['cut_px'] <= 1):
                    left.setdefault(c['key'], {'control': label, 'sel': c['sel'], 'now': f"{c['past_box_px']}px past {c['box']}" + (f", {c['cut_px']}px cut off" if c['cut_px'] > 1 else ''),
                                               'before': f"inside {q['box']}", 'passes': []})['passes'].append(name)
                ch = {k: f"{q.get(k)} -> {c.get(k)}" for k in ('weight', 'size', 'padding') if q.get(k) != c.get(k)}
                if ch and '_font-' not in name and '_scrollbars' not in name:
                    style.setdefault(c['key'], {'control': label, 'sel': c['sel'], 'changed': ch, 'passes': []})['passes'].append(name)
            osc = {s['key']: s for s in o['_fit'].get('scrollers', [])}
            for s in r['_fit'].get('scrollers', []):
                q = osc.get(s['key'])
                if q and s['scroll_height'] > 1.2 * q['scroll_height'] and s['scroll_height'] - q['scroll_height'] > 24:
                    grew.setdefault(s['key'], {'scroll_area': s['sel'], 'before': q['scroll_height'], 'now': s['scroll_height'], 'visible_height': s['client_height'],
                                               'grew_pct': round(100 * (s['scroll_height'] / q['scroll_height'] - 1)), 'passes': []})['passes'].append(name)
        out[page] = {'passes_compared': compared, 'control_left_its_box': list(left.values()), 'scroll_area_grew': list(grew.values()), 'control_style_changed': list(style.values())[:20]}
    return out


def measure(b, url, w, h, a, scheme, attr=None, shots=None, tag='', print_media=False, device=None, insets=None, do_focus=False):
    kw = dict(viewport={'width': w, 'height': h}, color_scheme=scheme, reduced_motion='reduce')
    if device or w <= 480:
        kw.update(is_mobile=True, has_touch=True, device_scale_factor=(DEVICES[device]['dpr'] if device else 2))
    ctx = b.new_context(**kw); pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    if device and insets:
        try:
            cdp.send('Emulation.setSafeAreaInsetsOverride', {'insets': {'top': insets[0], 'right': insets[1], 'bottom': insets[2], 'left': insets[3]}})
        except Exception:
            insets = None
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:100]))
    try:
        pg.goto(url, wait_until='load', timeout=45000)
    except Exception as e:
        ctx.close(); sys.exit(f'uicheck: could not open {url}: {str(e).splitlines()[0][:120]}')
    pg.wait_for_timeout(500)
    if print_media:
        pg.emulate_media(media='print')
    if attr:
        k, v = attr.split('=', 1); pg.evaluate(f'document.documentElement.setAttribute({json.dumps(k)}, {json.dumps(v)})'); pg.wait_for_timeout(150)
    if pg.evaluate('!document.body || !document.documentElement || document.documentElement.namespaceURI !== "http://www.w3.org/1999/xhtml"'):
        ctx.close(); sys.exit(f'uicheck: {url} is not an HTML page (no body element). Put the graphic inside an HTML page, or use shotcheck.py on an image of it.')
    opts = {'touchMin': (DEVICES[device]['touch'] if device else (44 if w <= 480 else 0)), 'device': device, 'obscured': bool(device) or w <= 480, 'insets': insets if device else None, 'vh': h}
    r = pg.evaluate(JS, opts); merge_fit(r, pg.evaluate(FIT, opts))
    sample_contrast(pg, r); confirm_listeners(pg, cdp, r)
    if print_media:   # paper changes what is cut off, hidden or unreadable; sizes and spacing are compared on screen, where points and pixels do not mix
        for k in ('type-scale-drift', 'section-rhythm', 'radius-drift', 'shadow-drift', 'edge-near-miss'):
            r[k] = []
    if errs:
        r['_errors'] = r.get('_errors', []) + ['script error on the page: ' + e for e in errs[:3]]
    if shots:
        os.makedirs(shots, exist_ok=True)
        name = re.sub(r'[^A-Za-z0-9._-]+', '_', os.path.basename(url.split('?')[0].rstrip('/')) or 'page') + (('_' + re.sub(r'\W+', '_', url.split('?', 1)[1])) if '?' in url else '')
        pg.evaluate('window.scrollTo(0,0)')
        pg.screenshot(path=f'{shots}/{name}_{w}{tag}_first-screen.png', full_page=False)
        pg.screenshot(path=f'{shots}/{name}_{w}{tag}.png', full_page=True)
        r['_shots'] = [f'{name}_{w}{tag}_first-screen.png', f'{name}_{w}{tag}.png']
        if not print_media:
            scroll_end_shots(pg, r, shots, name, w, tag)
            if not tag:
                close_ups(pg, cdp, r, shots, name, w, w, h, kw.get('device_scale_factor', 1))
    if not print_media:      # a header declared sticky must still be there after scrolling
        try:
            for it in pg.evaluate(STICKY):
                if not any(x.get('table') == it['table'] for x in r['table-sticky']):
                    r['table-sticky'].append(it)
        except Exception:
            pass
    if do_focus:
        r.update(focus_check(pg))
        try:
            pg.evaluate('window.scrollTo(0,0)'); r['_tab_walk'] = tab_walk(pg)
        except Exception as e:
            r['_tab_walk'] = {'error': str(e)[:80]}
    ctx.close()
    return r


def run(pages, a):
    widths = [int(x) for x in a.widths.split(',')] if a.widths else None
    dev = a.device if a.device in DEVICES else None
    insets = [int(x) for x in a.insets.split(',')] if a.insets else (DEVICES[dev]['insets'] if dev else None)
    if dev and not widths:
        widths = [DEVICES[dev]['w'], 360]
    widths = widths or [360, 768, 1280]
    res = {'tool': 'uicheck 2', 'pages': {}, 'widths': widths, 'device': dev, 'started': time.strftime('%Y-%m-%d %H:%M')}
    with sync_playwright() as p:
        b = p.chromium.launch()
        import platform
        res['environment'] = {'browser': 'Chromium ' + b.version.split('.')[0] + ' (headless)', 'system': platform.system(), 'scrollbar_px_main_passes': None, 'scrollbar_px_scrollbar_pass': None}
        b2 = None
        if not dev and any(w > 480 for w in widths):      # Playwright hides scrollbars; desktop browsers on Windows and Linux draw them and take their width from the layout
            try:
                b2 = p.chromium.launch(ignore_default_args=['--hide-scrollbars'])
            except Exception:
                b2 = None
        for page in pages:
            url = uri(page); passes = {}; widest = max(widths)
            for w in widths:
                h = a.height or (DEVICES[dev]['h'] if dev and w == DEVICES[dev]['w'] else VIEW_H.get(w, 800))
                passes[f'{w}'] = measure(b, url, w, h, a, 'light', shots=a.shots, device=dev, insets=insets, do_focus=(w == widest))
            first = passes[str(widths[0])]; dark_styles = first['_doc'].get('dark_styles')
            narrow_w, wide_w = min(widths), max(widths)
            if wide_w >= 1024 and narrow_w <= 480 and not dev:      # controls shown on desktop that have no counterpart at phone width
                wide_c, nar_c = passes[str(wide_w)].get('_controls', []), passes[str(narrow_w)].get('_controls', [])
                have = {c['name'].lower() for c in nar_c}; gone = [c for c in wide_c if c['name'].lower() not in have and not c['toggle']]
                toggles = [c['name'] for c in nar_c if c['toggle'] and c['name'].lower() not in {x['name'].lower() for x in wide_c}]
                if toggles:      # a menu button appears at the narrow width: the links it replaces are taken to be inside it
                    gone = [c for c in gone if c['tag'] != 'a']
                opts_n = [o for c in nar_c for o in (c.get('options') or [])]      # a list box at the narrow width replaces the row of buttons whose words it offers
                word = lambda t: re.split(r'[,(\d]', t.lower())[0].strip()
                gone = [c for c in gone if not (word(c['name']) and any(word(c['name']) == word(o) for o in opts_n))]
                if gone:
                    passes[str(narrow_w)].setdefault('nav-hidden', []).append({'hidden_at': narrow_w, 'shown_at': wide_w, 'count': len(gone),
                        'controls': [(c['name'] + (' -> ' + c['href'] if c['href'] else ''))[:60] for c in gone[:12]],
                        'new_toggles_at_narrow_width': toggles[:4], 'note': 'not a finding when a toggle listed here reveals them, or when only in-page section links are hidden on a single-scroll page'})
            extra = []
            if a.dark or dark_styles:
                extra += [(w, 'dark', None, '_dark') for w in sorted({widths[0], widest})]
            if a.attr:
                extra += [(w, 'light', a.attr, '_' + re.sub(r'\W+', '_', a.attr)) for w in sorted({widths[0], widest})]
            for w, scheme, attr, tag in extra:
                h = a.height or (DEVICES[dev]['h'] if dev and w == DEVICES[dev]['w'] else VIEW_H.get(w, 800))
                passes[f'{w}{tag}'] = measure(b, url, w, h, a, scheme, attr=attr, shots=a.shots, tag=tag, device=dev, insets=insets)
            for st in (a.states.split(',') if a.states else []):
                su = url + ('&' if '?' in url else '?') + 'state=' + st
                for w in sorted({widths[0], widest}):
                    passes[f'{w}_state-{st}'] = measure(b, su, w, VIEW_H.get(w, 800), a, 'light', shots=a.shots, tag='_state-' + st, device=dev, insets=insets)
            if a.print_media:
                passes['print'] = measure(b, url, 794, 1123, a, 'light', shots=a.shots, tag='_print', print_media=True)
            vh = lambda w: a.height or (DEVICES[dev]['h'] if dev and w == DEVICES[dev]['w'] else VIEW_H.get(w, 800))
            # fonts the page asks for first and this machine does not have; a stand-in with the same widths makes the fit true to the real font
            want = {f['not_available_here'][0]: f['rendered_with'] for f in first['_fonts'] if f['not_available_here']}; stacks = {f['not_available_here'][0]: f['stack'] + ', ' + (f.get('generic') or '') for f in first['_fonts'] if f['not_available_here']}
            miss = sorted(m for m, drawn in want.items() if (drawn or '') not in METRIC.get(m.lower(), []))
            fitrec = {'fonts_not_available': sorted(want), 'drawn_in': want, 'fit_as_real_font': sorted(set(want) - set(miss)), 'font_pass': {}}
            res['environment']['scrollbar_px_main_passes'] = (first.get('_fit') or {}).get('env', {}).get('scrollbar_px')
            if miss:      # a narrower stand-in hides what the real font would push out of its box
                plan = font_plan(b, {m: stacks[m] for m in miss}); fitrec['font_pass'] = {m: (f'{t[0]} ({t[1]})' if t else None) for m, t in plan.items()}
                css = ''.join(faces(m, t[0]) for m, t in plan.items() if t)
                note = 'only with ' + '; '.join(f'{m} drawn in {t[0]} ({t[1]})' for m, t in plan.items() if t) + (': at risk with the real font' if any(t and t[1] != 'same widths' for t in plan.values()) else ': as the real font would lay it out')
                for w in (widths if css else []):
                    passes[f'{w}_font-check'] = only_new(fit_pass(b, url, w, vh(w), css, dev, insets), passes[str(w)], note)
            if b2:
                for w in [w for w in widths if w > 480]:
                    sp = fit_pass(b2, url, w, vh(w)); px = (sp.get('_fit') or {}).get('env', {}).get('scrollbar_px'); res['environment']['scrollbar_px_scrollbar_pass'] = px
                    if px:
                        passes[f'{w}_scrollbars'] = only_new(sp, passes[str(w)], f'only with scrollbars that take {px}px, as on Windows and Linux desktops')
            rec = {'address': url, 'passes': passes, 'dark_styles_detected': bool(dark_styles), 'dark_measured': bool(a.dark or dark_styles), 'fit': fitrec}
            if not a.no_walk:
                w = DEVICES[dev]['w'] if dev else widest
                kw = dict(viewport={'width': w, 'height': VIEW_H.get(w, 800)}, reduced_motion='reduce')
                if dev: kw.update(is_mobile=True, has_touch=True)
                ctx = b.new_context(**kw)
                try:
                    rec['walk'] = click_census(ctx, url)
                except Exception as e:
                    rec['walk'] = [{'error': str(e)[:100]}]
                ctx.close()
            res['pages'][page] = rec
        b.close()
        if b2:
            b2.close()
    if getattr(a, 'baseline', None):
        try:
            res['regression'] = regression(res, json.load(open(a.baseline, encoding='utf-8'))); res['baseline'] = a.baseline
        except Exception as e:
            res['regression'] = {'error': f'could not read the baseline {a.baseline}: {str(e)[:80]}'}
    # cross-page drift (flows): the same tokens on every screen
    if len(pages) > 1:
        tok = {}
        for page, rec in res['pages'].items():
            c = rec['passes'][str(widths[0])]['_census']
            tok[page] = {'families': sorted(c['font_families']), 'radii': sorted(c['radii']), 'sizes': sorted(c['font_sizes'], key=float), 'shadows': c['shadows']}
        drift = {}
        for k in ('families', 'radii', 'sizes', 'shadows'):
            vals = {json.dumps(t[k]) for t in tok.values()}
            if len(vals) > 1:
                drift[k] = {os.path.basename(pg): t[k] for pg, t in tok.items()}
        res['style-drift'] = drift
    blob = json.dumps(res, sort_keys=True, default=str).encode()
    res['run_id'] = hashlib.sha1(blob).hexdigest()[:8]
    return res


def checks_of(r):
    return [k for k in r if not k.startswith('_')]


def render(res, quiet=False, limit=6):
    L = []
    for page, rec in res['pages'].items():
        ps = rec['passes']; first = next(iter(ps.values()))
        L.append(f"# uicheck run {res['run_id']}: {page}   device: {res['device'] or 'none'}   widths: {'/'.join(str(w) for w in res['widths'])}")
        d = first['_doc']
        L.append(f"dark styles in the page: {'yes, measured too' if rec['dark_styles_detected'] else ('no (forced with --dark)' if rec['dark_measured'] else 'no')} | canvas elements (not measurable, look at them): {d['canvases']} | viewport-fit=cover: {'yes' if d['viewport_fit_cover'] else 'no'}")
        miss = sorted({n for f in first['_fonts'] for n in f['not_available_here']})
        if miss:
            L.append('fonts not available on this machine (text is drawn in the next font of each stack; widow and wrap candidates still count, say which font stood in): ' + ', '.join(miss))
            fr = rec.get('fit', {}); fp = fr.get('font_pass') or {}
            if fr.get('fit_as_real_font'):
                L.append('fit as with the real font for: ' + ', '.join(f"{m} (drawn in {fr['drawn_in'][m]}, same widths)" for m in fr['fit_as_real_font']))
            if fp:
                done = {m: t for m, t in fp.items() if t}; none = [m for m, t in fp.items() if not t]
                L.append('fit with the real font is NOT what the main passes show for: ' + ', '.join(f"{m} (drawn in {fr['drawn_in'].get(m) or 'a default font'})" for m in fp) + '. '
                         + ('Font pass: ' + '; '.join(f'{m} drawn in {t}' for m, t in done.items()) + '. What only that pass lists is marked _font-check. ' if done else '')
                         + ('No stand-in on this machine for ' + ', '.join(none) + ': list fit under Verify, never under Clean.' if none else ''))
        for name, r in ps.items():
            parts = [f"{k} {len(r[k])}" for k in checks_of(r) if r[k]]
            L.append(f"## {name}: " + (' | '.join(parts) if parts else 'no candidates'))
            if r.get('_errors'):
                L.append('   errors: ' + '; '.join(r['_errors'][:3]))
        widest = ps[str(max(res['widths']))]
        if '_focus' in widest:
            f = widest['_focus']; L.append(f"focus: {f['tested']} of {f['focusable']} focusable elements tested ({f['distinct_looks']} distinct looks); no visible change on {len(widest['focus-missing'])}; weak change on {len(widest['focus-weak'])}; test errors {f['errors']}")
        if '_tab_walk' in widest and 'stops' in widest['_tab_walk']:
            t = widest['_tab_walk']; L.append(f"tab walk: {t['stops']} stops; backward jumps {len(t['backward_jumps'])}; stops not visible {len(t['stops_not_visible'])}; stuck on {t['stuck_on']}")
        c = first['_census']; wd = ps[str(max(res['widths']))]['_census']
        L.append(f"census ({max(res['widths'])}px): radii {sorted(wd['radii'])} | shadows {wd['shadows']} | font sizes {len(wd['font_sizes'])} | families {sorted(wd['font_families'])} | weights {sorted(wd['font_weights'])} | "
                 f"section paddings {sorted({x['top'] for x in wd['section_padding']} | {x['bottom'] for x in wd['section_padding']}, key=lambda v: float(v[:-2]) if v.endswith('px') else 0)} | icon strokes {wd['icon_strokes'][:5]}")
        L.append(f"decoration ({max(res['widths'])}px): {json.dumps(wd['decoration'])}")
        fs = wd['first_screen']; L.append(f"first screen at {max(res['widths'])}x{fs['height']}: h1 inside {fs['h1_inside']} | largest text {[(x['px'], x['text'][:24]) for x in fs['largest_text']]} | filled buttons {[x['text'] for x in fs['filled_buttons']]} | interactive elements {fs['interactive_elements']} | navigation {wd['navigation']}")
        fs = first['_census']['first_screen']; L.append(f"first screen at {res['widths'][0]}x{fs['height']}: h1 inside {fs['h1_inside']} | filled buttons {[x['text'] for x in fs['filled_buttons']]} | interactive elements {fs['interactive_elements']}")
        if not quiet:
            merged = {}
            for name, r in ps.items():
                for k in checks_of(r):
                    for item in r[k][:60]:
                        sig = json.dumps(item, sort_keys=True, ensure_ascii=False)
                        merged.setdefault(k, {}).setdefault(sig, []).append(name)
            for k in sorted(merged):
                items = list(merged[k].items())
                L.append(f"### {k} ({len(items)})")
                for sig, where in items[:limit]:
                    L.append(f"- {sig}  @{','.join(where)}")
                if len(items) > limit:
                    L.append(f"- ... {len(items) - limit} more in checks.json (open it: unlisted items are still candidates)")
            if first['_figures']:
                L.append('### figures to cross-check (same thing must show the same number everywhere)')
                for f in first['_figures'][:24]:
                    L.append(f"- {f['value']}  ({f['label']})" + (f"  | the same label beside another number: {f['elsewhere']}" if f.get('elsewhere') else ''))
            if rec.get('walk'):
                L.append('### click census (each control operated once on a fresh copy of the page)')
                for wk in rec['walk'][:45]:
                    flags = [k for k in ('broken_anchor', 'broken_link', 'label_and_destination_share_no_word', 'removed_content_without_confirmation', 'success_message_with_no_download_or_request', 'error_shown_by_style_only', 'nothing_changed', 'list_emptied_without_message') if wk.get(k)]
                    for o in wk.get('options_tried', []):
                        flags += [f"{o['option']}: {k}" for k in ('only_echoes_the_choice', 'list_emptied_without_message', 'nothing_changed') if o.get(k)]
                    brief = wk.get('effect') or wk.get('goes_to') or wk.get('not_operated') or ('; '.join(wk.get('examples', [])[:2]) if 'examples' in wk else '')
                    L.append(f"- [{wk.get('kind')}] {wk.get('control')}: {brief}" + (f"  -> target heading: {wk['target_heading']}" if wk.get('target_heading') else '') + (f"  FLAGS: {', '.join(flags)}" if flags else ''))
        cr = [(n, r['_crops']) for n, r in ps.items() if r.get('_crops')]; ends = [x for r in ps.values() for x in r.get('_shots', []) if '_scroll-end-' in x]
        if cr:
            L.append('close-ups (look at each sheet: control groups, form rows and panel edges at twice the size): ' + '; '.join(f"{c['folder']}/{c['sheet'] or '(no sheet: Pillow missing, ' + str(c['count']) + ' files)'}" for _, c in cr))
        if ends:
            L.append('scrolled-to-the-end screenshots (look at them: a full-page screenshot cannot show the end of a scroll area): ' + ', '.join(ends[:12]))
        rg = res.get('regression')
        if rg is not None:
            g = rg.get(page, rg if 'error' in rg else {})
            L.append(f"### regression against {res.get('baseline')}")
            if g.get('error') or g.get('note'):
                L.append('- ' + (g.get('error') or g.get('note')))
            else:
                for k, lab in (('control_left_its_box', 'CONTROL LEFT ITS BOX'), ('scroll_area_grew', 'SCROLL AREA GREW by more than a fifth'), ('control_style_changed', 'type or padding of a control changed (confirm it was meant)')):
                    for it in g.get(k, [])[:12]:
                        L.append(f"- {lab}: {json.dumps(it, ensure_ascii=False)}")
                if not any(g.get(k) for k in ('control_left_its_box', 'scroll_area_grew', 'control_style_changed')):
                    L.append(f"- nothing: no control left its box, no scroll area grew, no control changed type or padding ({g.get('passes_compared', 0)} passes compared)")
        if 'style-drift' in res:
            L.append('### style-drift between screens: ' + (json.dumps(res['style-drift']) if res['style-drift'] else 'none (same families, radii, sizes and shadow count on every screen)'))
        L.append('')
    env = res.get('environment', {}); fonts = sorted({n for rec in res['pages'].values() for n in rec.get('fit', {}).get('fonts_not_available', [])})
    sp = env.get('scrollbar_px_scrollbar_pass')
    L.append(f"environment: {env.get('browser', 'Chromium')} on {env.get('system', '?')} | scrollbars in the main passes: {'drawn over the content (0px)' if not env.get('scrollbar_px_main_passes') else str(env['scrollbar_px_main_passes']) + 'px'}"
             + (f" | scrollbar pass: {sp}px each, what only that pass lists is marked _scrollbars" if sp else ' | no scrollbar pass (phone widths only, or it could not start)'))
    L.append(f"Quote in the report header: uicheck run {res['run_id']} ({env.get('browser', 'Chromium')} on {env.get('system', '?')}; "
             + (f"{', '.join(fonts)} not installed, a stand-in drew the text; " if fonts else 'all fonts drawn as named; ')
             + (f"scrollbars hidden in the main passes and {env['scrollbar_px_scrollbar_pass']}px in the scrollbar pass)" if env.get('scrollbar_px_scrollbar_pass') else 'scrollbars drawn over the content)'))
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Measure a rendered page. Check names match references/severity-registry.md.')
    ap.add_argument('pages', nargs='+'); ap.add_argument('--out'); ap.add_argument('--json'); ap.add_argument('--shots')
    ap.add_argument('--widths'); ap.add_argument('--height', type=int); ap.add_argument('--device', choices=['iphone', 'android']); ap.add_argument('--insets')
    ap.add_argument('--dark', action='store_true'); ap.add_argument('--attr'); ap.add_argument('--states'); ap.add_argument('--print', dest='print_media', action='store_true')
    ap.add_argument('--no-walk', action='store_true'); ap.add_argument('--fail-on'); ap.add_argument('--quiet', action='store_true'); ap.add_argument('--baseline')
    a = ap.parse_args()
    if a.out:
        a.json = a.json or os.path.join(a.out, 'checks.json'); a.shots = a.shots or os.path.join(a.out, 'shots')
    res = run(a.pages, a)
    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump(res, open(a.json, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    print(render(res, a.quiet))
    if a.fail_on:
        want = None if a.fail_on == 'all' else set(a.fail_on.split(','))
        hit = sorted({k for rec in res['pages'].values() for r in rec['passes'].values() for k in checks_of(r) if r[k] and (want is None or k in want)})
        if (want is None or 'regression' in want) and any(g.get('control_left_its_box') or g.get('scroll_area_grew') for g in (res.get('regression') or {}).values() if isinstance(g, dict)):
            hit.append('regression')
        if hit:
            print('FAILED on: ' + ', '.join(hit)); sys.exit(1)
