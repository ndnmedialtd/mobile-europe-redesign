#!/usr/bin/env python3
"""Build D2F: D2E with light grey section headers (News, channels, Insights etc.) instead of black.

Built from me-redesign-d2e/ (run tools/build_d2e_site.py first); D2E is not changed, so the two can be compared.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2e'
OUT = ROOT / 'me-redesign-d2f'

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

for f in sorted(OUT.glob('*.html')):
    t = f.read_text()
    t = re.sub(r'(<body[^>]*class=")', r'\1d2f ', t, count=1)
    t = t.replace('Mobile Europe D2E mockup', 'Mobile Europe D2F mockup').replace('Mobile Europe – D2E homepage mockup', 'Mobile Europe – D2F homepage mockup')
    t = re.sub(r'(styles\.css|shared\.js)\?v=d2e\d+', r'\1?v=d2f9', t)
    f.write_text(t)

CSS = """

/* ===================== D2F: light grey section headers instead of black ===================== */
.d2f{--band:#dcdde0}
.d2f .nc-band{background:var(--band);color:var(--ink)}
.d2f .nc-band h1{color:var(--ink)}
.d2f .nc-band p{color:#4a4a4a}
.d2f .nc-band .topics a{color:var(--ink2);border-color:#b9b9bd}
.d2f .nc-band .topics a.on{background:var(--ink);color:#fff;border-color:var(--ink)}
/* the selected tab opens into the header, so it goes grey too (The Briefing / Research keep their navy) */
.d2f .cv-sections a.on:not(.f-b):not(.f-r),.d2f .cv-sections a.on:not(.f-b):not(.f-r):hover{background:var(--band)!important;color:var(--ink)!important}
.d2f .stk-tabs a.on:not(.f-b):not(.f-r),.d2f .stk-tabs a.on:not(.f-b):not(.f-r):hover{background:var(--band)!important;color:var(--ink)!important}
/* no black rule under the tabs: grey all the way (The Briefing / Research keep theirs) */
.d2f:not(.brief-page):not([data-page="res"]) :is(.cv-sections,.cv-up){border-bottom-color:var(--band)!important}
.d2f .stk{border-bottom-color:var(--band)}
/* sub-menu strip: grey like the header, with a light keyline underneath */
.d2f.cv-sub.d2a-cats .cats{background:var(--band)!important;border-bottom:1px solid #c6c7cb!important}
.d2f.cv-sub.d2a-cats .cats a{color:var(--ink)!important}
.d2f.cv-sub.d2a-cats .cats a:hover{background:#cbccd0!important;color:var(--ink)!important}
.d2f.cv-sub.d2a-cats .cats a.on,.d2f.cv-sub.d2a-cats .cats a.on:hover{background:var(--me)!important;color:#fff!important}
/* homepage Speaking next (The Briefing) box: the same grey as the headers and sub-menu */
.d2f .cv-minds{background:var(--band);border-color:#c6c7cb}
/* Downloads: the research link on the grey header */
.d2f .nc-band .nc-res{background:#fff;border-color:#c8c8cc;color:var(--ink)}
.d2f .nc-band .nc-res b{color:var(--ink)}
.d2f .nc-band .nc-res:hover{border-color:var(--ink)}
"""
(OUT / 'styles.css').write_text((OUT / 'styles.css').read_text() + CSS)
print('built', len(list(OUT.glob('*.html'))), 'pages in', OUT.name)
