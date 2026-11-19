#!/usr/bin/env python3
"""Build D2C: Version 1 (me-redesign/) with the D2B "three sites in one" header.

Version 1 is copied, never changed. Its own masthead and menu bar are hidden and the three-tab header
(Mobile Europe / The Briefing / Independent Research, each with its own coloured menu bar) is added in
their place by shared.js. The header styles are taken from the D2B block in me-redesign-v2/styles.css.
The mockup bar gets a "Version 1 / D2C" switch that keeps you on the same page.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign'
OUT = ROOT / 'me-redesign-d2c'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

# ---- pages: franchise bands go (their menus move into the header bar); tag the body ----
for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    t = re.sub(r'<div class="fband [^"]*">\n  <div class="wrap">.*?\n  </div>\n</div>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'<body([^>]*?) class="([^"]*)"', r'<body\1 class="d2c \2"', t, count=1)
    if ' class="d2c' not in t:
        t = re.sub(r'<body([^>]*)>', r'<body\1 class="d2c">', t, count=1)
    t = t.replace(' – Mobile Europe mockup</title>', ' – Mobile Europe D2C mockup</title>').replace('Homepage mockup</title>', 'Homepage D2C mockup</title>')
    f.write_text(t)

# ---- styles: the D2B header block, re-scoped to D2C, plus hiding Version 1's own masthead/menu ----
v2css = (ROOT / 'me-redesign-v2' / 'styles.css').read_text()
block = v2css[v2css.index('/* ===================== D2B: "three sites in one" header'):]
block = block.replace('.d2b', '.d2c').replace('D2B', 'D2C')
extra = '''
/* D2C: Version 1's own masthead and menu bar are replaced by the three-tab header */
.d2c .mast,.d2c .nav,.d2c .promo-strip{display:none!important}
.d2c .tri{margin-top:0}
'''
css = (OUT / 'styles.css').read_text() + '\n\n' + block + extra
(OUT / 'styles.css').write_text(css)

# ---- shared.js: build the header, version switch, drop the old header picker ----
js = (OUT / 'shared.js').read_text()
js = js.replace('<span class="lbl" style="padding:0 6px;color:#888">Mockup <b style="color:#fff">v1</b></span>',
                '<span class="lbl" style="padding:0 2px 0 6px;color:#888">Mockup</span><select id="ver-switch" aria-label="Mockup version"><option value="me-redesign-d2a">D2A</option><option value="me-redesign-d2b">D2B</option><option value="me-redesign-d2c">D2C</option></select><span class="div"></span>', 1)
js = re.sub(r'\n    <span class="div"></span>\n    <label class="lbl" for="hdr-var".*?</select>', '', js, count=1, flags=re.S)
js += r"""

// ===== D2C: "three sites in one" header =====
(function () {
  const page = document.body.dataset.page;
  const site = page === 'brief' || page === 'brief-event' ? 'brief' : page === 'res' ? 'res' : 'me';
  const ME_NAV = [['index.html', 'Home'], ['news.html', 'News'], ['insights.html', 'Insights'], ['cxo.html', 'CxO Zone'], ['white-papers.html', 'White Papers'], ['videos.html', 'Videos'], ['events.html', 'Events']];
  const BRIEF_NAV = [['the-briefing.html', 'Upcoming Briefings'], ['#', 'On demand'], ['#', 'Sponsor a Briefing'], ['#', 'Contact']];
  const RES_NAV = [['research.html', 'All reports'], ['research.html#analysts', 'Our analysts'], ['#', 'Topics'], ['#', 'Commission research']];
  const ME_ON = { home: 'index.html', news: 'news.html', cat: 'news.html', article: 'news.html', insights: 'insights.html', cxo: 'cxo.html', 'white-papers': 'white-papers.html', videos: 'videos.html', events: 'events.html' };
  const [items, on] = { me: [ME_NAV, ME_ON[page]], brief: [BRIEF_NAV, 'the-briefing.html'], res: [RES_NAV, 'research.html'] }[site];
  const nav = items.map(([h, t]) => `<a href="${h}"${h === on ? ' class="on" aria-current="page"' : ''}>${t}</a>`).join('');
  const tab = s => s === site ? ' on" aria-current="true' : '';
  const hasSearch = !!document.getElementById('search-toggle');
  const html = `<header class="tri" data-site="${site}">
    <div class="wrap tri-tabs">
      <a class="tri-tab me${tab('me')}" href="index.html" aria-label="Mobile Europe home">
        <img class="tri-logo" src="../brand/mobile-europe-logo-strap.png" alt="Mobile Europe: Communications infrastructure and digital services in EMEA" width="1343" height="236">
        <img class="tri-mark" src="../brand/me-mark.png" alt="" width="400" height="400">
      </a>
      <a class="tri-tab brief${tab('brief')}" href="the-briefing.html"><b>The Briefing</b></a>
      <a class="tri-tab res${tab('res')}" href="research.html"><b>Independent Research</b></a>
    </div>
    <div class="tri-bar"><div class="wrap">
      <nav class="tri-nav" aria-label="Site menu">${nav}</nav>
      <div class="tri-tools">
        ${hasSearch ? '<button class="tri-ico" type="button" id="tri-search" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg></button>' : ''}
        <a class="tri-sub" href="#" data-subscribe>Subscribe</a>
        <a class="tri-login" href="#" data-login>Log in</a>
        <button class="tri-ico tri-menu" type="button" id="tri-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
      </div>
    </div></div>
  </header>`;
  const anchor = document.querySelector('.lb-zone') || document.querySelector('.mast');
  if (!anchor) return;
  anchor.insertAdjacentHTML('afterend', html);
  const s = document.getElementById('tri-search');
  if (s) s.addEventListener('click', () => document.getElementById('search-toggle').click());
  document.getElementById('tri-menu').addEventListener('click', () => { const b = document.querySelector('.burger'); if (b) b.click(); });
  const m = window.ME_MEMBER && ME_MEMBER.get();
  if (m) { const l = document.querySelector('.tri-login'); l.textContent = 'Hi, ' + m.first; l.setAttribute('href', 'members.html'); l.removeAttribute('data-login'); }
})();

// Version 1 / D2C switch (mockup only): same page, other version
(function () {
  const sel = document.getElementById('ver-switch'); if (!sel) return;
  const here = (location.pathname.match(/\/(me-redesign(?:-d2[abc])?)\//) || [])[1] || 'me-redesign';
  sel.value = here;
  // pages that only exist in D2A/D2B fall back to the homepage elsewhere
  const ONLY_NEW = ['about.html', 'editorial-board.html', 'white-paper.html'];
  sel.addEventListener('change', () => {
    let file = location.pathname.split('/').pop() || 'index.html';
    if (/^me-redesign(-d2c)?$/.test(sel.value) && ONLY_NEW.includes(file)) file = 'index.html';
    location.href = '../' + sel.value + '/' + file + location.search + location.hash;
  });
})();
"""
(OUT / 'shared.js').write_text(js)

# cache-bust both files on every page
for f in OUT.glob('*.html'):
    t = f.read_text()
    f.write_text(re.sub(r'(styles\.css|shared\.js)\?v=\d+', r'\1?v=d2c2', t))
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
