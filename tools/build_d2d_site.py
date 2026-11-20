#!/usr/bin/env python3
"""Build D2D: D2A with a new menu, advisory board sidebar box, reworked articles and homepage tweaks.

Built from me-redesign-d2a/ (run tools/build_d2a_site.py first); D2A is not changed.
- Menu: no fixed category strip; a Channels tab (right of News) shows the categories on rollover/tap, as a strip like D2A's;
  Insights, CxO Zone and Videos open small sub-menus; no About tab.
- Sidebar: the "Get the newsletter" box becomes an Editorial Advisory Board box.
- Articles: label above the headline is section + one second label (e.g. INSIGHTS | INTERVIEW);
  no editor byline - a head only shows on guest articles, above the intro; continuous scroll to the next story.
- Homepage: Speaking next in a subtle box.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2a'
OUT = ROOT / 'me-redesign-d2d'
U = 'https://www.mobileeurope.co.uk/wp-content/uploads/'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

# ---- sidebar: newsletter box -> Editorial Advisory Board ----
FACES = ['2025/05/colin-advisoryboard.jpg', '2025/04/Amy-advisoryboard.png', '2025/04/anita2-advisoryboard.png',
         '2025/04/phillipe-advisoryboard.png', '2025/04/Fran-advisoryboard.png', '2025/06/terje3-advisoryboard.jpg']
BOARD_BOX = ('<a class="eb-side" href="editorial-board.html"><small>Mobile Europe</small><h4>Editorial Advisory Board</h4>'
             '<p>Senior leaders from BT, Orange, Telenor, Ericsson, Red Hat and more help shape what we cover.</p>'
             '<span class="eb-faces">' + ''.join(f'<img src="{U + f}" alt="" loading="lazy">' for f in FACES) + '<i>+6</i></span>'
             '<span class="eb-go">Meet the board →</span></a>')

for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    t = re.sub(r'<div class="nl"><h4>Get the newsletter</h4>.*?</div>', BOARD_BOX, t)
    t = re.sub(r'(<body[^>]*class=")', r'\1d2d ', t, count=1)
    t = t.replace(' – Mobile Europe mockup</title>', ' – Mobile Europe D2D mockup</title>').replace('Mobile Europe – D2A homepage mockup', 'Mobile Europe – D2D homepage mockup')
    t = re.sub(r'(styles\.css|shared\.js)\?v=\d+', r'\1?v=d2d2', t)
    f.write_text(t)

# ---- homepage ----
hp = OUT / 'index.html'
t = hp.read_text()
t = t.replace('<i>Featured</i><em>Interview</em>', '<i>This just in</i><em>Interview</em>', 1)
# "Also just in" becomes "Trending today" (with a trending icon); no "More latest news" button on the cover
TREND = '<svg class="trend-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 7h6v6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
t = t.replace('<aside class="cv-also" aria-label="Also just in">\n    <h2>Also just in</h2>', '<aside class="cv-also" aria-label="Trending today">\n    <h2>' + TREND + 'Trending today</h2>', 1)
assert 'Trending today</h2>' in t
t = re.sub(r'\n  <a class="cv-more" href="news.html">.*?</a>', '', t, count=1)
# the cover carousel comes back (taken from the Version 2 D2A template): three stories, dots, rotating every 6s
v2 = (ROOT / 'me-redesign-v2' / 'home-cover-2a.html').read_text().replace('article-cover.html', 'article.html')
more = re.findall(r'\n  <a class="cv-slide" href=.*?\n  </a>', v2, re.S)
more = [s.replace('<em>News</em>', '<em>Access</em>', 1) if 'telefonica' in s else s.replace('<em>News</em>', '<em>RAN</em>', 1) for s in more]
dots = re.search(r'\n  <div class="cv-dots".*?\n  </div>', v2, re.S).group(0)
first_end = t.index('</a>', t.index('<a class="cv-slide cur"')) + len('</a>')
t = t[:first_end] + ''.join(more) + t[first_end:]
t = t.replace('\n</section>\n\n<!-- Slim section bar -->', dots + '\n</section>\n\n<!-- Slim section bar -->', 1)
t = t.replace(' aria-label="Cover story">', ' aria-roledescription="carousel" aria-label="Cover stories">', 1)
rot = re.search(r"  const slides = \[\.\.\.document\.querySelectorAll\('\.cv-slide'\)\].*?  start\(\);\n", v2, re.S).group(0)
t = t.replace("// Cover page: reuse the site menu and search\n(function () {\n", "// Cover page: rotate cover stories; reuse the site menu and search\n(function () {\n" + rot, 1)
assert t.count('class="cv-slide') == 3 and 'cv-dots' in t and 'setInterval' in t
# headlines as indented line highlights (each line its own white band) rather than one white box
t = re.sub(r'(<span class="cv-head">.*?)<b>(.*?)</b>', r'\1<b><span>\2</span></b>', t, flags=re.S)
# the date moves under the headline (caps, like the other news dates)
t, n = re.subn(r'<time>([^<]*)</time></span><b><span>(.*?)</span></b>', r'</span><b><span>\2</span></b><time class="cv-date">\1</time>', t)
assert n == 3
h = '<h2>Bringing the best minds together in the telco space</h2>'
assert h in t
t = t.replace(h, '<div class="mh-row"><a class="mh-logo" href="the-briefing.html"><img src="../brand/me-the-briefing-logo.png" alt="ME The Briefing" width="1240" height="159"></a>' + h + '</div>', 1)
# billboard spot: the same GSMA ad as the top of the page, at the same size
sj = (OUT / 'shared.js').read_text()
ad = re.search(r'<a class="gsma-bb".*?</a>', sj, re.S).group(0)
bb = '<div class="bb-zone"><div class="ad-label">Advertisement</div><div class="ad ad-bb">Billboard (BB)<small>970×250 · GAM · 300×250 on mobile</small></div></div>'
assert bb in t
t = t.replace(bb, '<div class="bb-zone bb-lb"><div class="wrap"><div class="ad-label">Advertisement</div>\n    ' + ad + '\n  </div></div>', 1)
t = t.replace('\n      <a class="btn red" href="events.html">See all events</a>', '', 1)  # no See all events button
# Speaking next: one panel per speaker at the next Briefing (no "also speaking"), scrolling sideways with arrows
SN_JS = """// Speaking next: one panel per speaker (The Briefing and Telecoms in Focus, mixed) - event details, name, short bio, register
(function () {
  const U = 'https://www.mobileeurope.co.uk/wp-content/uploads/';
  const EV = {
    brief: { cls: 'brief', name: 'The Briefing', when: 'Tue 24 Nov · 09:30 GMT', date: '2026-11-24', title: 'AI in Network Optimisation: Finding Forgotten Revenue', href: 'briefing-event.html', cta: 'Register free' },
    tif: { cls: 'tif', name: 'Telecoms in Focus', when: 'Thu 10 Dec · Online', date: '2026-12-10', title: '2026 in focus, 2027 and beyond', href: 'events.html', cta: 'Register' }
  };
  // Briefing and Telecoms in Focus speakers, mixed
  const SP = [
    ['brief', 'Nektaria Efthymiou', 'Network Platform and Security Research Director', 'BT', '2026/10/Nektaria-Efthymiou.jpg', 'Leads BT’s research into network platforms and security.'],
    ['tif', 'Colin Bannon', 'CTO', 'BT Business', '2025/12/Colin-Bannon.jpg', 'Leads technology at BT Business and sits on our Editorial Advisory Board.'],
    ['brief', 'Andy Linham', 'Principal Strategy Manager', 'Vodafone Business', '2026/06/Andy-Linham-1024x1024.jpg', 'Shapes strategy at Vodafone Business, with a focus on enterprise networks.'],
    ['tif', 'Francesca Serravalle', 'Head of Network Monetisation Strategy', 'Vodafone', '2026/10/Francesca-Serravalle.jpg', 'Leads Vodafone’s work on turning network capability into revenue.'],
    ['brief', 'David Palmer', 'Strategy and Innovation Lead', 'Stonesthrow', '2026/11/David-Palmer-1-150x150.jpg', 'Co-founder of Pairpoint, a Vodafone and Sumitomo venture.'],
    ['tif', 'Philippe Ensarguet', 'VP Cloud & Software Engineering', 'Orange', '2025/11/Philippe-Ensarguet.jpg', 'Leads cloud and software engineering at Orange; on our Advisory Board.'],
    ['brief', 'Prasenjit Sinha', 'Head of Product', 'Anritsu', '2026/08/Prasenjit-Sinha.jpg', 'Heads product at Anritsu, this Briefing’s exclusive sponsor.'],
    ['brief', 'Brian Murray', 'Head of Marketing', 'Anritsu', '2026/08/Brian-Murray.jpg', 'Leads marketing at Anritsu and sits on our Editorial Advisory Board.'],
    ['brief', 'Larbi Belkhit', 'Principal Analyst', 'ABI Research', '2026/07/Larbi-Belkhit-1010x1024.jpg', 'Moderates, drawing on ABI Research’s analysis of networks and AI.', 'Moderator']
  ];
  const count = date => { const d = Math.max(0, Math.ceil((new Date(date + 'T09:00:00') - new Date()) / 864e5)); return d === 0 ? 'On stage <b>today</b>' : `On stage in <b>${d}</b> day${d === 1 ? '' : 's'}`; };
  document.getElementById('sn-grid').innerHTML = SP.map(([e, n, r, o, img, bio, tag]) => { const ev = EV[e]; return `
    <article class="sn ${ev.cls}">
      <div class="sn-lead"><img src="${U + img}" alt="${n}" loading="lazy"><span class="sn-count">${count(ev.date)}</span></div>
      <div class="sn-body">
        <h3 class="sn-name">${n}${tag ? ` <i class="sn-tag">${tag}</i>` : ''}</h3>
        <p class="sn-role">${r}, <em>${o}</em></p>
        <p class="sn-bio">${bio}</p>
        <div class="sn-evbox"><small class="sn-ev">${ev.name} · ${ev.when}</small><p class="sn-evt">${ev.title}</p></div>
        <a class="btn white" href="${ev.href}">${ev.cta}</a>
      </div>
    </article>`; }).join('');
})();
"""
a = t.index('// Speaking next: one lead speaker per event')
b = t.index('  });\n})();\n', a) + len('  });\n})();\n')
t = t[:a] + SN_JS + t[b:]
t = t.replace('<div class="cv-minds-hd">\n      <div>', '<div class="cv-minds-hd">\n      <div>', 1)
hd_end = t.index('</div>', t.index('<div class="mh-row">')) + len('</div>')
hd_end = t.index('</div>', hd_end) + len('</div>')   # close the heading block
t = t[:hd_end] + '\n      <div class="sn-nav"><button type="button" class="sn-prev" aria-label="Previous speakers">‹</button><button type="button" class="sn-next" aria-label="Next speakers">›</button></div>' + t[hd_end:]
# Trending today: more stories, gently scrolling up one at a time
TR_MORE = [('article.html?s=telefonica', '19 Nov', 'Telefónica Deutschland expands fibre broadband reach via Deutsche Glasfaser deal'),
           ('article.html?s=nokia', '18 Nov', 'VodafoneThree, Nokia partner to trial AI-powered mobile networks'),
           ('article.html', '17 Nov', 'Orange Jordan replaces 17-year-old billing platform with Ericsson system'),
           ('article.html', '16 Nov', 'MTN exits Syrian market as Zain prepares to take over')]
a = t.index('Trending today</h2>') + len('Trending today</h2>'); b = t.index('</aside>', a)
items = t[a:b].rstrip() + ''.join(f'\n      <a href="{h}"><time>{d}</time>{x}</a>' for h, d, x in TR_MORE)
t = t[:a] + '\n    <div class="tr-view"><div class="tr-list">' + items + '\n    </div></div>\n  ' + t[b:]
t = t.replace('</body>', """<script>
// Speaking next: panels scroll sideways (arrows, swipe, gentle auto-advance that pauses on hover)
(function () {
  const g = document.getElementById('sn-grid'), box = document.querySelector('.cv-minds'); if (!g) return;
  const step = () => { const c = g.querySelector('.sn'); return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(g).columnGap || 18) : g.clientWidth; };
  const go = dir => { const end = g.scrollLeft + g.clientWidth >= g.scrollWidth - 4; g.scrollTo({ left: dir > 0 && end ? 0 : g.scrollLeft + dir * step(), behavior: 'smooth' }); };
  box.querySelector('.sn-prev').addEventListener('click', () => go(-1));
  box.querySelector('.sn-next').addEventListener('click', () => go(1));
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) setInterval(() => { if (!box.matches(':hover, :focus-within')) go(1); }, 8000);
})();
// Trending today: the list scrolls up slowly and continuously
(function () {
  const view = document.querySelector('.tr-view'), list = view && view.querySelector('.tr-list'); if (!list) return;
  const size = () => { const hs = [...list.children].map(a => a.offsetHeight); view.style.height = Math.round(hs.slice(0, 3).reduce((s, x) => s + x, 0)) + 'px'; };
  size(); addEventListener('load', size); addEventListener('resize', size);
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const SPEED = 14;   // pixels per second
  let y = 0, last = performance.now(), hold = false;
  const move = dy => {
    if (!view.offsetParent) return;                    // hidden (e.g. on phones): do nothing
    if (!view.offsetHeight) size();                     // shown again after being hidden: measure it now
    if (!list.firstElementChild.offsetHeight) return;
    y += dy;
    // stories that go off the top rejoin at the bottom (and the other way when scrolling back); capped so it can never loop forever
    for (let i = 0; i < 20 && y >= list.firstElementChild.offsetHeight; i++) { y -= list.firstElementChild.offsetHeight; list.append(list.firstElementChild); }
    for (let i = 0; i < 20 && y < 0; i++) { const l = list.lastElementChild; list.prepend(l); y += l.offsetHeight; }
    if (y < 0 || y > view.offsetHeight) y = 0;
    list.style.transform = `translateY(${-y.toFixed(2)}px)`;
  };
  // hover: stop, and the mouse wheel / trackpad scrolls the list by hand
  view.addEventListener('mouseenter', () => { hold = true; });
  view.addEventListener('mouseleave', () => { hold = false; last = performance.now(); });
  view.addEventListener('focusin', () => { hold = true; });
  view.addEventListener('focusout', () => { hold = false; last = performance.now(); });
  view.addEventListener('wheel', e => { e.preventDefault(); move(e.deltaY * (e.deltaMode === 1 ? 16 : 1) * .6); }, { passive: false });
  setInterval(() => { const now = performance.now(), dt = Math.min(now - last, 100) / 1000; last = now; if (!hold && !still) move(SPEED * dt); }, 30);
})();
</script>
</body>""", 1)
# swap the two Speaking next lines: the strapline goes small on top, "Speaking next" sits beside the logo
t = t.replace('<span class="kicker">Speaking next</span>', '<span class="kicker">Bringing the best minds together in the telco space</span>', 1)
t = t.replace('<h2>Bringing the best minds together in the telco space</h2></div>', '<h2>Speaking next</h2></div>', 1)
assert '<h2>Speaking next</h2>' in t
hp.write_text(t)

# ---- article ----
ap = OUT / 'article.html'
t = ap.read_text()
GUESTS = {
    'redhat': {'img': U + '2025/03/Orange-poland-AdobeStock_833458545.jpeg', 'chip': 'Insights', 'label': 'Comment', 'date': '14 Nov 2026',
               'tab': 'insights.html', 'title': 'Telcos need an open platform to put AI to work across the network',
               'stand': 'Operators have no shortage of AI pilots. Turning them into everyday network operations is the harder part.',
               'guest': {'name': 'Fran Heeran', 'role': 'Vice President, Global Telecommunications Business, Red Hat', 'img': '2025/04/Fran-advisoryboard.png',
                         'bio': 'Fran Heeran leads Red Hat’s global telecoms business, with 25 years in telecoms including senior roles at Nokia and Vodafone Group.'}},
    'stl': {'img': U + '2026/10/Pusant-.png', 'chip': 'Insights', 'label': 'Comment', 'date': '12 Nov 2026',
            'tab': 'insights.html', 'title': 'Five questions operators should ask before scaling AI',
            'stand': 'Moving AI from trials into the core of the business raises questions about data, skills and returns.',
            'guest': {'name': 'Amy Cameron', 'role': 'Managing Director, Research, STL Partners', 'img': '2025/04/Amy-advisoryboard.png',
                      'bio': 'Amy Cameron leads research at STL Partners, the telecoms research and consulting firm.'}},
}
t = t.replace('const STORIES = {', 'const STORIES = window.ME_STORIES = {', 1)
i = t.index('const STORIES = window.ME_STORIES = {'); j = t.index('};', i)
t = t[:j] + ''.join(f', "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in GUESTS.items()) + t[j:]
t = t.replace("'Editor · ' + s.date", 's.date')
t = t.replace("' – Mobile Europe mockup'", "' – Mobile Europe D2D mockup'")
t = t.replace('<i>Featured</i>', '<i>Insights</i>', 1)
# no editor byline: date, read time and share only; it sits above the intro (a head shows only for guest authors)
t = re.sub(r'\n        <img src="[^"]*Jasdip[^"]*" alt="">\n        <div><b>By <a href="#">Jasdip Sensi</a></b><span>Editor · ', '\n        <div><span>', t, count=1)
by = re.search(r'\n      <div class="byline">.*?\n      </div>\n', t, re.S).group(0)
t = t.replace(by, '\n', 1)
t = t.replace('\n      <p class="standfirst">', by.rstrip('\n') + '\n      <p class="standfirst">', 1)
P = {
    'stand': re.search(r'<p class="standfirst">(.*?)</p>', t).group(1),
    'tags': re.search(r'<div class="art-tags">(.*?)</div>', t).group(1),
    'body': re.search(r'<div class="art-body">(.*?)\n      </div>\n', t, re.S).group(1),
    'topics': re.search(r'<div class="art-topics">.*?</div>', t).group(0),
}
ART_JS = r"""<script>
// D2D article: section + one second label above the headline, a head only on guest articles,
// and continuous scroll: the next story loads underneath as you reach the end of this one
(function () {
  const S = window.ME_STORIES, U = 'https://www.mobileeurope.co.uk/wp-content/uploads/';
  const P = __P__;
  const SEC = { 'news.html': 'News', 'insights.html': 'Insights', 'cxo.html': 'CxO Zone' };
  const SECOND = {
    pulsant: ['Interview', 'insights.html'], redhat: ['Comment', 'insights.html'], stl: ['Comment', 'insights.html'],
    telefonica: ['Access', 'category-access.html'], nokia: ['RAN', 'category-ran.html'],
    orange: ['Financial/Regulation', 'category-financial-regulation.html'], ses: ['Satellite', 'category-satellite.html'], belgium: ['RAN', 'category-ran.html']
  };
  const TOPIC = {
    pulsant: ['Cloud/NFV', 'category-cloud-nfv.html'], redhat: ['Cloud/NFV', 'category-cloud-nfv.html'], stl: ['Automation/AI', 'category-automation-ai.html'],
    telefonica: ['Access', 'category-access.html'], nokia: ['RAN', 'category-ran.html'], orange: ['Financial/Regulation', 'category-financial-regulation.html'],
    ses: ['Satellite', 'category-satellite.html'], belgium: ['RAN', 'category-ran.html']
  };
  const ORDER = ['pulsant', 'redhat', 'telefonica', 'nokia', 'stl', 'orange', 'ses', 'belgium'];
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const long = d => d.replace('Nov', 'November').replace('Oct', 'October');
  const SHARE = document.querySelector('.byline .share').outerHTML;

  function fill(hero, lay, key) {
    const s = S[key], [lab, labHref] = SECOND[key], g = s.guest, pul = key === 'pulsant';
    hero.style.setProperty('--img', `url(${s.img})`);
    hero.querySelector('.ac-title').textContent = s.title;
    const m = hero.querySelector('.cv-meta');
    m.querySelector('i').textContent = SEC[s.tab];
    const em = m.querySelector('em'); em.className = 'ac-trail'; em.removeAttribute('aria-label');
    em.innerHTML = `<a href="${labHref}">${esc(lab)}</a>`;
    m.querySelector('time').textContent = s.date;
    let cap = hero.querySelector('.ac-cap');
    if (s.cap) { if (!cap) { cap = document.createElement('p'); cap.className = 'ac-cap'; hero.append(cap); } cap.textContent = s.cap; } else if (cap) cap.remove();
    lay.querySelector('.art-tags').innerHTML = pul ? P.tags : `<a href="${s.tab}">${SEC[s.tab]}</a><a href="${labHref}">${esc(lab)}</a>`;
    lay.querySelector('.standfirst').innerHTML = pul ? P.stand : esc(s.stand);
    lay.querySelector('.art-body').innerHTML = pul ? P.body : `<p class="ac-note">Mockup: the full ${g ? 'guest article' : 'story'} text goes here, laid out like the Pulsant interview.</p>`;
    const read = pul ? '4 min read' : g ? '5 min read' : '2 min read', by = lay.querySelector('.byline');
    by.innerHTML = (g ? `<img src="${U + g.img}" alt=""><div><b>By <a href="#">${esc(g.name)}</a></b><span>${esc(g.role)}</span><span>${long(s.date)} · ${read}</span></div>`
                      : `<div><span>${long(s.date)} · ${read}</span></div>`) + SHARE;
    by.classList.toggle('by-guest', !!g);
    lay.querySelector('.art-foot').innerHTML = (pul ? P.topics : '') +
      (g ? `<div class="author-box"><img src="${U + g.img}" alt=""><div><small>About the author</small><b>${esc(g.name)}</b><p>${esc(g.bio)}</p></div></div>` : '');
    const bm = lay.querySelector('.bm-art'); if (bm) bm.dataset.bm = 'article:' + key;
  }

  const q = new URLSearchParams(location.search).get('s'), key0 = S[q] && SECOND[q] ? q : 'pulsant';
  const hero0 = document.querySelector('.ac-hero'), lay0 = document.querySelector('.ac-layout');
  const heroT = hero0.cloneNode(true), layT = lay0.cloneNode(true);
  heroT.removeAttribute('style');
  fill(hero0, lay0, key0);
  document.querySelectorAll('.stk-tabs a').forEach(a => a.classList.toggle('on', a.getAttribute('href') === S[key0].tab));

  // schema.org breadcrumb for Google (Home > Section > Topic > Story)
  const base = location.href.replace(/[^/]*$/, ''), s0 = S[key0], [topic, topicHref] = TOPIC[key0];
  const ld = document.createElement('script'); ld.type = 'application/ld+json';
  ld.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: base + 'index.html' },
    { '@type': 'ListItem', position: 2, name: SEC[s0.tab], item: base + s0.tab },
    { '@type': 'ListItem', position: 3, name: topic, item: base + topicHref },
    { '@type': 'ListItem', position: 4, name: s0.title }
  ] });
  document.head.appendChild(ld);

  // continuous scroll; "In related news" moves below the chain
  const main = lay0.closest('main');
  const nx = document.createElement('div'); nx.className = 'nx'; main.after(nx);
  const rel = document.createElement('div'); rel.className = 'wrap nx-rel';
  [...main.children].filter(el => el !== lay0).forEach(el => rel.append(el)); nx.after(rel);
  const i0 = ORDER.indexOf(key0), queue = ORDER.slice(i0 + 1).concat(ORDER.slice(0, i0));
  const arts = [{ key: key0, el: hero0 }];
  const sentinel = document.createElement('div'); nx.append(sentinel);
  const addNext = () => {
    const key = queue.shift();
    if (!key) { io.disconnect(); sentinel.remove(); return; }
    const box = document.createElement('div'); box.className = 'nx-art'; box.dataset.s = key;
    box.innerHTML = '<div class="wrap nx-label"><span>Next article</span></div>';
    const h = heroT.cloneNode(true), l = layT.cloneNode(true), w = document.createElement('div');
    w.className = 'wrap'; w.append(l); box.append(h, w); sentinel.before(box);
    fill(h, l, key); arts.push({ key, el: h });
  };
  const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) addNext(); }, { rootMargin: '0px 0px 900px 0px' });
  io.observe(sentinel);
  window.ME_NEXT = addNext;  // mockup testing hook

  // the address bar, page title and section tab follow the story you are reading
  let cur = key0, busy = false;
  addEventListener('scroll', () => {
    if (queue.length && sentinel.isConnected && sentinel.getBoundingClientRect().top < innerHeight + 900) addNext();
    if (busy) return; busy = true;
    requestAnimationFrame(() => {
      busy = false;
      let k = arts[0].key;
      for (const a of arts) if (a.el.getBoundingClientRect().top < innerHeight * .4) k = a.key;
      if (k === cur) return;
      cur = k; const s = S[k];
      history.replaceState(null, '', '?s=' + k);
      document.title = s.title + ' – Mobile Europe D2D mockup';
      document.querySelectorAll('.cv-up a, .stk-tabs a').forEach(a => a.classList.toggle('on', a.getAttribute('href') === s.tab));
    });
  }, { passive: true });
})();
</script>
""".replace('__P__', json.dumps(P, ensure_ascii=False))
a = t.index('<script>\n(function () {\n  const SECTIONS'); b = t.index('</script>\n', a) + len('</script>\n')
t = t[:a] + ART_JS + t[b:]
ap.write_text(t)

# ---- shared.js: no category strip; Channels tab and rollover menus ----
js = (OUT / 'shared.js').read_text()
js, n = re.subn(r'\n// D2A: bring back the category bar.*?\n\}\)\(\);\n', '\n', js, count=1, flags=re.S)
assert n == 1
js += r"""

// D2D: Channels tab (the categories) and section strips for Channels, Insights, CxO Zone and Videos
(function () {
  const nav = document.querySelector('.cv-sections'); if (!nav) return;
  const row = nav.querySelector('.wrap'), page = document.body.dataset.page;
  const about = row.querySelector('a[href="about.html"]'); if (about) about.remove();
  const news = row.querySelector('a[href="news.html"]');
  const topics = document.createElement('a');
  topics.href = 'channels.html'; topics.textContent = 'Channels'; topics.dataset.dd = 'topics';
  news.after(topics);
  if (page === 'cat' || page === 'topics') { news.classList.remove('on'); news.removeAttribute('aria-current'); topics.classList.add('on'); }
  const href = window.ME_CAT_HREF;
  const CATS = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge', 'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability'];
  const MENUS = {
    topics: [['channels.html', 'All']].concat(CATS.map(c => [href(c), c])),
    insights: [['insights.html', 'All'], ['insights.html?f=partner', 'Partner content'], ['insights.html?f=interviews', 'Interviews'], ['insights.html?f=analysis', 'Analysis']],
    cxo: [['cxo.html', 'CxO News'], ['#', 'CTO of the Year Awards'], ['#', 'CTO of the Year Hall of Fame']],
    videos: [['videos.html', 'All'], ['videos.html?f=mwc', 'MWC']]
  };
  [['insights.html', 'insights'], ['cxo.html', 'cxo'], ['videos.html', 'videos']].forEach(([h, k]) => { const a = row.querySelector(`a[href="${h}"]`); if (a) a.dataset.dd = k; });

  // no rollovers: a section's strip (styled exactly like the D2A category strip) shows only on that
  // section's own pages - Channels (with All) and the category pages, Insights, CxO Zone and Videos
  const base = page === 'article' ? null : row.querySelector('a.on[data-dd]');
  if (!base) return;
  document.body.classList.add('d2a-cats');
  const here = (location.pathname.split('/').pop() || 'index.html') + location.search;
  const esc = s => s.replace(/&/g, '&amp;');
  let strip = document.querySelector('.cats');
  if (!strip) { strip = document.createElement('div'); strip.className = 'cats'; strip.innerHTML = '<div class="wrap"></div>'; }
  strip.classList.add('dd'); strip.hidden = false; nav.after(strip);
  const w = strip.querySelector('.wrap'), me = document.querySelector('.cv-me');
  w.innerHTML = MENUS[base.dataset.dd].map(([h, l]) => `<a href="${h}"${h === here ? ' class="on" aria-current="page"' : ''}>${esc(l)}</a>`).join('');
  // as on D2A: where the big ME mark hangs over the strip, start the links just to its right
  const fit = () => {
    w.style.paddingLeft = '';
    if (me) { const a = me.getBoundingClientRect(), b = w.getBoundingClientRect(); if (a.bottom > b.top + 4 && a.right > b.left) w.style.paddingLeft = Math.round(a.right - b.left + 14) + 'px'; }
  };
  fit(); addEventListener('resize', fit); addEventListener('load', fit);
})();
"""
# mockup bar: Channels page in the page list; the version switch falls back to News elsewhere (D2D-only page)
js = js.replace("['news.html', 'news', 'News'], ['insights.html', 'insights', 'Insights'], ['cxo.html', 'cxo', 'CxO Zone'], ['white-papers.html', 'white-papers', 'White Paper Hub'], ['videos.html', 'videos', 'Videos'], ['events.html', 'events', 'Events'], ['category-5g.html'",
                "['news.html', 'news', 'News'], ['channels.html', 'topics', 'Channels'], ['insights.html', 'insights', 'Insights'], ['cxo.html', 'cxo', 'CxO Zone'], ['white-papers.html', 'white-papers', 'White Paper Hub'], ['videos.html', 'videos', 'Videos'], ['events.html', 'events', 'Events'], ['category-5g.html'", 1)
js = js.replace("    if (/^me-redesign(-d2c)?$/.test(sel.value) && ONLY_NEW.includes(file)) file = 'index.html';",
                "    if (/^me-redesign(-d2c)?$/.test(sel.value) && ONLY_NEW.includes(file)) file = 'index.html';\n    if (file === 'channels.html' && !/d2[de]$/.test(sel.value)) file = 'news.html';", 1)
assert "['channels.html', 'topics', 'Channels']" in js and "file === 'channels.html'" in js
js += r"""

// D2D: on the homepage, News, Channels and category pages the label on a story picture opens its channel
// (red on rollover); clicking anywhere else on the card still opens the story
(function () {
  if (!['home', 'news', 'cat', 'topics'].includes(document.body.dataset.page)) return;
  const href = window.ME_CAT_HREF;
  const CATS = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge', 'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability'];
  const OTHER = { 'Insights': 'insights.html', 'Interview': 'insights.html?f=interviews', 'Analysis': 'insights.html?f=analysis', 'Opinion': 'insights.html', 'CXO': 'cxo.html' };
  document.querySelectorAll('.pic .tag').forEach(tag => {
    const name = tag.textContent.trim(), sec = tag.closest('.tp-sec');
    // on the Channels page a label that isn't a channel (e.g. a region) opens that section's channel
    const to = CATS.includes(name) ? href(name) : OTHER[name] || (sec && sec.querySelector('.sh a').getAttribute('href'));
    if (!to) return;
    tag.dataset.href = to; tag.classList.add('tag-link'); tag.title = 'More ' + name;
  });
  document.addEventListener('click', e => {
    const tag = e.target.closest('.tag-link'); if (!tag) return;
    e.preventDefault(); e.stopPropagation(); location.href = tag.dataset.href;
  }, true);
})();
"""
js += r"""

// D2D: once the tabs scroll out of view, a slim copy sticks to the top of the window with a small ME logo
(function () {
  const nav = document.querySelector('.cv-sections'); if (!nav) return;
  if (['brief', 'brief-event', 'res'].includes(document.body.dataset.page)) return;  // not on The Briefing / Research pages
  const bar = document.createElement('div'); bar.className = 'stk';
  bar.innerHTML = `<div class="wrap stk-in"><a class="stk-me" href="index.html" aria-label="Mobile Europe home"><img src="../brand/me-mark.png" alt="" width="400" height="400"></a><nav class="stk-tabs" aria-label="Sections">${nav.querySelector('.wrap').innerHTML}</nav></div>`;
  bar.querySelectorAll('[aria-current]').forEach(a => a.removeAttribute('aria-current'));
  bar.querySelectorAll('[data-dd]').forEach(a => { a.removeAttribute('data-dd'); a.removeAttribute('aria-haspopup'); a.removeAttribute('aria-expanded'); });
  document.body.append(bar);
  const upd = () => { const on = nav.getBoundingClientRect().bottom < 0; bar.classList.toggle('on', on); bar.inert = !on; };
  addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
  const on = bar.querySelector('.stk-tabs a.on'); if (on) on.parentElement.scrollLeft = on.offsetLeft - 16;
})();
"""
js += r"""

// D2D: Insights and Videos sub-sections (?f=...) show just those stories from the page
(function () {
  const page = document.body.dataset.page, f = new URLSearchParams(location.search).get('f');
  const tag = c => { const t = c.querySelector('.tag'); return t ? t.textContent.trim() : ''; };
  const DEF = {
    insights: {
      partner: ['Partner content', c => c.classList.contains('sp-card'), 'Expert views and case studies from our partners across the telecoms industry.'],
      interviews: ['Interviews', c => tag(c) === 'Interview', 'In-depth conversations with the leaders shaping EMEA telecoms.'],
      analysis: ['Analysis', c => tag(c) === 'Analysis', 'Our take on the deals, strategies and trends behind the headlines.']
    },
    videos: { mwc: ['MWC', c => /^MWC/.test(tag(c)), 'Interviews and briefings filmed at MWC Barcelona.'] }
  };
  const d = DEF[page] && DEF[page][f]; if (!d) return;
  const [label, test, desc] = d;
  // as on the channel pages, the selected sub-section becomes the page headline
  const band = document.querySelector('.nc-band');
  if (band) { band.querySelector('h1').textContent = label; const p = band.querySelector('p'); if (p) p.textContent = desc; }
  const lead = document.querySelector('main .top-story, main .vid-hero');
  if (lead && !test(lead)) lead.remove();
  const grids = [...document.querySelectorAll('main .grid2, main .grid3, main .grid4, main .vid-grid')];
  const cards = [...document.querySelectorAll('main a.card, main a.vid-card')];
  cards.forEach(c => { if (test(c)) grids[0].append(c); else c.remove(); });
  document.querySelectorAll('main .pin-slot').forEach(s => { if (!s.children.length) s.remove(); });
  const h = document.querySelector('main .sh h2'); if (h) h.textContent = label;
  if (!grids[0].children.length) grids[0].insertAdjacentHTML('beforeend', '<p class="ac-note">Nothing here yet.</p>');
  // the second block of stories is now empty: drop it with its billboard
  grids.slice(1).forEach(g => { if (g.children.length) return; const m = g.closest('main'); const bb = m && m.previousElementSibling; if (bb && bb.classList.contains('bb-zone')) bb.remove(); if (m) m.remove(); });
  document.title = label + ' – ' + document.title;
})();
"""
(OUT / 'shared.js').write_text(js)

# ---- Channels homepage: the latest three stories from every channel ----
CAT_NAMES = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge',
             'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability']
cat_href = lambda c: 'category-5g.html' if c == '5G & Beyond' else 'category-' + re.sub(r'[/ ]+', '-', c.lower().replace(' & ', '-')) + '.html'
secs = []
for c in CAT_NAMES:
    cards = re.findall(r'<a class="card" href="[^"]*">.*?</a>', (OUT / cat_href(c)).read_text(), re.S)[:3]
    name = c.replace('&', '&amp;')
    joined = '\n          '.join(cards)
    secs.append(f'''      <section class="tp-sec">
        <div class="sh"><h2>{name}</h2><a href="{cat_href(c)}">View all</a></div>
        <div class="grid3">
          {joined}
        </div>
      </section>''')
news = (OUT / 'news.html').read_text()
a = news.index('<main class="wrap nc-main">'); b = news.index('<div id="site-footer">')
rail = re.search(r'<aside class="rail"><div class="sticky">.*?</div></aside>', news[a:b], re.S).group(0)
tp = news[:a] + '<main class="wrap nc-main tp-main">\n  <div class="with-rail">\n    <div>\n' + '\n'.join(secs) + '\n    </div>\n    ' + rail + '\n  </div>\n</main>\n\n' + news[b:]
tp = tp.replace('<body data-page="news"', '<body data-page="topics"', 1)
tp = tp.replace('<title>News – ', '<title>Channels – ', 1)
tp = tp.replace('<h1>News</h1>\n    <p>The latest communications infrastructure and digital services news from across Europe, the Middle East and Africa.</p>',
                '<h1>Channels</h1>\n    <p>The latest from every area we cover, from RAN and optical networks to AI, security and sustainability.</p>', 1)
tp = tp.replace('<a class="on" href="news.html" aria-current="page">', '<a href="news.html">', 1)
assert 'data-page="topics"' in tp and '<h1>Channels</h1>' in tp
(OUT / 'channels.html').write_text(tp)

# ---- styles (D2D only) ----
CSS = r"""

/* ===================== D2D ===================== */
/* section strip (Channels, categories, Insights, CxO Zone, Videos pages only), exactly like the D2A category strip */
.d2d .cats.dd[hidden]{display:none}
.tp-sec + .tp-sec{margin-top:40px}
/* Speaking next: panels in a sideways-scrolling row (two in view on wide screens, one on smaller ones) */
.d2d .sn-grid{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:calc((100% - 18px) / 2);column-gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain}
.d2d .sn-grid::-webkit-scrollbar{display:none}
.d2d .sn-grid > .sn{scroll-snap-align:start;min-width:0}
.d2d .sn-also{flex-wrap:wrap;row-gap:6px}
@media (max-width:1100px){.d2d .sn-grid{grid-auto-columns:100%}}
.d2d .sn-nav{display:flex;gap:8px;flex:none}
.d2d .sn-nav button{width:40px;height:40px;border-radius:50%;border:1.5px solid var(--ink);background:#fff;color:var(--ink);font:400 26px/1 var(--body);cursor:pointer;display:grid;place-items:center;padding:0 0 3px;transition:background .15s,color .15s}
.d2d .sn-nav button:hover{background:var(--ink);color:#fff}
.d2d .cv-minds-hd{align-items:center}
@media (max-width:760px){.d2d .cv-minds-hd{flex-direction:row;align-items:flex-start}.d2d .sn-nav button{width:34px;height:34px;font-size:22px}}
.d2d .sn-body{gap:0;align-self:stretch}
.d2d .sn-ev{font-size:10.5px;letter-spacing:.12em;color:#f3a6cc}
.d2d .sn-evbox{width:100%;border-top:1px solid rgba(255,255,255,.18);padding-top:10px;margin:auto 0 14px}
.d2d .sn-evt{font:500 13px/1.35 var(--body);color:#d9dbee;margin-top:4px;min-height:2.7em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.d2d .sn-name{font-size:23px;line-height:1.15;margin-top:0}
.d2d .sn-tag{font:700 10px/1 var(--body);font-style:normal;letter-spacing:.1em;text-transform:uppercase;background:var(--brief-pink);color:#fff;padding:4px 6px 3px;border-radius:3px;vertical-align:4px;margin-left:6px}
.d2d .sn-role{margin-top:4px}
.d2d .sn-bio{font-size:13.5px;line-height:1.5;color:#c9cbe0;margin:8px 0 12px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.d2d .sn-body .btn{margin-top:0}
/* the photo runs the full height of the panel, so the button sits level with its bottom edge */
.d2d .sn-grid .sn-lead{aspect-ratio:auto;align-self:stretch;min-height:200px}
.d2d .sn-grid .sn-lead img{position:absolute;inset:0}
@media (max-width:760px){.d2d .sn-grid .sn-lead{align-self:start;aspect-ratio:1;min-height:0}}
@media (max-width:760px){.d2d .sn-name{font-size:19px}.d2d .sn-bio{-webkit-line-clamp:3}}
/* Trending today: three stories in view, moving up one at a time */
.d2d .tr-view{overflow:hidden}
.d2d .tr-list{will-change:transform}
.d2d .tr-list a{box-sizing:border-box;display:block!important}
/* more room between the stories and the advert column, split by a thin grey keyline */
@media (min-width:901px){
  .d2d .with-rail{column-gap:60px}
  .d2d .with-rail > .rail{align-self:stretch;position:relative}
  .d2d .with-rail > .rail::before{content:"";position:absolute;left:-30px;top:0;bottom:0;border-left:1px solid #dddcd8}
}
/* homepage cover: Trending today panel, smaller second label, headline sits lower (no More latest news button) */
.d2d .cv-also h2{display:flex;align-items:center;gap:7px;color:var(--me)}
.d2d.cv2 .cv-also{width:236px}
@media (max-width:1100px){.d2d.cv2 .cv-also{width:210px}}
.d2d .cv-also .trend-ico{width:14px;height:14px;flex:none;color:#fff}
/* headline: each line gets its own white band, ragged on the right */
.d2d.cv2 .cv-head b{background:none;padding:0;line-height:1.2}
.d2d.cv2 .cv-head b span{background:#fff;color:var(--ink);padding:4px 14px 5px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
/* cover picture grows a little on rollover */
.d2d .cv-slide{background:none}
.d2d .cv-slide::before{content:"";position:absolute;inset:0;background:var(--img) center 35%/cover no-repeat #222;transition:transform .7s ease}
.d2d .cv-slide:hover::before{transform:scale(1.05)}
@media (prefers-reduced-motion:reduce){.d2d .cv-slide::before{transition:none}}
@media (max-width:760px){.d2d.cv2 .cv-dots{top:14px;bottom:auto}}
.d2d .cv-head em{display:flex;align-items:center;font-size:12px;line-height:1;letter-spacing:.08em;padding:6px 10px 8px}
/* capitals sit low in their line box: a little less room on top so the labels look centred */
.d2d .cv-head .cv-meta i{padding:6px 10px 8px}
/* rollover: headline (and Trending today links) turn red instead of underlining */
.d2d .cv-slide:hover .cv-head b{text-decoration:none}
.d2d .cv-slide .cv-head b span{transition:color .15s}
.d2d .cv-slide:hover .cv-head b span{color:var(--me)}
.d2d .cv-also a{transition:color .15s}
.d2d .cv-also a:hover{text-decoration:none;color:#ff5c7c}
.d2d.cv2 .cv-head{max-width:440px}
.d2d.cv2 .cv-head{bottom:104px}
.d2d .cv-date{display:block;background:#fff;color:var(--muted);font:600 12px var(--body);letter-spacing:.1em;text-transform:uppercase;padding:4px 14px 10px}
/* soft blurred tint along the bottom of the cover picture, behind the tabs, so they read the same on any photo */
.d2d .cv-hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:78px;z-index:2;pointer-events:none;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.32));backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);-webkit-mask-image:linear-gradient(transparent,#000 55%);mask-image:linear-gradient(transparent,#000 55%)}
@media (max-width:760px){.d2d .cv-head em,.d2d .cv-head .cv-meta i{padding:5px 8px 6px}.d2d.cv2 .cv-head{bottom:62px;max-width:none}.d2d .cv-hero::after{height:62px}.d2d .cv-head em{font-size:11px}}
/* The Briefing and Independent Research pages: only their two tabs, which sit up in the header where Subscribe / Log in were (desktop);
   the main Briefing and Research pages get a big ME mark (as on the homepage) overlapping the band, with the title level with its bottom */
.d2d:is([data-page="brief"],[data-page="brief-event"],[data-page="res"]) .cv-sections a:not(.f-b):not(.f-r){display:none}
@media (min-width:761px){
  .d2d:is([data-page="brief"],[data-page="brief-event"],[data-page="res"]) .cv-acct{display:none}
  .d2d:is([data-page="brief"],[data-page="brief-event"],[data-page="res"]) .cv-sections{position:relative;z-index:11;margin-top:-38px;background:transparent!important;border-bottom:0!important;pointer-events:none}
  .d2d:is([data-page="brief"],[data-page="brief-event"],[data-page="res"]) .cv-sections .wrap{height:38px!important;padding-top:0!important;align-items:flex-end}
  .d2d:is([data-page="brief"],[data-page="brief-event"],[data-page="res"]) .cv-sections a{pointer-events:auto;padding-top:11px!important;padding-bottom:10px!important}
}
.d2d:is([data-page="brief"],[data-page="res"]) .cv-bar{position:relative;z-index:10}
.d2d:is([data-page="brief"],[data-page="res"]) .cv-me{width:150px;height:150px;align-self:flex-start;margin:8px 0 -100px}
.d2d:is([data-page="brief"],[data-page="res"]) .cv-me:has(img){filter:drop-shadow(0 8px 18px rgba(0,0,0,.3))}
@media (min-width:761px){.d2d:is([data-page="brief"],[data-page="res"]) .fband .wrap{padding-left:194px}.d2d[data-page="brief"].cv-sub .fband .mark{width:auto}}
@media (min-width:1101px){.d2d[data-page="brief"].cv-sub .fband.brief .name{font-size:60px!important}}
/* the title's letters end level with the bottom of the big ME mark */
@media (min-width:761px){.d2d[data-page="brief"] .fband .wrap{padding-top:42px!important;padding-bottom:20px!important}.d2d[data-page="res"] .fband .wrap{padding-top:11px!important;padding-bottom:20px!important}}
@media (max-width:1100px) and (min-width:761px){.d2d:is([data-page="brief"],[data-page="res"]) .cv-me{width:120px;height:120px;margin-bottom:-70px}.d2d:is([data-page="brief"],[data-page="res"]) .fband .wrap{padding-left:164px;padding-top:16px!important}}
@media (max-width:760px){.d2d:is([data-page="brief"],[data-page="res"]) .cv-me{width:72px;height:72px;margin:6px 0 -44px}}
/* Briefing sign-up page: no top advert; the small ME tucks into the top-left of the navy bar, which moves up */
.d2d[data-page="brief-event"] .lb-zone{display:none}
@media (min-width:761px){
  .d2d[data-page="brief-event"] .cv-bar{position:relative;z-index:10}
  .d2d[data-page="brief-event"] .cv-in{min-height:58px}
  .d2d[data-page="brief-event"] .cv-me{align-self:flex-start;margin:8px 0 -18px}
  .d2d[data-page="brief-event"] .fband .wrap{padding-left:104px}
}
/* articles: more room after the big intro */
.d2d .ac-layout .standfirst{margin-bottom:34px}
/* sticky tab bar (shows once the main tabs have scrolled away) */
.stk{position:fixed;left:0;right:0;top:0;z-index:60;background:#f2f2f0;border-bottom:4px solid var(--ink);box-shadow:0 3px 12px rgba(0,0,0,.14);transform:translateY(-110%);visibility:hidden;transition:transform .22s,visibility .22s}
.stk.on{transform:none;visibility:visible}
.stk-in{display:flex;align-items:flex-end;gap:16px;height:54px}
.stk-me{align-self:center;flex:none}
.stk-me img{display:block;width:38px;height:38px}
.stk-tabs{display:flex;gap:4px;align-items:flex-end;flex:1;min-width:0;height:100%;overflow-x:auto;scrollbar-width:none}
.stk-tabs a{font:600 13.5px/1 var(--head);text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;background:var(--me);color:#fff;padding:12px 14px 10px;border-radius:0 10px 0 0;transition:background .15s,color .15s}
.stk-tabs a:hover{background:#fff;color:var(--me)}
.stk-tabs a.on{background:var(--ink);color:#fff}
.stk-tabs .f-b{margin-left:auto}
.stk-tabs .f-b,.stk-tabs .f-r{background:var(--brief-navy)}
.stk-tabs .f-b:hover,.stk-tabs .f-r:hover{background:#fff;color:var(--me)}
.tabs-grey .stk-tabs a:not(.on):not(.f-b):not(.f-r){background:#dcdcd8;color:#444}
.tabs-grey .stk-tabs a:not(.on):not(.f-b):not(.f-r):hover{background:var(--me);color:#fff}
@media (max-width:760px){.stk-in{height:46px;gap:10px}.stk-me img{width:32px;height:32px}.stk-tabs a{font-size:12.5px;padding:10px 11px 9px}}
@media (prefers-reduced-motion:reduce){.stk{transition:none}}
/* grey tabs: flat (no shadow) with grey text */
.d2d.tabs-grey .cv-sections a:not(.f-b):not(.f-r){box-shadow:none}
.d2d.tabs-grey .cv-sections a:not(.on):not(.f-b):not(.f-r):not(:hover){color:#444}
.tp-sec .sh{margin-top:0}
.tag-link{cursor:pointer;z-index:2;transition:background .15s}
.tag.tag-link:hover{background:var(--me)}
.tag.ins.tag-link:hover{background:var(--ink)}

/* sidebar: Editorial Advisory Board box (in place of the newsletter box) */
.eb-side{display:block;background:var(--ink);color:#fff;border-radius:10px;padding:20px}
.eb-side small{font:700 10.5px var(--body);letter-spacing:.12em;text-transform:uppercase;color:#ff8fa5}
.eb-side h4{font:600 22px/1.1 var(--head);text-transform:uppercase;margin-top:4px}
.eb-side p{color:#bbb;font-size:13.5px;line-height:1.45;margin:6px 0 14px}
.eb-faces{display:flex;align-items:center;padding-left:8px}
.eb-faces img,.eb-faces i{width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid var(--ink);margin-left:-8px;background:#333;flex:none}
.eb-faces i{display:grid;place-items:center;font:700 12px var(--body);font-style:normal;color:#fff;background:var(--me)}
.eb-go{display:inline-block;margin-top:14px;font:700 14px var(--body);border-bottom:2px solid var(--me);padding-bottom:2px}
.eb-side:hover .eb-go{color:#ff8fa5}

/* homepage: Speaking next in a subtle box */
.d2d .cv-minds{background:#ececea;border:1px solid #dcdcd8;border-radius:0 18px 0 18px;padding:22px 26px 28px}
.d2d .cv-minds-hd{border-top:0;padding-top:0}
.d2d .mh-row{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:6px}
.d2d .mh-logo img{display:block;height:42px;width:auto}
.d2d .mh-row h2{font-size:20px;padding-left:18px;border-left:1px solid #cfcfcb}
@media (max-width:760px){.d2d .mh-logo img{height:30px}.d2d .mh-row{gap:8px}.d2d .mh-row h2{font-size:17px;padding-left:0;border-left:0;flex-basis:100%}}
@media (max-width:760px){.d2d .cv-minds{padding:18px 14px 20px}}

/* articles: date line (no editor byline); a guest author's head sits above the intro */
.d2d .ac-layout .byline{margin:4px 0 18px}
.d2d .byline.by-guest span{display:block}
.d2d .byline.by-guest img{width:56px;height:56px}
/* continuous scroll */
.nx-art{margin-top:56px}
.nx-label{border-top:6px solid var(--ink);padding-top:10px;margin-bottom:14px}
.nx-label span{font:600 14px var(--head);letter-spacing:.1em;text-transform:uppercase;color:var(--me)}
.nx-art .ac-hero{view-transition-name:none}
.nx-rel{margin-top:40px}
"""
(OUT / 'styles.css').write_text((OUT / 'styles.css').read_text() + CSS)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
