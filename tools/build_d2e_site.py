#!/usr/bin/env python3
"""Build D2E: D2D with the homepage tabs above the cover picture (right under the header).

Built from me-redesign-d2d/ (run tools/build_d2d_site.py first); D2D is not changed.
The big ME mark hangs over the tab row, so the tabs start just to its right.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2d'
OUT = ROOT / 'me-redesign-d2e'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    t = re.sub(r'(<body[^>]*class=")', r'\1d2e ', t, count=1)
    t = t.replace('Mobile Europe D2D mockup', 'Mobile Europe D2E mockup').replace('Mobile Europe – D2D homepage mockup', 'Mobile Europe – D2E homepage mockup')
    t = re.sub(r'(styles\.css|shared\.js)\?v=d2d\d+', r'\1?v=d2e63', t)
    # header strapline also links to the homepage (looks the same on rollover)
    t = re.sub(r'<p class="cv-tag">([^<]*)</p>', r'<p class="cv-tag"><a href="index.html">\1</a></p>', t)
    t = t.replace('family=Oswald:wght@500;600;700', 'family=Oswald:wght@400;500;600;700&family=Roboto+Condensed:wght@400;500;600;700;900')
    t = t.replace('</head>', '<link rel="stylesheet" href="https://use.typekit.net/xvr5zgs.css">\n</head>', 1)
    f.write_text(t)

# homepage: the tabs go above the cover picture
hp = OUT / 'index.html'
t = hp.read_text()
navbar = re.search(r'<!-- Slim section bar -->\n<nav class="cv-sections".*?</nav>\n', t, re.S).group(0)
t = t.replace(navbar, '', 1)
t = t.replace('<!-- Full-bleed cover story -->', navbar.replace('<nav class="cv-sections"', '<nav class="cv-sections cv-up home-up"', 1) + '\n<!-- Full-bleed cover story -->', 1)
t = t.replace('</body>', """<script>
// the big ME mark hangs over the tab row: start the tabs just to its right
(function () {
  const nav = document.querySelector('.home-up'), me = document.querySelector('.cv-me'); if (!nav || !me) return;
  const w = nav.querySelector('.wrap');
  const fit = () => { w.style.paddingLeft = ''; const a = me.getBoundingClientRect(), b = w.getBoundingClientRect(); if (a.bottom > b.top + 4 && a.right > b.left) w.style.paddingLeft = Math.round(a.right - b.left + 14) + 'px'; };
  fit(); addEventListener('resize', fit); addEventListener('load', fit);
})();
</script>
</body>""", 1)
assert 'home-up' in t
hp.write_text(t)

# mockup bar: "Headers: Black / Grey" switch; tab links get their text in data-t (keeps the bold width reserved)
sj = OUT / 'shared.js'
js = sj.read_text()
tabsel = '<option value="grey">Grey</option></select><span class="div"></span>'
assert tabsel in js
js = js.replace(tabsel, tabsel + '<label class="lbl" for="hdr-style">Headers</label><select id="hdr-style" aria-label="Header colour"><option value="black">Black</option><option value="grey">Grey</option></select><span class="div"></span><label class="lbl" for="btn-style">Buttons</label><select id="btn-style" aria-label="Action button colour"><option value="red">Red</option><option value="blue">Blue</option></select><span class="div"></span>', 1)
js += """
// D2E: action button colour switch (mockup only): Blue keeps red for the brand only
(function () {
  let v = 'red'; try { v = localStorage.getItem('me-btn') || 'red'; } catch (e) {}
  const apply = x => document.body.classList.toggle('btn-blue', x === 'blue');
  apply(v);
  const sel = document.getElementById('btn-style');
  if (sel) { sel.value = v; sel.addEventListener('change', () => { apply(sel.value); try { localStorage.setItem('me-btn', sel.value); } catch (e) {} }); }
})();

// D2E: header colour switch (mockup only), remembered in this browser
(function () {
  let v = 'black'; try { v = localStorage.getItem('me-hdr') || 'black'; } catch (e) {}
  const apply = x => document.body.classList.toggle('hdr-grey', x === 'grey');
  apply(v);
  const sel = document.getElementById('hdr-style');
  if (sel) { sel.value = v; sel.addEventListener('change', () => { apply(sel.value); try { localStorage.setItem('me-hdr', sel.value); } catch (e) {} }); }
})();
// D2E: articles show the full date above the headline, e.g. Thursday 19 November 2026 (also on next stories as they load)
(function () {
  const full = el => { if (/day /.test(el.textContent)) return; const d = new Date(el.getAttribute('datetime') || el.textContent.trim()); if (isNaN(d)) return;
    el.textContent = d.toLocaleDateString('en-GB', { weekday: 'long' }) + ' ' + d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); };
  const run = () => document.querySelectorAll('.ac-head .cv-meta time').forEach(full);
  run(); new MutationObserver(run).observe(document.body, { childList: true, subtree: true, characterData: true });
})();
// D2E: each tab carries its own text so the row can reserve the bold width (no shift between pages)
document.querySelectorAll('.cv-sections a, .stk-tabs a').forEach(a => { a.dataset.t = a.textContent.trim(); });
"""
sj.write_text(js)
# mockup bar: "Font" switch for the headings and menus (trial fonts, loaded only when picked)
js = sj.read_text()
hdrsel = '<option value="grey">Grey</option></select><span class="div"></span><label class="lbl" for="hdr-style">'
js = js.replace('aria-label="Header colour"><option value="black">Black</option><option value="grey">Grey</option></select><span class="div"></span>',
  'aria-label="Header colour"><option value="black">Black</option><option value="grey">Grey</option></select><span class="div"></span><label class="lbl" for="font-style">Sections</label><select id="font-style" aria-label="Section heading and menu font"><option value="rc">Roboto Condensed</option><option value="oswald">Oswald (original)</option><option value="barlow">Barlow Condensed</option><option value="saira">Saira Condensed</option><option value="fira">Fira Sans Condensed</option><option value="plex">IBM Plex Sans Condensed</option><option value="archivo">Archivo Narrow</option><option value="antonio">Antonio</option></select><span class="div"></span><label class="lbl" for="hl-style">Headlines</label><select id="hl-style" aria-label="Headline font"><option value="rob">Roboto (current)</option><option value="rc">Roboto Condensed</option><option value="inter">Inter</option><option value="plex">IBM Plex Sans</option><option value="fira">Fira Sans</option><option value="barlow">Barlow</option><option value="rslab">Roboto Slab</option><option value="metronic">Metronic Slab (Adobe)</option><option value="source">Source Serif</option><option value="merri">Merriweather</option><option value="playfair">Playfair Display</option></select><span class="div"></span>', 1)
assert 'id="font-style"' in js
js += """
// D2E: the font switches are for local review only; the published mockup has no font choice
if (!/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)) ['font-style', 'hl-style'].forEach(id => { const s = document.getElementById(id); if (!s) return; const l = document.querySelector('label[for="' + id + '"]'), d = s.nextElementSibling; if (l) l.remove(); if (d && d.classList.contains('div')) d.remove(); s.remove(); });
// D2E: heading font switch (mockup only), remembered in this browser
(function () {
  const sel = document.getElementById('font-style'); if (!sel) return;
  let v = 'rc'; try { v = localStorage.getItem('me-font') || 'rc'; } catch (e) {}
  sel.value = v;
  sel.addEventListener('change', () => { try { localStorage.setItem('me-font', sel.value); } catch (e) {} window.meFont(sel.value); });
})();
// D2E: headline font switch (mockup only), remembered in this browser
(function () {
  const sel = document.getElementById('hl-style'); if (!sel) return;
  let v = 'rob'; try { v = localStorage.getItem('me-hl') || 'rob'; } catch (e) {}
  sel.value = v;
  sel.addEventListener('change', () => { try { localStorage.setItem('me-hl', sel.value); } catch (e) {} window.meHl(sel.value); });
})();
"""
sj.write_text(js)
FONT_EARLY = "<script>window.meFont=function(k){var G={barlow:'Barlow+Condensed:wght@400;500;600;700;900',saira:'Saira+Condensed:wght@400;500;600;700;900',fira:'Fira+Sans+Condensed:wght@400;500;600;700;900',plex:'IBM+Plex+Sans+Condensed:wght@400;500;600;700',archivo:'Archivo+Narrow:wght@400;500;600;700',antonio:'Antonio:wght@400;500;600;700'};document.body.dataset.font=k;if(G[k]&&!document.getElementById('gf-'+k)){var l=document.createElement('link');l.id='gf-'+k;l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family='+G[k]+'&display=swap';document.head.appendChild(l)}};try{if(!/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname))throw 0;var f=new URLSearchParams(location.search).get('font');if(f)localStorage.setItem('me-font',f);meFont(localStorage.getItem('me-font')||'rc')}catch(e){meFont('rc')}</script>"
HL_EARLY = "<script>window.meHl=function(k){var G={inter:'Inter:wght@600;700;800',plex:'IBM+Plex+Sans:wght@600;700',fira:'Fira+Sans:wght@600;700;800',barlow:'Barlow:wght@600;700;800',source:'Source+Serif+4:wght@600;700',merri:'Merriweather:wght@700',playfair:'Playfair+Display:wght@600;700;800'};document.body.dataset.hl=k;if(G[k]&&!document.getElementById('gh-'+k)){var l=document.createElement('link');l.id='gh-'+k;l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family='+G[k]+'&display=swap';document.head.appendChild(l)}};try{if(!/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname))throw 0;var h=new URLSearchParams(location.search).get('hl');if(h)localStorage.setItem('me-hl',h);meHl(localStorage.getItem('me-hl')||'rob')}catch(e){meHl('rob')}</script>"
for f in OUT.glob('*.html'):
    t = f.read_text()
    f.write_text(re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + FONT_EARLY + HL_EARLY, t, count=1))
# apply the saved header colour before first paint (no black-to-grey flash); ?hdr=grey also sets it
EARLY = "<script>try{var q=new URLSearchParams(location.search).get('hdr');if(q)localStorage.setItem('me-hdr',q);if(localStorage.getItem('me-hdr')==='grey')document.body.classList.add('hdr-grey');var b=new URLSearchParams(location.search).get('btn');if(b)localStorage.setItem('me-btn',b);if(localStorage.getItem('me-btn')==='blue')document.body.classList.add('btn-blue')}catch(e){}</script>"
for f in OUT.glob('*.html'):
    t = f.read_text()
    f.write_text(re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + EARLY, t, count=1))

# Speaking next: a "New" tab on speakers added in the last 14 days, and they come first.
# Later the speaker list will come from the event itself, so a speaker added there shows here with the tab automatically.
t = hp.read_text()
a1 = "  const count = date =>"
assert a1 in t
t = t.replace(a1, """  // date each speaker was added to the event (will come from the event record); New = added in the last 14 days, shown first
  const ADDED = { 'Nektaria Efthymiou': '2026-11-19' };
  const isNew = n => ADDED[n] && (new Date() - new Date(ADDED[n] + 'T00:00:00')) / 864e5 < 14;
  SP.sort((x, y) => isNew(y[1]) - isNew(x[1]));
""" + a1, 1)
a2 = '<div class="sn-lead"><img src="${U + img}" alt="${n}" loading="lazy">'
assert a2 in t
t = t.replace(a2, a2 + '${isNew(n) ? \'<span class="sn-new">New</span>\' : \'\'}', 1)
hp.write_text(t)

CSS = """

/* ===================== D2E: homepage tabs above the cover picture ===================== */
.d2e[data-page="home"] .cv-bar{position:relative;z-index:8;border-bottom:0}
.d2e .home-up .wrap{gap:4px}
.d2e .home-up a{padding-left:13px;padding-right:13px}
.d2e .home-up ~ .cv-hero::after{display:none}
.d2e.cv2 .home-up ~ .cv-hero .cv-head{bottom:44px}
@media (max-width:760px){.d2e.cv2 .home-up ~ .cv-hero .cv-head{bottom:28px}}
/* every menu bar: plain text links split by | (lighter type); The Briefing / Independent Research stay bolder in navy;
   the selected section keeps its tab */
.d2e .cv-sections .wrap{align-items:center;gap:0;height:50px!important;padding-top:0!important}
.d2e .cv-sections a,.d2e .cv-sections a:hover{background:none!important;border:0!important;box-shadow:none!important;border-radius:0!important;padding:0 16px!important;line-height:1;font-weight:400!important}
.d2e .cv-sections a{color:var(--ink)!important}
.d2e .cv-sections a + a{border-left:1.5px solid #b9b9b4!important}
.d2e .cv-sections a:hover{color:var(--me)!important}
.d2e .cv-sections a.f-b,.d2e .cv-sections a.f-r{color:var(--brief-navy)!important;font-weight:600!important}
.d2e .cv-sections a.f-b{border-left:0!important}
.d2e .cv-sections a.on,.d2e .cv-sections a.on:hover{align-self:flex-end;background:var(--ink)!important;color:#fff!important;border-radius:0 12px 0 0!important;padding:14px 18px 12px!important;font-weight:600!important;border-left:0!important}
.d2e .cv-sections a.f-b.on,.d2e .cv-sections a.f-r.on{background:var(--brief-navy)!important}
.d2e .cv-sections a.on + a{border-left:0!important}
@media (max-width:760px){
  .d2e .cv-sections .wrap{height:42px!important}
  .d2e .cv-sections a,.d2e .cv-sections a:hover{padding:0 11px!important}
  .d2e .cv-sections a.on,.d2e .cv-sections a.on:hover{padding:11px 12px 9px!important}
}
/* Briefing / Research pages: only their two tabs, so a shorter tab row */
@media (min-width:761px){.d2e:is(.brief-page,[data-page="res"]) .cv-sections .wrap{height:38px!important}}
/* sticky bar: the same style */
.d2e .stk-tabs{align-items:center}
.d2e .stk-tabs a,.d2e .stk-tabs a:hover{background:none!important;color:var(--ink)!important;padding:0 13px;border-radius:0;font-weight:400}
.d2e .stk-tabs a + a{border-left:1.5px solid #b9b9b4}
.d2e .stk-tabs a:hover{color:var(--me)!important}
.d2e .stk-tabs a.f-b,.d2e .stk-tabs a.f-r{color:var(--brief-navy)!important;font-weight:600}
.d2e .stk-tabs a.f-b{border-left:0}
.d2e .stk-tabs a.on,.d2e .stk-tabs a.on:hover{align-self:flex-end;background:var(--ink)!important;color:#fff!important;border-radius:0 10px 0 0;padding:12px 14px 10px;font-weight:600;border-left:0}
.d2e .stk-tabs a.on + a{border-left:0}

/* fonts (trial, also in D2F): Roboto Condensed for headings and menus in place of Oswald, Black on the main headings;
   Metronic Slab (Adobe Fonts kit xvr5zgs) in place of Roboto Slab, with the Briefing name in Semibold */
.d2e{--head:'Roboto Condensed',var(--body);--slab:"metronic-slab",'Roboto Slab',Georgia,serif}
.d2e :is(.sh h2,.nc-band h1,.ptitle,.cv-also h2,.latest-box h3,.onstage-hd h2,.mem-h h2,.mem-locked h1,.eb-side h4,.nl h4){font-weight:900!important}
.d2e :is(.fr.brief b,.mm-brief b,.fband.brief .name,.bl-strip b,.tri-tab.brief b,.bm-word){font-weight:600!important}
/* News / Insights / CxO lead: the headline goes red only when the text panel is hovered, not the picture */
.d2e .top-story:hover h2{color:inherit}
.d2e .top-story .txt:hover h2{color:var(--me)}
/* the same for the other big lead stories (the homepage cover keeps red on any rollover): homepage Insights / CxO Zone / Videos leads, channel page leads */
.d2e :is(.hx-lead,.lead-big):hover :is(h2,h3){color:inherit}
.d2e .cx-lead:hover h3{color:inherit}
.d2e :is(.hx-lead,.lead-big) .txt:hover :is(h2,h3){color:var(--me)}

/* ---- Headers: Black / Grey switch (mockup bar). Grey = light grey section headers instead of black (was D2F) ---- */
.hdr-grey{--band:#dcdde0}
.hdr-grey .nc-band{background:var(--band);color:var(--ink)}
.hdr-grey .nc-band h1{color:var(--ink)}
.hdr-grey .nc-band p{color:#4a4a4a}
.hdr-grey .nc-band .topics a{color:var(--ink2);border-color:#b9b9bd}
.hdr-grey .nc-band .topics a.on{background:var(--ink);color:#fff;border-color:var(--ink)}
/* the selected tab opens into the header, so it goes grey too (The Briefing / Research keep their navy) */
.hdr-grey .cv-sections a.on:not(.f-b):not(.f-r),.hdr-grey .cv-sections a.on:not(.f-b):not(.f-r):hover{background:var(--band)!important;color:var(--ink)!important}
.hdr-grey .stk-tabs a.on:not(.f-b):not(.f-r),.hdr-grey .stk-tabs a.on:not(.f-b):not(.f-r):hover{background:var(--band)!important;color:var(--ink)!important}
/* no black rule under the tabs: grey all the way (The Briefing / Research keep theirs) */
.hdr-grey:not(.brief-page):not([data-page="res"]) :is(.cv-sections,.cv-up){border-bottom-color:var(--band)!important}
.hdr-grey .stk{border-bottom-color:var(--band)}
/* sub-menu strip: grey like the header, with a light keyline underneath */
.hdr-grey.cv-sub.d2a-cats .cats{background:var(--band)!important;border-bottom:1px solid #c6c7cb!important}
.hdr-grey.cv-sub.d2a-cats .cats a{color:var(--ink)!important}
.hdr-grey.cv-sub.d2a-cats .cats a:hover{background:#cbccd0!important;color:var(--ink)!important}
.hdr-grey.cv-sub.d2a-cats .cats a.on,.hdr-grey.cv-sub.d2a-cats .cats a.on:hover{background:var(--me)!important;color:#fff!important}
/* homepage Speaking next (The Briefing) box: the same grey as the headers and sub-menu */
.hdr-grey .cv-minds{background:var(--band);border-color:#c6c7cb}
/* Downloads: the research link on the grey header */
.hdr-grey .nc-band .nc-res{background:#fff;border-color:#c8c8cc;color:var(--ink)}
.hdr-grey .nc-band .nc-res b{color:var(--ink)}
.hdr-grey .nc-band .nc-res:hover{border-color:var(--ink)}

/* Speaking next: "New" tab on a newly added speaker, top left of the picture */
.d2e .sn-new{position:absolute;left:0;top:0;z-index:2;background:var(--me);color:#fff;font:700 11px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;padding:7px 10px 6px;border-radius:0 0 10px 0}
@media (max-width:760px){.d2e .sn-new{font-size:10px;padding:5px 8px 4px}}
/* Font switch (mockup bar): heading / menu font options */
.d2e[data-font="oswald"]{--head:'Oswald',var(--body)}
.d2e[data-font="barlow"]{--head:'Barlow Condensed',var(--body)}
.d2e[data-font="saira"]{--head:'Saira Condensed',var(--body)}
.d2e[data-font="fira"]{--head:'Fira Sans Condensed',var(--body)}
.d2e[data-font="plex"]{--head:'IBM Plex Sans Condensed',var(--body)}
.d2e[data-font="archivo"]{--head:'Archivo Narrow',var(--body)}
.d2e[data-font="antonio"]{--head:'Antonio',var(--body)}
/* homepage Speaking next (The Briefing) box: the light grey from Headers: Grey, with black or grey headers */
.d2e .cv-minds{background:#dcdde0;border-color:#c6c7cb}
/* Headlines switch (mockup bar): story / article headline font options */
.d2e[data-hl="rc"]{--hl:'Roboto Condensed',var(--body)}
.d2e[data-hl="inter"]{--hl:'Inter',var(--body)}
.d2e[data-hl="plex"]{--hl:'IBM Plex Sans',var(--body)}
.d2e[data-hl="fira"]{--hl:'Fira Sans',var(--body)}
.d2e[data-hl="barlow"]{--hl:'Barlow',var(--body)}
.d2e[data-hl="rslab"]{--hl:'Roboto Slab',var(--body)}
.d2e[data-hl="metronic"]{--hl:"metronic-slab",var(--body)}
.d2e[data-hl="source"]{--hl:'Source Serif 4',var(--body)}
.d2e[data-hl="merri"]{--hl:'Merriweather',var(--body)}
.d2e[data-hl="playfair"]{--hl:'Playfair Display',var(--body)}
.d2e[data-hl]:not([data-hl="rob"]) :is(.cv-head b,.ac-title,.art h1,.lead-main h1,.top-story h2,.card h3,.hx-lead h3,.cx-list h3,.evx-t h3,.wp3 h3,.wp-card h3,.wp-pinned h2,.vid-card h3,.vid-hero h2,.res-item h3,.rows h3,.is-lead b,.sn-name,.ev h3,.ev-card h3,.nb-card h3,.os-card h3,.rh-copy h1,.wpd-band h1,.ev-head h1,.bl-next h1,.art-body h2){font-family:var(--hl)!important}
/* articles: the red-on-black label above the headline (e.g. Interview) is smaller */
.d2e .ac-head .cv-meta em{font-size:12px!important;letter-spacing:.08em}
@media (max-width:760px){.d2e .ac-head .cv-meta em{font-size:10.5px!important}}
.d2e .cv-tag a,.d2e .cv-tag a:hover{color:inherit;text-decoration:none}
/* phones, homepage: bigger Mobile Europe wordmark (the header buttons sit a little tighter to make room) */
@media (max-width:760px){
  .d2e[data-page="home"] .cv-acct{gap:2px}
  .d2e[data-page="home"] .cv-acct .cv-ico{width:30px}
  .d2e[data-page="home"] .cv-acct > a{padding-left:8px;padding-right:8px}
  .d2e[data-page="home"] .cv-word-link{width:100%}
  .d2e[data-page="home"] .cv-word{width:100%!important;max-width:160px}
}
/* billboards behave like Google Ad Manager slots: a fixed-size creative, never squashed. If the screen is too narrow
   for it, the slot (with its label) is left out; phones get their own mobile size (320x100 / 300x250) */
@media (min-width:761px){
  .d2e .gsma-bb{width:1200px;max-width:none;flex:none;margin:0 auto}
  .d2e .ad-bb{max-width:none}
}
@media (min-width:761px) and (max-width:1259px){
  .d2e .lb-zone,.d2e .bb-zone:has(.gsma-bb){display:none!important}
}
@media (min-width:761px) and (max-width:1029px){
  .d2e .bb-zone:has(.ad-bb){display:none!important}
}
/* homepage: the red mark always tucks over the top of the cover picture, at every screen size */
@media (min-width:761px) and (max-width:1279px){.d2e[data-page="home"] .cv-me{width:140px!important;height:140px!important;margin-bottom:-84px!important}}
/* small tablets: the strapline would wrap to several lines and push the picture down, so it is left out there */
@media (min-width:761px) and (max-width:959px){.d2e:not(.d2g)[data-page="home"] .cv-id .cv-tag{display:none}}
@media (max-width:760px){.d2e[data-page="home"] .cv-me{width:84px!important;height:84px!important;margin-bottom:-42px!important;position:relative;top:32px;z-index:9}}

/* ===================== D2E: Buttons: Blue (action buttons blue, red kept for the brand) ===================== */
.btn-blue{--act:#1f5fd6;--act-dark:#1749a8}
.btn-blue .btn:not(.white):not(.ghost),.btn-blue .btn.red,.btn-blue .btn.pink,.btn-blue .bl-introrow .btn,.btn-blue .r-introrow .btn,.btn-blue.cv-sub.brief-page .fband .btn.pink,.btn-blue .tri-sub,.btn-blue .to-top{background:var(--act)!important;color:#fff!important}
.btn-blue .btn:not(.white):not(.ghost):hover,.btn-blue .tri-sub:hover,.btn-blue .to-top:hover{background:var(--act-dark)!important}
.btn-blue .to-top{box-shadow:0 6px 18px rgba(31,95,214,.35)}
.btn-blue .cv-more:hover{background:var(--act)!important;border-color:var(--act)!important;color:#fff!important}
.btn-blue .pref input:checked + i{background:var(--act)}
.btn-blue .tone-pink .is-event .btn,.btn-blue .mm-next .btn{background:#fff!important;color:var(--act)!important}
.btn-blue :is(.art-body a,.author-box a,.sh a,.latest-box .all,.login-row a,.login-foot a,.ecta,.wp-dl,.cta,.res-item .cta,.mem-h a,.issue-nav a span,.ab-media a:not(.btn),.ab-team a:not(.btn)){color:var(--act)!important}
"""
(OUT / 'styles.css').write_text((OUT / 'styles.css').read_text() + CSS)

# Buttons: Blue: headlines no longer turn red on rollover, they get a thin underline instead.
# The red headline hovers are kept for Red only (:where adds no specificity, so other rules still win as before).
st = (OUT / 'styles.css').read_text()
HL = []
# .d2d / .d2e are classes on body itself, so join onto them rather than nesting
_pre = lambda p, x: p + x if re.match(r'\.d2[a-g]\b', x) else p + ' ' + x
def _hl(m):
    sel, body = m.group(2).strip(), m.group(3)
    if re.search(r'cv-sections|stk-tabs|cv-up|nav|tabs', sel) or not re.search(r'\b(h[1-4]|b)\b|span', sel):
        return m.group(0)
    parts = [x.strip() for x in sel.split(',')] if ':is(' not in sel else [sel]
    HL.extend(parts)
    return m.group(1) + ','.join(_pre(':where(body:not(.btn-blue))', x) for x in parts) + '{' + body + '}'
st = re.sub(r'(^|})([^{}@]*:hover[^{}]*)\{([^{}]*color:\s*var\(--me\)[^{}]*)\}', _hl, st, flags=re.M)
assert len(HL) >= 15, HL
st += '\n/* Buttons: Blue: thin underline on headline rollover instead of red */\n' + ',\n'.join(_pre('.btn-blue', x) for x in HL) + \
  '{text-decoration:underline;text-decoration-thickness:max(2px,.055em);text-underline-offset:.14em;text-decoration-skip-ink:auto}\n'
(OUT / 'styles.css').write_text(st)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
