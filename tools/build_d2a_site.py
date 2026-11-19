#!/usr/bin/env python3
"""Build the full D2A site (cover header, tabs moved up, page transitions) into me-redesign-d2a/.

Version 2 (me-redesign-v2/) is the source and is never changed. Run tools/build_cover_pages.py
first if the D2A homepage/article/news templates in v2 need regenerating.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-v2'
OUT = ROOT / 'me-redesign-d2a'

SKIP = re.compile(r'^(home-.*|article-cover|news-cover)\.html$')

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for f in SRC.iterdir():
    if f.suffix in ('.js', '.css') or (f.suffix == '.html' and not SKIP.match(f.name)):
        shutil.copy2(f, OUT / f.name)


def rel_links(html):
    """Point the D2A templates at this folder's normal page names."""
    return (html.replace('home-cover-2a.html', 'index.html').replace('home-cover.html', 'index.html')
                .replace('article-cover.html', 'article.html').replace('news-cover.html', 'news.html'))


# ---- templates taken from the D2A pages built in v2 ----
ABOUT_TAB = ('<a href="events.html">Events</a>', '<a href="events.html">Events</a><a href="about.html">About</a>')
home = rel_links((SRC / 'home-cover-2a.html').read_text()).replace(*ABOUT_TAB)
VT_STYLE = re.search(r'<style>\n/\* D2A.*?</style>', home, re.S).group(0)
COVER_HDR = re.search(r'<!-- Cover header.*?</header>\n', home, re.S).group(0)
NAV = re.search(r'<!-- Slim section bar -->.*?</nav>\n', home, re.S).group(0)
NAV_UP = NAV.replace('<!-- Slim section bar -->', '<!-- Tabs move up under the header on inner pages -->').replace('<nav class="cv-sections"', '<nav class="cv-sections cv-up"')
article_t = rel_links((SRC / 'article-cover.html').read_text()).replace(*ABOUT_TAB)
SUB_JS = re.search(r'<script>\n\(function \(\) \{\n  document.getElementById\(\'cv-menu\'\).*?</script>', article_t, re.S).group(0)

home = home.replace('Option D2A · Cover, split + transitions – Mobile Europe mockup', 'Mobile Europe – D2A homepage mockup')
# Below the cover top (hero, tabs, speakers, latest news, quotes) carry on as the Current homepage:
# billboard, Insights, Independent Research band, CxO Zone, White Paper Hub, The Briefing & Events
cur = (SRC / 'index.html').read_text()
rest = cur[cur.index('<div class="bb-zone">'):cur.index('<div id="site-footer">')]
home = re.sub(r'\n  <section class="heard">.*?\n  </section>\n', '\n', home, count=1, flags=re.S)  # no "Heard at Mobile Europe"
# Pinned (sponsored) post in More latest news, as on the Current homepage: it takes the last card's place
# and shared.js drops it into a random mid-grid position
pin = re.search(r'\n        <div class="pin-slot">.*?\n        </div>', cur, re.S).group(0)
grid = re.search(r'<h2>More latest news</h2>.*?<div class="grid3">(.*?)\n      </div>', home, re.S)
cards = re.findall(r'\n        <a class="card".*?</a>', grid.group(1))
home = home.replace(grid.group(1), ''.join(cards[:-1]) + pin, 1)
cut = home.index('<div id="site-footer">')
home = home[:cut] + '\n' + rest + home[cut:]
(OUT / 'index.html').write_text(home)
(OUT / 'article.html').write_text(article_t)

# category chips (all topics), used in the band on category pages
CATS = []
for f in sorted(SRC.glob('category-*.html')):
    t = re.search(r'<h1 class="ptitle">(.*?)</h1>', f.read_text()).group(1)
    CATS.append((f.name, t))

TAB_FOR = {'news': 'news.html', 'insights': 'insights.html', 'cxo': 'cxo.html', 'white-papers': 'white-papers.html',
           'videos': 'videos.html', 'events': 'events.html', 'cat': 'news.html', 'brief': 'the-briefing.html',
           'brief-event': 'the-briefing.html', 'res': 'research.html', 'about': 'about.html'}

HEAD_RE = re.compile(
    r'<main class="wrap">\n  <div class="crumb">.*?</div>\n  <h1 class="ptitle">(?P<t>.*?)</h1>\n'
    r'  <p class="pdesc">(?P<d>.*?)</p>\n(?:  (?P<topics><div class="topics">.*?</div>)\n)?', re.S)


def nav_for(page):
    tab = TAB_FOR.get(page)
    n = NAV_UP
    if tab:
        n = n.replace(f'href="{tab}"', f'href="{tab}" aria-current="page"', 1)
        n = re.sub(r'<a( class="(f-b|f-r)")? href="' + re.escape(tab) + '" aria-current="page">',
                   lambda m: f'<a class="{(m.group(2) + " ") if m.group(2) else ""}on" href="{tab}" aria-current="page">', n, 1)
    return n


def band(title, desc, chips, kicker=''):
    k = f'<span class="nc-kick">{kicker}</span>' if kicker else ''
    return f'''<section class="nc-band">
  <div class="wrap">
    {k}<h1>{title}</h1>
    <p>{desc}</p>
    {chips}
  </div>
</section>

<main class="wrap nc-main">
'''


def convert(path):
    html = path.read_text()
    page = re.search(r'<body data-page="([^"]+)"', html).group(1)
    cls = re.search(r'<body[^>]*class="([^"]*)"', html)
    extra = (cls.group(1) + ' ') if cls else ''
    html = re.sub(r'<body([^>]*?)( class="[^"]*")?>', lambda m: f'<body{m.group(1)} class="{extra}cover-page cv2 cv2a cv-sub">', html, 1)
    html = html.replace('</head>', VT_STYLE + '\n</head>', 1)
    html = html.replace('<div id="site-header"></div>\n', '<div id="site-header"></div>\n\n' + COVER_HDR + '\n' + nav_for(page), 1)

    m = HEAD_RE.search(html)
    if m:
        if page == 'cat':
            me = path.name
            on = ' class="on" aria-current="page"'
            b = band(m.group('t').replace('/', '/<wbr>'), m.group('d'), '')  # topics are in the category strip above
        else:
            # no chip row under the intro (the category strip does that job), except About's two sub-pages
            b = band(m.group('t'), m.group('d'), m.group('topics') if page == 'about' else '')
        html = html[:m.start()] + b + html[m.end():]

    js = SUB_JS.replace('})();\n</script>', "  // phones: scroll the tab row so the selected tab is in view\n  const on = document.querySelector('.cv-up a.on'); if (on) on.parentElement.scrollLeft = on.offsetLeft - 16;\n})();\n</script>")
    html = re.sub(r'(<script src="shared\.js[^"]*"></script>)', lambda m: m.group(1) + '\n' + js, html, 1)
    path.write_text(html)


# D2A-only pages kept in tools/d2a (Version 2 has no equivalent): white paper download page
V = re.search(r'styles\.css\?v=(\d+)', (SRC / 'white-papers.html').read_text()).group(1)
for f in (ROOT / 'tools' / 'd2a').glob('*.html'):
    (OUT / f.name).write_text(f.read_text().replace('?v=0', '?v=' + V))
# White Paper Hub: every paper opens the download page
wp = (OUT / 'white-papers.html').read_text()
wp = wp.replace('<a class="btn red" href="#">Download free</a>', '<a class="btn red" href="white-paper.html">Download free</a>')
wp = wp.replace('<a class="wp-card" href="#">', '<a class="wp-card" href="white-paper.html">')
(OUT / 'white-papers.html').write_text(wp)

for f in sorted(OUT.glob('*.html')):
    if f.name not in ('index.html', 'article.html'):
        convert(f)

# ---- mockup bar: label this version, drop the v2-only homepage and header pickers ----
js = (OUT / 'shared.js').read_text()
js = js.replace('Mockup <b style="color:#fff">v2</b>', 'Mockup <b style="color:#fff">D2A</b>')
js = re.sub(r"\$\{page === 'home' \? `<span class=\"div\"></span><label class=\"lbl\" for=\"home-opt\".*?</select>` : ''\}\n", '', js, flags=re.S)
js = re.sub(r'    <label class="lbl" for="hdr-var".*?</select>\n', '', js, flags=re.S)
js += """

// D2A: bring back the category bar
// as a strip right under the main nav (the section tabs), on every page that has them
(function () {
  const bar = document.querySelector('.cv-sections'), cats = document.querySelector('.cats');
  if (!bar || !cats || document.body.dataset.page === 'article') return;  // no category strip on articles
  bar.after(cats);  // Next Briefing / New report carousel left out for now
  document.body.classList.add('d2a-cats');
  // homepage: the big ME mark hangs over the strip, so start the categories just to its right
  const me = document.querySelector('.cv-me'), w = cats.querySelector('.wrap');
  const fit = () => {
    w.style.paddingLeft = '';
    const a = me.getBoundingClientRect(), b = w.getBoundingClientRect();
    if (a.bottom > b.top + 4 && a.right > b.left) w.style.paddingLeft = Math.round(a.right - b.left + 14) + 'px';
  };
  fit(); addEventListener('resize', fit); addEventListener('load', fit);
})();
"""
(OUT / 'shared.js').write_text(js)
# ---- brand logos: the ME mark is the main logo, the full Mobile Europe logo heads the menu ----
ME_IMG = '<img src="../brand/me-mark.png" alt="ME" width="400" height="400">'
WORD = '<a class="cv-word-link" href="index.html" aria-label="Mobile Europe home"><img class="cv-word" src="../brand/mobile-europe-wordmark.png" alt="Mobile Europe" width="1289" height="159"></a>'
for f in OUT.glob('*.html'):
    t = f.read_text()
    # Mobile Europe wordmark to the left of the strapline
    t = re.sub(r'(<p class="cv-tag">.*?</p>)', lambda m: '<div class="cv-id">' + WORD + m.group(1) + '</div>', t, count=1)
    f.write_text(re.sub(r'(<a class="cv-me"[^>]*>)<span>ME</span>', lambda m: m.group(1) + ME_IMG, t))
js = (OUT / 'shared.js').read_text()
js = js.replace('<a href="index.html" class="mm-logo"><img src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png"',
                '<a href="index.html" class="mm-logo"><img src="../brand/mobile-europe-logo.png" width="2000" height="636"')
# About + Editorial Advisory Board: link them from the menu, footer and top links
js = js.replace("['events.html', 'events', 'Events']];", "['events.html', 'events', 'Events'], ['about.html', 'about', 'About']];", 1)
js = js.replace('<a href="#">About</a>', '<a href="about.html">About</a>').replace('<a href="#">Editorial Advisory Board</a>', '<a href="editorial-board.html">Editorial Advisory Board</a>')
js = js.replace("['members.html', 'members', 'Members area']];", "['members.html', 'members', 'Members area'], ['about.html', 'about', 'About'], ['white-paper.html', 'wp-dl', 'White paper download']];", 1)
# pop-ups (log in, subscribe/join, sales): one-line Mobile Europe logo, a little bigger
WIDE = '<img class="login-logo me-wide" src="../brand/mobile-europe-logo-wide.jpg" width="300" height="39" alt="Mobile Europe">'
js = js.replace('<img class="login-logo" src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png" alt="Mobile Europe">', WIDE)
js = js.replace('<div class="pin-inline" style="margin-bottom:8px">', WIDE + '\n      <div class="pin-inline" style="margin-bottom:8px">', 1)
(OUT / 'shared.js').write_text(js)
# ---- pinned areas: no "Pinned post" label/icon, no "Pin your … here" link; "Sponsored" label reads "Partner content" ----
for f in OUT.glob('*.html'):
    t = f.read_text()
    t = re.sub(r'<span class="pin-inline" data-pin[^>]*>[^<]*</span>', '', t)
    t = re.sub(r'\n\s*<a class="pin-cta" href="#" data-pin-cta>[^<]*</a>', '', t)
    t = re.sub(r'<a class="pin-cta" href="#" data-pin-cta>[^<]*</a>', '', t)
    t = t.replace('<span class="sp-label">Sponsored</span>', '<span class="sp-label">Partner content</span>')
    f.write_text(t)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
