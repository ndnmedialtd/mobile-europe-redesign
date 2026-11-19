#!/usr/bin/env python3
"""Build the D2A cover pages in me-redesign-v2 from home-cover-2.html:
home-cover-2a.html (cover homepage), article-cover.html (redesigned article)
and news-cover.html (section page with the tabs moved up).
Pages are linked with cross-document view transitions (image -> article, tabs move up)."""
import re
from pathlib import Path

V2 = Path(__file__).resolve().parent.parent / 'me-redesign-v2'
base = (V2 / 'home-cover-2.html').read_text()
U = 'https://www.mobileeurope.co.uk/wp-content/uploads/'

HOME = 'home-cover-2a.html'
VT = '''<style>
/* D2A: animate between pages (Chrome, Edge, Safari 18.2+; other browsers just load the page) */
@view-transition{navigation:auto}
</style>'''

head_end = base.index('<!-- Full-bleed cover story')
foot_start = base.index('<div id="site-footer"></div>')
head = base[:head_end].replace('href="home-cover.html"', f'href="{HOME}"')
nav = re.search(r'<!-- Slim section bar -->.*?</nav>\n', base, re.S).group(0)
nav = nav.replace('href="news.html">News', 'href="news-cover.html">News')

STORIES = {
    'pulsant': dict(img='2026/11/Rob-Coupland-ME.png', chip='Featured', label='Interview', date='11 Nov 2026', tab='insights.html',
                    title='Data centres must look beyond the ‘bragawatts’ race, says Pulsant CEO',
                    cap='Rob Coupland, CEO of Pulsant since 2019.'),
    'telefonica': dict(img='2026/11/telefonica-germany.png', chip='This just in', label='News', date='19 Nov 2026', tab='news-cover.html',
                       title='Telefónica Deutschland expands fibre broadband reach via Deutsche Glasfaser deal',
                       stand='Telefónica Deutschland is expanding its fibre broadband reach through a new partnership with Deutsche Glasfaser, giving its O2 brand access to more fibre homes across Germany.'),
    'nokia': dict(img='2026/11/Nokia-VodafoneThree.png', chip='This just in', label='News', date='18 Nov 2026', tab='news-cover.html',
                  title='VodafoneThree, Nokia partner to trial AI-powered mobile networks',
                  stand='VodafoneThree has partnered with Nokia to test how AI could help make its mobile network faster and more reliable.'),
}
ORDER = ['pulsant', 'telefonica', 'nokia']


def page(title, body_attrs, inner, script):
    h = head.replace(re.search(r'<title>.*?</title>', head).group(0), f'<title>{title} – Mobile Europe mockup</title>')
    h = h.replace('</head>', VT + '\n</head>')
    h = re.sub(r'<body[^>]*>', f'<body {body_attrs}>', h)
    return h + inner + base[foot_start:base.index('<script>', foot_start)] + script + '\n</body>\n</html>\n'


# Shared header behaviour for the secondary pages (menu, search, logged-in name)
SUB_JS = '''<script>
(function () {
  document.getElementById('cv-menu').addEventListener('click', () => document.querySelector('.mast .burger').click());
  document.getElementById('cv-search').addEventListener('click', () => {
    const p = document.getElementById('search-panel'); document.querySelector('.cv-bar').after(p); p.hidden = !p.hidden; if (!p.hidden) p.querySelector('input').focus();
  });
  const m = window.ME_MEMBER && ME_MEMBER.get();
  if (m) { const l = document.querySelector('.cv-login'); l.textContent = 'Hi, ' + m.first; l.setAttribute('href', 'members.html'); l.removeAttribute('data-login'); }
})();
</script>'''

# ---------- D2A homepage ----------
home = base.replace('href="home-cover.html"', f'href="{HOME}"')
home = home.replace('<title>Option D2 · Cover, split', '<title>Option D2A · Cover, split + transitions')
home = home.replace('class="cover-page cv2"', 'class="cover-page cv2 cv2a"')
home = home.replace('</head>', VT + '\n</head>')
slides = []
for k, key in enumerate(ORDER):
    s = STORIES[key]
    attrs = ' aria-hidden="true" tabindex="-1"' if k else ''
    slides.append(f'''  <a class="cv-slide{' cur' if not k else ''}" href="article-cover.html?s={key}" style="--img:url({U + s['img']})"{attrs}>
    <span class="cv-head"><span class="cv-meta"><i>{s['chip']}</i><em>{s['label']}</em><time>{s['date']}</time></span><b>{s['title']}</b></span>
  </a>''')
a = home.index('  <a class="cv-slide cur"')
b = home.index('  <aside class="cv-also"')
home = home[:a] + '\n'.join(slides) + '\n' + home[b:]
home = home.replace(re.search(r'<!-- Slim section bar -->.*?</nav>\n', home, re.S).group(0), nav)
home = home.replace('<a class="cv-more" href="news.html">', '<a class="cv-more" href="news-cover.html">')
(V2 / HOME).write_text(home)

# ---------- Article page ----------
art = (V2 / 'article.html').read_text()
body = re.search(r'<div class="art-body">.*?</div>\n\n      <div class="art-foot">.*?</article>', art, re.S).group(0)
body = body.replace('</article>', '')
byline = re.search(r'<div class="byline">.*?\n      </div>\n', art, re.S).group(0)
tags = re.search(r'<div class="art-tags">.*?</div>', art).group(0)
rail = re.search(r'<aside class="rail art-rail">.*?</aside>', art, re.S).group(0)
related = re.search(r'<div class="sh"><h2>In related news</h2>.*?</div>\n  <div class="grid4">.*?</div>', art, re.S).group(0)
p = STORIES['pulsant']
stand = re.search(r'<p class="standfirst">.*?</p>', art).group(0)

art_inner = f'''<!-- Secondary pages: the tabs move up under the header -->
{nav.replace('<nav class="cv-sections"', '<nav class="cv-sections cv-up"')}
<section class="ac-hero" style="--img:url({U + p['img']})" aria-label="Story image">
  <div class="ac-head">
    <span class="cv-meta"><i>{p['chip']}</i><em>{p['label']}</em><time>{p['date']}</time></span>
    <h1 class="ac-title">{p['title']}</h1>
  </div>
  <p class="ac-cap">{p['cap']}</p>
</section>

<main class="wrap">
  <div class="with-rail art-layout ac-layout">
    <article class="art">
      {tags}
      {stand}
      {byline}
      {body}
    </article>
    {rail}
  </div>

  {related}
</main>

'''
STORY_JS = 'const STORIES = ' + repr({k: {kk: (U + vv if kk == 'img' else vv) for kk, vv in v.items()} for k, v in STORIES.items()}).replace("'", '"') + ';'
art_js = SUB_JS + '''
<script>
// Swap in the story chosen on the cover (?s=), so the image and headline match the one clicked
(function () {
  ''' + STORY_JS + '''
  const key = new URLSearchParams(location.search).get('s') || 'pulsant', s = STORIES[key];
  document.querySelectorAll('.cv-up a').forEach(a => a.classList.toggle('on', a.getAttribute('href') === (s || STORIES.pulsant).tab));
  if (!s || key === 'pulsant') return;
  document.querySelector('.ac-hero').style.setProperty('--img', `url(${s.img})`);
  document.querySelector('.ac-title').textContent = s.title;
  document.title = s.title + ' – Mobile Europe mockup';
  const m = document.querySelector('.ac-head .cv-meta');
  m.querySelector('i').textContent = s.chip; m.querySelector('em').textContent = s.label; m.querySelector('time').textContent = s.date;
  document.querySelector('.ac-cap').remove();
  document.querySelector('.standfirst').textContent = s.stand;
  document.querySelector('.art-tags').innerHTML = '<a href="news-cover.html">News</a>';
  document.querySelector('.art-body').innerHTML = '<p class="ac-note">Mockup: the full story text goes here, laid out exactly like the Pulsant interview. Click the Featured cover story to see a complete article.</p>';
  document.querySelector('.art-topics').remove(); document.querySelector('.byline span').textContent = 'Editor · ' + s.date.replace('Nov', 'November') + ' · 2 min read';
})();
</script>'''
(V2 / 'article-cover.html').write_text(page(p['title'], 'data-page="article" class="cover-page cv2 cv2a cv-sub"', art_inner, art_js))

# ---------- News section page ----------
news = (V2 / 'news.html').read_text()
first_main = news[news.index('<main class="wrap">'):news.index('</main>') + 7]
topics = re.search(r'<div class="topics">.*?</div>', first_main, re.S).group(0)
content = first_main[first_main.index('  <a class="top-story"'):first_main.rindex('</main>')]
news_inner = f'''<!-- Secondary pages: the tabs move up under the header; the active tab opens into the section band -->
{nav.replace('<nav class="cv-sections"', '<nav class="cv-sections cv-up"').replace('href="news-cover.html">', 'href="news-cover.html" class="on" aria-current="page">')}
<section class="nc-band">
  <div class="wrap">
    <h1>News</h1>
    <p>The latest communications infrastructure and digital services news from across Europe, the Middle East and Africa.</p>
    {topics}
  </div>
</section>

<main class="wrap nc-main">
{content}</main>

'''
(V2 / 'news-cover.html').write_text(page('News', 'data-page="news" class="cover-page cv2 cv2a cv-sub"', news_inner, SUB_JS))
print('wrote', HOME, 'article-cover.html', 'news-cover.html')
