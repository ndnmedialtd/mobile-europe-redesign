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
    t = re.sub(r'(styles\.css|shared\.js)\?v=d2d\d+', r'\1?v=d2e2', t)
    t = t.replace('family=Oswald:wght@500;600;700', 'family=Oswald:wght@400;500;600;700')
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
"""
(OUT / 'styles.css').write_text((OUT / 'styles.css').read_text() + CSS)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
