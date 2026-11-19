#!/usr/bin/env python3
"""Build D2B: the D2A site with a "three sites in one" header.

Mobile Europe, The Briefing and Independent Research each get a folder tab. The site you are in has the
raised tab, joined to a menu bar in that site's colour (grey / navy / red) carrying that site's own menu.
Built from me-redesign-d2a/ (run tools/build_d2a_site.py first); D2A and Version 2 are not changed.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2a'
OUT = ROOT / 'me-redesign-d2b'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

ME_NAV = [('index.html', 'Home'), ('news.html', 'News'), ('insights.html', 'Insights'), ('cxo.html', 'CxO Zone'),
          ('white-papers.html', 'White Papers'), ('videos.html', 'Videos'), ('events.html', 'Events'), ('about.html', 'About')]
BRIEF_NAV = [('the-briefing.html', 'Upcoming Briefings'), ('#', 'On demand'), ('#', 'Sponsor a Briefing'), ('#', 'Contact')]
RES_NAV = [('research.html', 'All reports'), ('research.html#analysts', 'Our analysts'), ('#', 'Topics'), ('#', 'Commission research')]
ME_ON = {'home': 'index.html', 'news': 'news.html', 'cat': 'news.html', 'article': 'news.html', 'insights': 'insights.html',
         'cxo': 'cxo.html', 'white-papers': 'white-papers.html', 'videos': 'videos.html', 'events': 'events.html', 'about': 'about.html'}

SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'


def header(page):
    site = 'brief' if page in ('brief', 'brief-event') else 'res' if page == 'res' else 'me'
    items, on = {'me': (ME_NAV, ME_ON.get(page)), 'brief': (BRIEF_NAV, 'the-briefing.html'), 'res': (RES_NAV, 'research.html')}[site]
    nav = ''.join(f'<a href="{h}"' + (' class="on" aria-current="page"' if h == on else '') + f'>{t}</a>' for h, t in items)
    tab = lambda s: ' on" aria-current="true' if s == site else ''
    return f'''<!-- D2B: three sites in one. The site you are in has the raised tab, joined to its own menu bar -->
<header class="tri" data-site="{site}">
  <div class="wrap tri-tabs">
    <a class="tri-tab me{tab('me')}" href="index.html" aria-label="Mobile Europe home">
      <img class="tri-logo" src="../brand/mobile-europe-logo-strap.png" alt="Mobile Europe: Communications infrastructure and digital services in EMEA" width="1343" height="236">
      <img class="tri-mark" src="../brand/me-mark.png" alt="" width="400" height="400">
    </a>
    <a class="tri-tab brief{tab('brief')}" href="the-briefing.html"><b>The Briefing</b></a>
    <a class="tri-tab res{tab('res')}" href="research.html"><b>Independent Research</b></a>
  </div>
  <div class="tri-bar">
    <div class="wrap">
      <nav class="tri-nav" aria-label="{ {'me': 'Mobile Europe', 'brief': 'The Briefing', 'res': 'Independent Research'}[site] } menu">{nav}</nav>
      <div class="tri-tools">
        <button class="tri-ico" type="button" id="cv-search" aria-label="Search">{SEARCH}</button>
        <a class="tri-sub" href="#" data-subscribe>Subscribe</a>
        <a class="tri-login cv-login" href="#" data-login>Log in</a>
        <button class="tri-ico tri-menu" type="button" id="cv-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
      </div>
    </div>
  </div>
</header>
'''


for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    page = re.search(r'<body data-page="([^"]+)"', t).group(1)
    t = re.sub(r'<!-- Cover header.*?</header>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'\n?<!-- (Slim section bar|Tabs move up under the header on inner pages) -->.*?</nav>\n', '\n', t, count=1, flags=re.S)
    t = re.sub(r'<div class="fband [^"]*">\n  <div class="wrap">.*?\n  </div>\n</div>\n', '', t, count=1, flags=re.S)
    t = t.replace('<div id="site-header"></div>\n', '<div id="site-header"></div>\n' + header(page), 1)
    t = t.replace("querySelector('.cv-bar')", "querySelector('.tri')")
    t = re.sub(r'(<body[^>]*class=")', r'\1d2b ', t, count=1)
    t = t.replace(' – Mobile Europe mockup</title>', ' – Mobile Europe D2B mockup</title>').replace('Mobile Europe – D2A homepage mockup', 'Mobile Europe – D2B homepage mockup')
    f.write_text(t)

js = (OUT / 'shared.js').read_text()
js = js.replace("document.querySelector('.cv-sections'), cats", "document.querySelector('.tri'), cats")
js = re.sub(r'<label class="lbl" for="tab-style">Tabs</label><select id="tab-style".*?</select><span class="div"></span>', '', js, count=1, flags=re.S)
(OUT / 'shared.js').write_text(js)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
