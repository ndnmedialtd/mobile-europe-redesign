#!/usr/bin/env python3
"""D2F is now part of D2E (Headers: Grey in the mockup bar). This writes small redirect pages so old D2F links
open the same page in D2E with grey headers."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'me-redesign-d2e'
OUT = ROOT / 'me-redesign-d2f'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for f in sorted(SRC.glob('*.html')):
    (OUT / f.name).write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Mobile Europe D2E</title>
<script>try{{localStorage.setItem('me-hdr','grey')}}catch(e){{}}location.replace('../me-redesign-d2e/{f.name}'+location.search+location.hash)</script>
</head><body><p><a href="../me-redesign-d2e/{f.name}?hdr=grey">Open this page in D2E</a></p></body></html>
""")
print('wrote', len(list(OUT.glob('*.html'))), 'redirect pages in', OUT.name)
