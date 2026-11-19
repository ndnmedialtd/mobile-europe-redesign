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
# One cover story, not a carousel: keep the first slide, drop the others, the dots and the auto-rotate
home = re.sub(r'\n  <a class="cv-slide" href=.*?\n  </a>', '', home, flags=re.S)
home = re.sub(r'\n  <div class="cv-dots".*?\n  </div>', '', home, count=1, flags=re.S)
home = home.replace('<!-- Full-bleed cover story (rotates) -->', '<!-- Full-bleed cover story -->')
home = home.replace(' aria-roledescription="carousel" aria-label="Cover stories"', ' aria-label="Cover story"', 1)
home = home.replace("  start();\n  document.getElementById('cv-menu')", "  document.getElementById('cv-menu')", 1)
# and switch the rotation code off completely (hover/leave on the cover used to restart it, which blanked the single slide)
home = re.sub(r"  const slides = \[\.\.\.document\.querySelectorAll\('\.cv-slide'\)\].*?hero\.addEventListener\('mouseleave', start\);\n", '', home, count=1, flags=re.S)
home = home.replace('// Cover page: rotate cover stories; reuse the site menu and search', '// Cover page: reuse the site menu and search', 1)
# More latest news: start the advert column level with the black rule above the heading
home = home.replace('<div class="with-rail" style="margin-top:8px">\n    <div>\n      <div class="sh"><h2>More latest news</h2>',
                    '<div class="with-rail" style="margin-top:48px">\n    <div>\n      <div class="sh" style="margin-top:0"><h2>More latest news</h2>', 1)
cut = home.index('<div id="site-footer">')
home = home[:cut] + '\n' + rest + home[cut:]
# "Also just in" (top three on the homepage): each opens its own story on the article page
U = 'https://www.mobileeurope.co.uk/wp-content/uploads/'
ALSO = {
    'orange': ('Orange pledges extra €250m to support emerging tech startups', '2022/09/Orange-Spain-Metaverse-Shop-e1666341211856-1068x661.png', '18 Nov 2026',
               'Orange has pledged an additional €250 million to its investment arm, Orange Ventures, adding to the group’s total assets under management.'),
    'ses': ('SES, ITU expand partnership to improve digital education in Africa', '2026/11/SES.png', '18 Nov 2026',
            'SES and the International Telecommunication Union are widening their partnership to bring better connectivity to schools across Africa.'),
    'belgium': ('Belgium confirms 2G shutdown plans for 2028/29', '2026/11/Belgium.png', '17 Nov 2026',
                'Belgium has confirmed that its mobile operators will switch off their 2G networks in 2028/29, freeing spectrum for newer technologies.'),
}
for key, (title, img, date, stand) in ALSO.items():
    home = home.replace(f'<a href="article.html"><time>{date[:6]}</time>{title}</a>', f'<a href="article.html?s={key}"><time>{date[:6]}</time>{title}</a>', 1)
extra = ''.join(f', "{k}": {{"img": "{U + v[1]}", "chip": "This just in", "label": "News", "date": "{v[2]}", "tab": "news.html", "title": "{v[0]}", "stand": "{v[3]}"}}' for k, v in ALSO.items())
i = article_t.index('const STORIES = {'); j = article_t.index('};', i)
article_t = article_t[:j] + extra + article_t[j:]
# Breadcrumb, the light way: the label above the headline becomes a "Section › Topic" link trail,
# plus hidden schema.org BreadcrumbList data for Google (no extra breadcrumb bar)
TRAIL_JS = """<script>
(function () {
  const SECTIONS = { 'news.html': 'News', 'insights.html': 'Insights', 'cxo.html': 'CxO Zone' };
  const TOPIC = {
    pulsant: ['insights.html', 'Cloud/NFV', 'category-cloud-nfv.html'],
    telefonica: ['news.html', 'Access', 'category-access.html'],
    nokia: ['news.html', 'RAN', 'category-ran.html'],
    orange: ['news.html', 'Financial/Regulation', 'category-financial-regulation.html'],
    ses: ['news.html', 'Satellite', 'category-satellite.html'],
    belgium: ['news.html', 'RAN', 'category-ran.html']
  };
  const key = new URLSearchParams(location.search).get('s') || 'pulsant';
  const [sec, topic, topicHref] = TOPIC[key] || TOPIC.pulsant;
  const em = document.querySelector('.ac-head .cv-meta em');
  em.classList.add('ac-trail');
  em.innerHTML = `<a href="${sec}">${SECTIONS[sec]}</a><span aria-hidden="true">›</span><a href="${topicHref}">${topic}</a>`;
  em.setAttribute('aria-label', 'Breadcrumb');
  const base = location.href.replace(/[^/]*$/, ''), title = document.querySelector('.ac-title').textContent;
  const ld = document.createElement('script'); ld.type = 'application/ld+json';
  ld.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: base + 'index.html' },
    { '@type': 'ListItem', position: 2, name: SECTIONS[sec], item: base + sec },
    { '@type': 'ListItem', position: 3, name: topic, item: base + topicHref },
    { '@type': 'ListItem', position: 4, name: title }
  ] });
  document.head.appendChild(ld);
})();
</script>
"""
article_t = article_t.replace('</body>', TRAIL_JS + '</body>', 1)
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
    if (!me) return;
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
# Bookmarks: a small "save" icon on story cards and a "Bookmark to read later" link on articles.
# Logged out it opens the log-in pop-up; logged in (test/test) it toggles saved (kept in this browser only).
js += r"""

// D2A bookmarks
(function () {
  const ICON = filled => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5h11a1 1 0 0 1 1 1v15.2a.6.6 0 0 1-1 .45L12 15.6l-5.5 4.55a.6.6 0 0 1-1-.45V4.5a1 1 0 0 1 1-1z" fill="${filled ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`;
  const KEY = 'me-saved';
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const write = a => { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} };
  const loggedIn = () => !!(window.ME_MEMBER && ME_MEMBER.get());
  const paint = (b, on) => {
    b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
    b.querySelector('.bm-ico').innerHTML = ICON(on);
    const t = b.querySelector('.bm-txt'); if (t) t.textContent = on ? 'Saved to read later' : 'Bookmark to read later';
    b.setAttribute('aria-label', on ? 'Remove bookmark' : 'Bookmark to read later');
  };
  const make = (id, withText) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = withText ? 'bm bm-art' : 'bm bm-card'; b.dataset.bm = id;
    b.innerHTML = '<span class="bm-ico"></span>' + (withText ? '<span class="bm-txt"></span>' : '');
    paint(b, loggedIn() && read().includes(id));
    return b;
  };
  // story cards (not partner content)
  document.querySelectorAll('a.card:not(.sp-card), a.lead-big, a.top-story').forEach((card, i) => {
    const img = card.querySelector('img'); if (!img) return;
    const box = card.querySelector('.pic') || img.parentElement;
    if (getComputedStyle(box).position === 'static') box.style.position = 'relative';
    const t = card.querySelector('h2, h3, h4');
    box.appendChild(make((t ? t.textContent : card.getAttribute('href') + i).trim().slice(0, 80), false));
  });
  // article: after the tags
  const tags = document.querySelector('.art-tags');
  if (tags) {
    const id = 'article:' + (new URLSearchParams(location.search).get('s') || 'pulsant');
    // same line as the tags (wraps underneath only if there are a lot of tags)
    const row = document.createElement('div'); row.className = 'art-tagrow';
    tags.before(row); row.append(tags, make(id, true));
  }
  // click: logged out -> log-in pop-up; logged in -> toggle saved
  document.addEventListener('click', e => {
    const b = e.target.closest('.bm'); if (!b) return;
    e.preventDefault(); e.stopPropagation();
    if (!loggedIn()) { const l = document.querySelector('[data-login]'); if (l) l.click(); return; }
    const a = read(), id = b.dataset.bm, i = a.indexOf(id);
    if (i > -1) a.splice(i, 1); else a.push(id);
    write(a); paint(b, i === -1);
  }, true);
})();
"""
js += r"""

// D2A: where a column opens with a black-ruled section heading, start the advert column level with that rule
(function () {
  const rows = [...document.querySelectorAll('.with-rail')].map(w => {
    const col = w.firstElementChild, rail = w.querySelector(':scope > .rail');
    const sh = col && col.firstElementChild;
    return rail && sh && sh.classList.contains('sh') ? { col, rail, sh } : null;
  }).filter(Boolean);
  const fit = () => rows.forEach(({ col, rail, sh }) => {
    rail.style.marginTop = '';
    const c = col.getBoundingClientRect(), r = rail.getBoundingClientRect();
    if (Math.abs(r.top - c.top) > 2 || r.left < c.right) return;   // only when the rail sits beside the column
    const gap = Math.round(sh.getBoundingClientRect().top - c.top);
    if (gap > 0) rail.style.marginTop = gap + 'px';
  });
  fit(); addEventListener('resize', fit); addEventListener('load', fit);
})();
"""
# Mockup bar: "Tabs: Red / Grey" switch to compare the main-nav tab styles (remembered in this browser)
nxt = '<a href="${pages[(idx + 1) % pages.length][0]}" aria-label="Next page">→</a>\n    <span class="div"></span>'
assert nxt in js
js = js.replace(nxt, nxt + '<label class="lbl" for="tab-style">Tabs</label><select id="tab-style" aria-label="Tab style"><option value="red">Red</option><option value="grey">Grey</option></select><span class="div"></span>', 1)
js += r"""

// D2A: tab style switch (mockup only)
(function () {
  let v = 'red'; try { v = localStorage.getItem('me-tabs') || 'red'; } catch (e) {}
  // The Briefing and Independent Research pages always use grey tabs, so their navy bands lead
  const fr = ['brief', 'brief-event', 'res'].includes(document.body.dataset.page);
  const apply = x => document.body.classList.toggle('tabs-grey', fr || x === 'grey');
  apply(v);
  const sel = document.getElementById('tab-style');
  if (sel) { sel.value = v; sel.addEventListener('change', () => { apply(sel.value); try { localStorage.setItem('me-tabs', sel.value); } catch (e) {} }); }
})();
"""
# Mockup bar: switch between D2A and D2B, staying on the same page
lab = '<span class="lbl" style="padding:0 6px;color:#888">Mockup <b style="color:#fff">D2A</b></span>'
assert lab in js
js = js.replace(lab, '<span class="lbl" style="padding:0 2px 0 6px;color:#888">Mockup</span><select id="ver-switch" aria-label="Mockup version"><option value="me-redesign-d2a">D2A</option><option value="me-redesign-d2b">D2B</option><option value="me-redesign-d2c">D2C</option></select><span class="div"></span>', 1)
js += r"""

// D2A / D2B version switch (mockup only): same page, other version
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
# The Briefing page: Event alerts moves out of the band to sit on the right of the intro
bp = OUT / 'the-briefing.html'
t = bp.read_text()
btn = '\n    <a class="btn pink" href="#" data-login>Event alerts</a>'
assert btn in t
t = t.replace(btn, '', 1)
t = re.sub(r'(<p class="bl-intro">.*?</p>)', lambda m: '<div class="bl-introrow">' + m.group(1) + '<a class="btn pink" href="#" data-login>Event alerts</a></div>', t, count=1, flags=re.S)
bp.write_text(t)

# Independent Research page: same treatment, New report alerts on the right of the intro
rp = OUT / 'research.html'
t = rp.read_text()
btn = '\n    <a class="btn" style="background:#fff;color:var(--res)" href="#" data-login>New report alerts</a>'
assert btn in t
t = t.replace(btn, '', 1)
t = t.replace('<div class="r-intro"><div class="wrap">', '<div class="r-intro"><div class="wrap r-introrow">', 1)
t = re.sub(r'(<div class="wrap r-introrow"><p>.*?</p>)', lambda m: m.group(1) + '<a class="btn" href="#" data-login>New report alerts</a>', t, count=1, flags=re.S)
rp.write_text(t)

# tab style switch: apply the saved choice before first paint (no red-to-grey flash)
EARLY = "<script>try{if(['brief','brief-event','res'].includes(document.body.dataset.page)||localStorage.getItem('me-tabs')==='grey')document.body.classList.add('tabs-grey')}catch(e){}</script>"
for f in OUT.glob('*.html'):
    t = f.read_text()
    if 'me-tabs' not in t:
        t = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + EARLY, t, count=1)
        f.write_text(t)

# header: "Join" reads "Subscribe"
for f in OUT.glob('*.html'):
    t = f.read_text()
    f.write_text(t.replace('<a href="#" data-subscribe>Join</a>', '<a href="#" data-subscribe>Subscribe</a>'))
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
