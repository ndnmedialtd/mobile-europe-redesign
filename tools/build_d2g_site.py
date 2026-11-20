#!/usr/bin/env python3
"""Build D2G: D2E with a built logo - the big ME mark becomes a red square with MOBILE / EUROPE stacked in bold
(rounded top-right and bottom-left), and the separate Mobile Europe wordmark is removed.

Built from me-redesign-d2e/ (run tools/build_d2e_site.py first); D2E is not changed.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2e'
OUT = ROOT / 'me-redesign-d2g'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)


# logo icon: a small white line icon top left of the red block, different for each section and channel
ICONS = {
    'broadcast': '<path class="ghost" d="M16.2 7.8a6 6 0 0 1 0 8.4M7.8 16.2a6 6 0 0 1 0-8.4M19.1 4.9a10 10 0 0 1 0 14.2M4.9 19.1a10 10 0 0 1 0-14.2"/><circle cx="12" cy="12" r="2"/><path class="w1" d="M16.2 7.8a6 6 0 0 1 0 8.4M7.8 16.2a6 6 0 0 1 0-8.4"/><path class="w2" d="M19.1 4.9a10 10 0 0 1 0 14.2M4.9 19.1a10 10 0 0 1 0-14.2"/>',
    'news': '<path d="M4 5h13v14H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v8a2 2 0 0 1-2 2"/><path d="M7 9h7M7 12h7M7 15h4"/>',
    'grid': '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
    'bulb': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    'download': '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    'play': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9l5 3-5 3z"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
    'chart': '<path d="M4 20h16M7 16v-5M12 16V6M17 16v-8"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
    'people': '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.5A5 5 0 0 1 21 20"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    'signal': '<path d="M5 20v-3M10 20v-7M15 20V9M20 20V5"/>',
    'home': '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    'chip': '<rect x="7" y="7" width="10" height="10" rx="1"/><path d="M10 10h4v4h-4zM9 3v4M15 3v4M9 17v4M15 17v4M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    'headset': '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1"/><rect x="17" y="14" width="4" height="6" rx="1"/>',
    'cloud': '<path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9.5 4.3 4.3 0 0 0 7 18z"/>',
    'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>',
    'server': '<rect x="4" y="4" width="16" height="6" rx="1"/><rect x="4" y="14" width="16" height="6" rx="1"/><path d="M8 7h.01M8 17h.01"/>',
    'scales': '<path d="M12 4v16M7 20h10M5 8h14M5 8l-3 6a3 3 0 0 0 6 0zM19 8l-3 6a3 3 0 0 0 6 0z"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'tower': '<path d="M12 9v12M8 21l4-12 4 12M9.5 16h5"/><circle cx="12" cy="7" r="1.5"/><path d="M7.5 3.5a6 6 0 0 0 0 7M16.5 3.5a6 6 0 0 1 0 7"/>',
    'satellite': '<path d="M4 10a10 10 0 0 0 10 10z"/><path d="M9 15l4-4M13 7a4 4 0 0 1 4 4M13 3a8 8 0 0 1 8 8"/>',
    'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'doc': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    'leaf': '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
}
# section icons beside the broadcast icon: switched off for now (set True to bring them back)
SHOW_SECTION_ICON = False
SECTION = {
    'news.html': ('News', 'news.html'), 'article.html': ('News', 'news.html'), 'channels.html': ('Channels', 'channels.html'),
    'insights.html': ('Insights', 'insights.html'), 'cxo.html': ('CxO Zone', 'cxo.html'), 'white-papers.html': ('Downloads', 'white-papers.html'),
    'white-paper.html': ('Downloads', 'white-papers.html'), 'videos.html': ('Videos', 'videos.html'), 'events.html': ('Events', 'events.html'),
    'the-briefing.html': ('The<br>Briefing', 'the-briefing.html'), 'briefing-event.html': ('The<br>Briefing', 'the-briefing.html'),
    'research.html': ('Research', 'research.html'), 'about.html': ('About', 'about.html'), 'editorial-board.html': ('Editorial<br>Board', 'editorial-board.html'),
    'members.html': ('Members', 'members.html'),
    'category-5g.html': ('5G &amp;<br>Beyond', 'category-5g.html'), 'category-access.html': ('Access', 'category-access.html'),
    'category-automation-ai.html': ('Automation<br>/AI', 'category-automation-ai.html'), 'category-bss-oss-cx.html': ('BSS/OSS<br>/CX', 'category-bss-oss-cx.html'),
    'category-cloud-nfv.html': ('Cloud<br>/NFV', 'category-cloud-nfv.html'), 'category-digital-platforms-apis.html': ('Platforms<br>&amp; APIs', 'category-digital-platforms-apis.html'),
    'category-edge.html': ('Edge', 'category-edge.html'), 'category-financial-regulation.html': ('Finance<br>/Regulation', 'category-financial-regulation.html'),
    'category-optical-ip.html': ('Optical<br>/IP', 'category-optical-ip.html'), 'category-ran.html': ('RAN', 'category-ran.html'),
    'category-satellite.html': ('Satellite', 'category-satellite.html'), 'category-security.html': ('Security', 'category-security.html'),
    'category-sustainability.html': ('Sustain-<br>ability', 'category-sustainability.html'),
}
PAGE_ICON = {
    'index.html': 'broadcast', 'news.html': 'news', 'article.html': 'news', 'channels.html': 'grid', 'insights.html': 'bulb',
    'cxo.html': 'briefcase', 'white-papers.html': 'download', 'white-paper.html': 'download', 'videos.html': 'play',
    'events.html': 'calendar', 'the-briefing.html': 'clock', 'briefing-event.html': 'clock', 'research.html': 'doc',
    'about.html': 'info', 'editorial-board.html': 'people', 'members.html': 'user',
    'category-5g.html': 'signal', 'category-access.html': 'home', 'category-automation-ai.html': 'chip',
    'category-bss-oss-cx.html': 'headset', 'category-cloud-nfv.html': 'cloud', 'category-digital-platforms-apis.html': 'code',
    'category-edge.html': 'server', 'category-financial-regulation.html': 'scales', 'category-optical-ip.html': 'globe',
    'category-ran.html': 'tower', 'category-satellite.html': 'satellite', 'category-security.html': 'shield',
    'category-sustainability.html': 'leaf',
}
for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    t = re.sub(r'(<body[^>]*class=")', r'\1d2g ', t, count=1)
    t = t.replace('Mobile Europe D2E mockup', 'Mobile Europe D2G mockup').replace('Mobile Europe – D2E homepage mockup', 'Mobile Europe – D2G homepage mockup')
    t = re.sub(r'(styles\.css|shared\.js)\?v=d2e\d+', r'\1?v=d2g20', t)
    # trial: the big ME mark is built in the page: MOBILE / EUROPE stacked in bold on the red square
    t = t.replace('<a class="cv-me" href="index.html" aria-label="Mobile Europe home"><img src="../brand/me-mark.png" alt="ME" width="400" height="400"></a>',
                  '<a class="cv-me me-built" href="index.html" aria-label="Mobile Europe home"><span class="me-stack"><b>MOBILE</b><b>EUROPE</b></span></a>')
    ico = ICONS['broadcast']   # the red logo always carries the homepage icon
    t = t.replace('<span class="me-stack">', '<span class="me-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ico + '</svg></span><span class="me-stack">', 1)
    # section icon: a second little icon, in black, beside the broadcast icon inside the red logo (not on the homepage)
    if SHOW_SECTION_ICON and f.name in SECTION:
        sec_ico = ('<span class="me-ico me-sec" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                   + ICONS[PAGE_ICON[f.name]] + '</svg></span>')
        t = t.replace('<span class="me-stack">', sec_ico + '<span class="me-stack">', 1)
    f.write_text(t)

CSS = """

/* ===================== D2G: built logo ===================== */
/* built logo, "masthead" style: MOBILE / EUROPE in Roboto Condensed Black at the bottom of the red square,
   a short white rule top left, rounded top-right corner. Sizes follow the square, so it works at every size */
.d2g .cv-me.me-built{container-type:size;border-radius:0!important;display:block!important;position:relative}
/* the logo sits flush against the grey billboard band above it (pulls up over the header's 1px top line) */
.d2g .cv-me.me-built{margin-top:-1px!important;z-index:9}
/* inner pages: a bit bigger, filling the header bar from top to bottom */
.d2g.cv-sub:not(.brief-page):not([data-page="res"]) .cv-me.me-built{width:68px!important;height:68px!important;align-self:flex-start!important;margin-bottom:0!important}
@media (max-width:760px){.d2g.cv-sub:not(.brief-page):not([data-page="res"]) .cv-me.me-built{width:56px!important;height:56px!important}}
.d2g .me-stack{position:absolute;left:9.5cqw;right:6cqw;bottom:8.5cqw;display:flex;flex-direction:column;align-items:flex-start;color:#fff;font:900 24cqw/.88 'Roboto Condensed',var(--body)!important;letter-spacing:0;text-transform:uppercase}
.d2g .me-stack b{display:block;font-weight:900}
.d2g .me-ico{position:absolute;left:8.5cqw;top:8.5cqw;width:22cqw;height:22cqw;color:#fff;display:block}
.d2g .me-ico svg{width:100%;height:100%;display:block}
/* small logos (inner pages, phones): the icon takes a bigger share of the block and a slightly heavier line */
@container (max-width:100px){.d2g .me-ico{left:7cqw;top:6cqw;width:31cqw;height:31cqw}.d2g .me-ico svg{stroke-width:2.4}}
/* no MOBILE EUROPE wordmark beside it (the built mark carries the name) */
.d2g .cv-id .cv-word-link{display:none!important}
.d2g .cv-id .cv-tag{border-left:0!important;padding-left:0!important}
/* the section's own icon, in black, just right of the broadcast icon */
.d2g .me-ico.me-sec{left:36cqw;color:var(--ink)}
@container (max-width:100px){.d2g .me-ico.me-sec{left:43cqw}}
/* broadcast icon: the waves radiate out from the dot, inner then outer, on a slow loop;
   a dark red copy of the waves stays behind them all the time, so the icon keeps its shape */
.d2g .me-ico .ghost{stroke:#8e0a27}
.d2g .cv-me .me-ico .w1,.d2g .cv-me .me-ico .w2{transform-origin:12px 12px;animation:meWave 2.4s ease-out infinite}
.d2g .cv-me .me-ico .w2{animation-delay:.35s}
@keyframes meWave{0%{opacity:0;transform:scale(.7)}25%{opacity:1;transform:scale(1)}60%{opacity:1;transform:scale(1.04)}100%{opacity:0;transform:scale(1.12)}}
@media (prefers-reduced-motion:reduce){.d2g .cv-me .me-ico .w1,.d2g .cv-me .me-ico .w2{animation:none}}
/* The Briefing page: the logo's bottom edge lines up with the baseline of THE BRIEFING (logo a little bigger, title moved right to keep the gap) */
@media (min-width:1101px){.d2g[data-page="brief"] .cv-me.me-built{width:135px!important;height:135px!important;margin-bottom:-85px!important}.d2g[data-page="brief"] .fband .wrap{padding-left:179px!important}}
@media (max-width:1100px) and (min-width:761px){.d2g[data-page="brief"]{--bme:min(130px,calc(75px + 5vw))}.d2g[data-page="brief"] .cv-me.me-built{width:var(--bme)!important;height:var(--bme)!important;margin-bottom:calc(50px - var(--bme))!important}.d2g[data-page="brief"] .fband .wrap{padding-left:calc(var(--bme) + 44px)!important}}
"""
(OUT / 'styles.css').write_text((OUT / 'styles.css').read_text() + CSS)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
