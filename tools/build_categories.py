"""Generate the category pages (all except 5G & Beyond, which is hand-made) from the 5G layout.

Run from the repo root:  python3 tools/build_categories.py
Stories come from tools/category_data.json (scraped from mobileeurope.co.uk category pages).
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "me-redesign"
U = "https://www.mobileeurope.co.uk/wp-content/uploads/"
V = "?v=18"
DATA = json.loads((ROOT / "tools" / "category_data.json").read_text())


def e(s):
    return escape(s, quote=True)


# Independent Research reports, matched to the category they fit best
REPORTS = {
    "oss": ("OSS: Why trusted data matters as a catalyst for AI modernisation", "Dawn Bushaus, Telecoms Analyst", "2026/10/ME-Report-BLUEPLANET-COVER-v1.jpg"),
    "agentic": ("Agentic AI: Achieving autonomous network operations", "Sue Tabbitt, Business & Tech Journalist", "2026/03/ME-Report-Celfocus26-COVER.jpg"),
    "p5g": ("Solving the profit puzzle of P5G networks", "Dawn Bushaus, Telecoms Analyst", "2026/03/ME-Report-Druid-COVER-v1.jpg"),
    "openran": ("Open RAN – evolving to fulfil its promise", "Independent Research report", "2024/07/cover-report-open-ran-2024.jpg"),
    "location": ("Advancing location intelligence for emergency services in Europe", "Annie Turner, Contributing Editor", "2025/06/ME-Report-SS8-COVER-TINT-v2-1024x724.jpg"),
}

# Upcoming Briefings, matched by topic (falls back to the next Briefing)
BRIEFINGS = {
    "next": ("24", "Nov 2026", "AI", "AI in Network Optimisation: Finding Forgotten Revenue", "briefing-event.html"),
    "security": ("4", "Feb 2027", "Security", "The critical role of telcos in defence", "the-briefing.html"),
    "5g": ("15", "Apr 2027", "5G", "Extracting the full potential of 5G Standalone", "the-briefing.html"),
    "cloud": ("27", "May 2027", "Cloud", "Delivering a Cloud-native Telco", "the-briefing.html"),
}

# Sponsored pinned post for each category (advertiser content from the White Paper Hub)
PINS = {
    "wp-byod": ("Looking to deliver a seamless BYOD mobile experience?", "2026/09/GSMA-sept26-wp-696x843.jpg"),
    "wp-ericsson-auto": ("Outcomes first, autonomy follows: Business Value Pathways towards autonomous networks", "2026/07/business-value-pathways-cover3-696x860.jpg"),
    "wp-ossbss": ("Moving towards intelligent platforms: The new role of OSS/BSS", "2026/02/Ericsson-WP2-feb26-v1-696x860.jpg"),
    "wp-windriver": ("IDC Spotlight: Telco Core and IT Modernization – Cloud-Native Convergence Built for the AI Era", "2026/11/windriver-nov26-696x901.jpg"),
    "wp-dt": ("How Deutsche Telekom easily shares network settings with more than 820 OEMs", "2026/02/Ericsson-WP2-feb26-v1-1-696x860.jpg"),
    "wp-softwaremind": ("Future-Ready Telco Playbook: 4 Challenges Operators Need to Tackle", "2026/04/Softwaremind-Apr-2026-Whitepaper-1-696x860.jpg"),
    "wp-tallence": ("Telecoms 2030: How Intent-Driven Telcos Can Unlock New Value", "2026/07/Screenshot-2026-07-02-at-14.14.01-696x896.jpg"),
    "wp-comarch-trends": ("Navigating the Intelligent Future: 2026 Telco Strategic Trends", "2026/01/Comarch-WP-feb26-v1-696x860.jpg"),
    "wp-comarch-6g": ("6G – A Path Towards AI-Native Generation of Networks", "2026/07/Screenshot-2026-07-17-at-15.23.18-696x843.jpg"),
    "wp-twin": ("Network Digital Twin: The Key Catalyst for Autonomy", "2026/02/Celfocus-Feb-2026-Whitepaper-1-696x860.jpg"),
    "wp-enea": ("Detecting and Countering Fraud and Revenue Leakage in Mobile Networks", "2026/11/Detecting-and-Countering-Fraud-and-Revenue-Leakage-in-Mobile-Networks-Handbook-for-Fraud-Revenue-Assurance-Network-Teams-1-1-696x905.jpg"),
    "wp-ios": ("Want to deploy iOS and Android features in weeks?", "2026/09/ISS-OnOff-Telecom-Case-Study-3-696x843.jpg"),
}

# slug -> (display name, description, report key or None, briefing key, pin key)
CATS = {
    "access": ("Access", "Fibre, fixed wireless and broadband access networks, and the operators and wholesalers building them.", None, "next", "wp-byod"),
    "automation-ai": ("Automation/AI", "AI in the network and the business: autonomous operations, AI-RAN, agentic AI and the infrastructure behind it.", "agentic", "next", "wp-ericsson-auto"),
    "bss-oss-cx": ("BSS/OSS/CX", "Billing, operations support and customer experience systems, and the modernisation programmes replacing them.", "oss", "next", "wp-ossbss"),
    "cloud-nfv": ("Cloud/NFV", "Telco cloud, network functions virtualisation, hyperscaler partnerships and data centres.", None, "cloud", "wp-windriver"),
    "digital-platforms-apis": ("Digital Platforms & APIs", "Network APIs, digital platforms and the new services operators are building on top of their networks.", None, "next", "wp-dt"),
    "edge": ("Edge", "Edge computing, private networks, data centres and the infrastructure moving compute closer to users.", "p5g", "next", "wp-softwaremind"),
    "financial-regulation": ("Financial/Regulation", "Deals, investment, results, job cuts and the regulators shaping telecoms markets across EMEA.", None, "next", "wp-tallence"),
    "optical-ip": ("Optical/IP", "Fibre backbones, subsea cables, IP networks and the long-haul routes connecting Europe and beyond.", None, "next", "wp-comarch-trends"),
    "ran": ("RAN", "Radio access networks: Open RAN, AI-RAN, massive MIMO, ISAC and the vendors competing to supply them.", "openran", "5g", "wp-comarch-6g"),
    "satellite": ("Satellite", "Satellite and non-terrestrial networks, direct-to-device services and the spectrum battles around them.", None, "next", "wp-twin"),
    "security": ("Security", "Network security, sovereignty, defence, critical infrastructure and public safety communications.", "location", "security", "wp-enea"),
    "sustainability": ("Sustainability", "Energy efficiency, e-waste, digital inclusion and network shutdowns across the telecoms industry.", None, "next", "wp-ios"),
}

STYLE = """<style>
.ctx{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px}
.ctx .lbl{font:700 10.5px var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.toppanel{display:grid;grid-template-columns:1.7fr 1fr;gap:22px;margin-top:22px;padding:18px;background:var(--soft);border-radius:10px}
.toppanel.full{grid-template-columns:1fr}
.lead-big{display:grid;grid-template-columns:1.1fr 1fr;gap:20px;background:#fff;border-radius:8px;overflow:hidden}
.lead-big .pic{aspect-ratio:auto;height:100%;min-height:260px}
.toppanel.full .lead-big .pic{min-height:320px}
.lead-big .txt{padding:22px 20px 20px 0}
.lead-big h2{font:700 27px/1.12 var(--body);letter-spacing:-.015em;margin-top:8px}
.toppanel.full .lead-big h2{font-size:32px}
.lead-big:hover h2{color:var(--me)}
.lead-big p{color:var(--ink2);margin-top:10px}
.rep-small{background:#fff;border-radius:8px;padding:18px;display:flex;flex-direction:column;gap:12px}
.rep-small h3{font:700 17px/1.25 var(--body)}
.rep-small:hover h3{color:var(--res)}
.rep-small .by{font-size:12.5px;color:var(--muted)}
.rep-small .cta{font:700 12.5px var(--body);color:var(--res)}
@media (max-width:900px){.toppanel{grid-template-columns:1fr}.lead-big{grid-template-columns:1fr}.lead-big .txt{padding:0 18px 18px}.lead-big .pic,.toppanel.full .lead-big .pic{min-height:0;aspect-ratio:16/9}}
</style>"""


def short_date(d):
    # "17 November 2026" -> "17 Nov 2026"
    p = d.split()
    return f"{p[0]} {p[1][:3]} {p[2]}" if len(p) == 3 else d


def card(item, with_excerpt=False):
    t, img, tag, d, ex = item
    exh = f"<p>{e(ex)}</p>" if with_excerpt and ex else ""
    tg = f'<span class="tag{" ins" if tag == "Insights" else ""}">{e(tag)}</span>' if tag else ""
    return (f'<a class="card" href="article.html"><div class="pic"><img src="{U}{img}" alt="">{tg}</div>'
            f'<h3>{e(t)}</h3>{exh}<div class="date">{e(short_date(d))}</div></a>')


def page(slug, name, desc, rep_key, brief_key, pin_key):
    items = [i for i in DATA[slug] if not i[0].lower().startswith("download:")]
    lead, first, rest = items[0], items[1:4], items[4:10]
    lt, li, ltag, ld, lex = lead
    n = e(name)

    report = ""
    if rep_key:
        rt, rby, rimg = REPORTS[rep_key]
        report = f"""
    <!-- Optional: editors can pin a relevant Independent Research report on any category page -->
    <a class="rep-small" href="research.html">
      <span class="pin-inline" data-pin style="color:var(--res)">Pinned · Independent Research</span>
      <div class="cover"><img src="{U}{rimg}" alt="{e(rt)} report cover"></div>
      <h3>{e(rt)}</h3>
      <div class="by">{e(rby)}</div>
      <span class="cta">Download free →</span>
    </a>"""

    bd, bm, btopic, btitle, bhref = BRIEFINGS[brief_key]
    blabel = f"The Briefing on {btopic}" if brief_key != "next" else "Next Briefing"
    pt, pimg = PINS[pin_key]

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{n} – Mobile Europe mockup</title>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto:wght@400;500;600;700;800&family=Roboto+Slab:wght@500;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css{V}">
{STYLE}
</head>
<body data-page="cat" data-cat="{n}">
<div id="site-header"></div>

<main class="wrap">
  <div class="crumb"><a href="index.html">Home</a><span>|</span>{n}</div>
  <h1 class="ptitle">{n}</h1>
  <p class="pdesc">{e(desc)}</p>

  <section class="toppanel{'' if rep_key else ' full'}">
    <a class="lead-big" href="article.html">
      <div class="pic"><img src="{U}{li}" alt="">{f'<span class="tag">{e(ltag)}</span>' if ltag else ''}</div>
      <div class="txt">
        <div class="kick">Latest</div>
        <h2>{e(lt)}</h2>
        <p>{e(lex)}</p>
        <div class="date">{e(ld)}</div>
      </div>
    </a>{report}
  </section>

  <div class="with-rail" style="margin-top:8px">
    <div>
      <div class="sh"><h2>More in {n}</h2><a href="#">RSS</a></div>
      <div class="grid2">
        {card(first[0], True)}
        <div class="pin-slot" data-fixed>
          <a class="card sp-card" href="article.html">
            <div class="sp-top"><span class="sp-label">Sponsored</span><span class="pin-inline" data-pin>Pinned post</span></div>
            <div class="pic"><img src="{U}{pimg}" alt="" style="object-position:center 20%"></div>
            <h3>{e(pt)}</h3>
          </a>
          <a class="pin-cta" href="#" data-pin-cta>Pin your post here →</a>
        </div>
        {card(first[1], True)}
        {card(first[2], True)}
      </div>
    </div>
    <aside class="rail">
      <div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU 1<small>300×250 · GAM</small></div></div>
      <div class="ctx">
        <div class="lbl">{e(blabel)}</div>
        <a class="ev" href="{bhref}" style="border:0"><div class="d"><b>{bd}</b><small>{bm}</small></div><div class="t" style="padding:10px 12px"><div class="series">The Briefing <em>| {e(btopic)}</em></div><h3 style="font-size:15px">{e(btitle)}</h3></div></a>
        <a class="btn pink" style="margin-top:10px;width:100%;justify-content:center" href="{bhref}">{'Register free' if bhref == 'briefing-event.html' else 'Get a reminder'}</a>
      </div>
      <div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU 2<small>300×250 · GAM</small></div></div>
    </aside>
  </div>
</main>

<div class="bb-zone"><div class="ad-label">Advertisement</div><div class="ad ad-bb">Billboard (BB)<small>970×250 · GAM</small></div></div>

<main class="wrap">
  <div class="with-rail">
    <div class="grid2">
      {''.join(card(i) for i in rest)}
    </div>
    <aside class="rail"><div class="sticky">
      <div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU 3<small>300×250 · GAM</small></div></div>
      <div class="nl"><h4>{n} alerts</h4><p>Get this section’s top stories, plus new reports and Briefings on the topic, once a week.</p><input placeholder="Work email" aria-label="Work email"><button class="btn red">Follow topic</button></div>
      <div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU 4<small>300×250 · GAM</small></div></div>
    </div></aside>
  </div>
  <div style="text-align:center;margin-top:30px"><a class="btn ghost" href="#">Load more {n}</a></div>
</main>

<div id="site-footer"></div>
<script src="shared.js{V}"></script>
</body>
</html>
"""
    (OUT / f"category-{slug}.html").write_text(html)


for slug, cfg in CATS.items():
    page(slug, *cfg)
print("Wrote", len(CATS), "category pages:", ", ".join(f"category-{s}.html" for s in CATS))
