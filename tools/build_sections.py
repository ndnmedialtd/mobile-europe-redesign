"""Generate the Insights, CxO Zone, White Paper Hub, Videos and Events mockup pages.

Run from the repo root:  python3 tools/build_sections.py
Content (titles, images, dates) is taken from mobileeurope.co.uk for layout only.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "me-redesign"
U = "https://www.mobileeurope.co.uk/wp-content/uploads/"
V = "?v=14"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Mobile Europe mockup</title>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto:wght@400;500;600;700;800&family=Roboto+Slab:wght@400;500;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css{v}">
</head>
<body data-page="{page}">
<div id="site-header"></div>
"""
FOOT = """
<div id="site-footer"></div>
<script src="shared.js{v}"></script>
</body>
</html>
"""

MPU = '<div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU {n}<small>300×250 · GAM</small></div></div>'
BB = '<div class="bb-zone"><div class="ad-label">Advertisement</div><div class="ad ad-bb">Billboard (BB)<small>970×250 · GAM · 300×250 on mobile</small></div></div>'
NB_CARD = """<a class="nb-card" href="briefing-event.html">
        <div class="top">
          <div class="lbl"><span>The Briefing · Next live event</span><span>AI</span></div>
          <div class="when">Tuesday 24 November</div>
          <h3>AI in Network Optimisation: Finding Forgotten Revenue</h3>
          <div class="count" data-cd></div>
        </div>
        <div class="bot">
          <div class="spons">Exclusive sponsor<br><img src="https://www.mobileeurope.co.uk/wp-content/uploads/2026/07/anritsu-logo.svg" alt="Anritsu"></div>
          <span class="btn pink">Register free</span>
        </div>
      </a>"""
RES_CARD = """<a class="side-rep" href="research.html">
        <small>Independent Research · New report</small>
        <img src="https://www.mobileeurope.co.uk/wp-content/uploads/2026/10/ME-Report-BLUEPLANET-COVER-v1.jpg" alt="">
        <b>OSS: Why trusted data matters as a catalyst for AI modernisation</b>
        <span>Download free →</span>
      </a>"""
NEWSLETTER = '<div class="nl"><h4>Get the newsletter</h4><p>The week’s essential EMEA telecoms news and analysis, plus first notice of new Briefings and reports.</p><input placeholder="Work email" aria-label="Work email"><button class="btn red">Subscribe</button></div>'


def e(s):
    return escape(s, quote=True)


def card(title, img, tag, date, ins=False):
    t = f'<span class="tag{" ins" if ins else ""}">{e(tag)}</span>' if tag else ""
    d = f'<div class="date">{e(date)}</div>' if date else ""
    return (f'<a class="card" href="article.html"><div class="pic"><img src="{U}{img}" alt="">{t}</div>'
            f'<h3>{e(title)}</h3>{d}</a>')


def pinned(title, img, ins=False):
    return f"""<div class="pin-slot" data-fixed>
          <a class="card sp-card" href="article.html">
            <div class="sp-top"><span class="sp-label">Sponsored</span><span class="pin-inline" data-pin>Pinned post</span></div>
            <div class="pic"><img src="{U}{img}" alt=""></div>
            <h3>{e(title)}</h3>
          </a>
          <a class="pin-cta" href="#" data-pin-cta>Pin your post here →</a>
        </div>"""


def head_block(crumb, h1, desc, chips):
    chip_html = "".join(f'<a class="{"on" if i == 0 else ""}" href="#">{e(c)}</a>' for i, c in enumerate(chips))
    return f"""
<main class="wrap">
  <div class="crumb"><a href="index.html">Home</a><span>|</span>{e(crumb)}</div>
  <h1 class="ptitle">{e(h1)}</h1>
  <p class="pdesc">{e(desc)}</p>
  <div class="topics">{chip_html}</div>
"""


# ---------------------------------------------------------------- News-style
def news_style(page, title, desc, chips, lead, items, pin, more_label, ins=False):
    """lead = (title, img, tag, date, standfirst); items = list of (title, img, tag, date)."""
    lt, li, ltag, ld, lsf = lead
    first, rest = items[:3], items[3:9]
    html = HEAD.format(title=title, page=page, v=V) + head_block(title, title, desc, chips)
    html += f"""
  <a class="top-story" href="article.html">
    <div class="pic"><img src="{U}{li}" alt=""><span class="tag{' ins' if ins else ''}">{e(ltag)}</span></div>
    <div class="txt">
      <div class="kick">Latest</div>
      <h2>{e(lt)}</h2>
      <p>{e(lsf)}</p>
      <div class="date">{e(ld)}</div>
    </div>
  </a>

  <div class="with-rail" style="margin-top:8px">
    <div>
      <div class="sh"><h2>{e(more_label)}</h2><a href="#">RSS</a></div>
      <div class="grid2">
        {card(*first[0], ins=ins)}
        {pinned(*pin)}
        {card(*first[1], ins=ins)}
        {card(*first[2], ins=ins)}
      </div>
    </div>
    <aside class="rail">
      {MPU.format(n=1)}
      {NB_CARD}
      {MPU.format(n=2)}
    </aside>
  </div>
</main>

{BB}

<main class="wrap">
  <div class="with-rail">
    <div class="grid2">
      {''.join(card(*i, ins=ins) for i in rest)}
    </div>
    <aside class="rail"><div class="sticky">
      {MPU.format(n=3)}
      {NEWSLETTER}
      {MPU.format(n=4)}
    </div></aside>
  </div>
  <div style="text-align:center;margin-top:30px"><a class="btn ghost" href="#">Load more</a></div>
</main>
"""
    (OUT / f"{page}.html").write_text(html + FOOT.format(v=V))


news_style(
    "insights", "Insights",
    "Interviews, analysis and opinion from the people shaping communications infrastructure and digital services in EMEA.",
    ["All insights", "Interviews", "Analysis", "Opinion", "Partner content"],
    ("Data centres must look beyond the ‘bragawatts’ race, says Pulsant CEO", "2026/11/Rob-Coupland-ME.png", "Interview", "11 November 2026",
     "The data centre industry has become “obsessed with bragawatts” and the race to build bigger AI campuses, according to Pulsant CEO Rob Coupland."),
    [
        ("Cellnex UK MD on ‘catching up’ with Europe’s 5G networks", "2026/11/Steve-Cray.png", "Interview", "5 Nov 2026"),
        ("Does a football club really need its own mobile service? ‘There’s no need,’ says Everton Mobile boss", "2026/10/Everton-Mobile.png", "Interview", "30 Oct 2026"),
        ("Mavenir CRO on why AI is putting the mobile core back in focus", "2026/10/Dejan-Leskaoski.png", "Interview", "20 Oct 2026"),
        ("Fresh wave of job cuts hits telecoms industry", "2026/10/Job-cuts-continue-ME.png", "Analysis", "13 Oct 2026"),
        ("Fibre’s consolidation phase will be won on systems and service quality, not speed", "2026/09/Octave.png", "Opinion", "9 Oct 2026"),
        ("Can BT fix TalkTalk – and is the brand worth saving?", "2026/10/TalkTalk-BT-AI.png", "Analysis", "8 Oct 2026"),
        ("Samsung on ISAC: Could mobile networks replace cameras?", "2026/10/Samsung-ISAC.png", "Interview", "6 Oct 2026"),
        ("Vodafone IoT: ‘Europe’s IoT landscape is turning into a checkerboard’", "2026/10/Vodafone-IoT-ME.png", "Interview", "1 Oct 2026"),
        ("TalkTalk on the brink: What went wrong?", "2026/09/TalkTalk.png", "Analysis", "28 Sep 2026"),
    ],
    ("Customers have picked their assistant – and it isn’t the one you built", "2026/10/Celfocus-image.png"),
    "More insights", ins=True,
)

news_style(
    "cxo", "CxO Zone",
    "Appointments, boardroom moves and leadership news from operators and vendors across EMEA.",
    ["All", "Appointments", "Boardroom", "Deals", "Leadership"],
    ("Google’s Don Harrison resigns from SpaceX board", "2026/11/SpaceX-696x464.jpeg", "Boardroom", "10 November 2026",
     "SpaceX has announced Don Harrison has stepped down from its Board of Directors, according to a company filing."),
    [
        ("Telus names ex-EE and ex-KPMG chiefs to board", "2026/11/Telus.png", "Boardroom", "9 Nov 2026"),
        ("Google poaches Samsung VP Annika Bizon to lead TMT team", "2026/11/Google-Annika-Bizon.png", "Appointment", "6 Nov 2026"),
        ("Celfocus’ Carla Penedo joins Mobile Europe’s Editorial Advisory Board", "2026/11/CELFOCUS-.png", "Appointment", "4 Nov 2026"),
        ("Zain, Ooredoo combine 4,000 towers in Qatar and Kuwait", "2026/10/Zain-Ooredoo.png", "Deals", "23 Oct 2026"),
        ("Ericsson CEO shakes up leadership in major restructuring", "2026/10/Ericsson.png", "Leadership", "16 Oct 2026"),
        ("Telenet CEO John Porter exits after 13 years", "2026/10/TELENET-CEO.png", "Leadership", "15 Oct 2026"),
        ("Telenor names ex-Nokia CEO to lead IoT board", "2026/10/Nokia-Pekka.png", "Boardroom", "12 Oct 2026"),
        ("Nokia appoints Turki Alzwaiml as Country Manager for Saudi Arabia", "2026/10/Nokia-Saudi-Arabia.png", "Appointment", "8 Oct 2026"),
        ("VMO2 CEO: BT-TalkTalk deal ‘makes a mockery of the market’", "2026/10/VMO2-BT.png", "Leadership", "7 Oct 2026"),
    ],
    ("On AI and autonomous networks: Sceptics and believers make the same mistake", "2026/10/OCT-Celfocus-696x464.png"),
    "More from the CxO Zone",
)


# ---------------------------------------------------------------- Block pages
def block_page(page, title, desc, chips, body, rail_extra):
    html = HEAD.format(title=title, page=page, v=V) + head_block(title, title, desc, chips)
    html += f"""
  <div class="with-rail" style="margin-top:24px">
    <div>{body}</div>
    <aside class="rail"><div class="sticky">
      {MPU.format(n=1)}
      {rail_extra}
      {MPU.format(n=2)}
    </div></aside>
  </div>
</main>
"""
    (OUT / f"{page}.html").write_text(html + FOOT.format(v=V))


# White Paper Hub ------------------------------------------------------------
WP = [
    ("IDC Spotlight: Telco Core and IT Modernization – Cloud-Native Convergence Built for the AI Era", "Report", "Wind River", "2026/11/windriver-nov26-696x901.jpg"),
    ("Detecting and Countering Fraud and Revenue Leakage in Mobile Networks", "Handbook", "ENEA", "2026/11/Detecting-and-Countering-Fraud-and-Revenue-Leakage-in-Mobile-Networks-Handbook-for-Fraud-Revenue-Assurance-Network-Teams-1-1-696x905.jpg"),
    ("Looking to deliver a seamless BYOD mobile experience?", "Case study", "GSMA", "2026/09/GSMA-sept26-wp-696x843.jpg"),
    ("Want to deploy iOS and Android features in weeks?", "Case study", "GSMA", "2026/09/ISS-OnOff-Telecom-Case-Study-3-696x843.jpg"),
    ("Taking a proactive approach to telecom fraud prevention", "Case study", "GSMA", "2026/07/GSMA-Case-Study-July-2026-cover-2-696x988.jpg"),
    ("6G – A Path Towards AI-Native Generation of Networks", "White paper", "Comarch", "2026/07/Screenshot-2026-07-17-at-15.23.18-696x843.jpg"),
    ("Outcomes first, autonomy follows: Business Value Pathways towards autonomous networks", "White paper", "Ericsson", "2026/07/business-value-pathways-cover3-696x860.jpg"),
    ("Telecoms 2030: How Intent-Driven Telcos Can Unlock New Value", "White paper", "Tallence", "2026/07/Screenshot-2026-07-02-at-14.14.01-696x896.jpg"),
    ("Future-Ready Telco Playbook: 4 Challenges Operators Need to Tackle", "White paper", "Software Mind", "2026/04/Softwaremind-Apr-2026-Whitepaper-1-696x860.jpg"),
    ("Secure AI by Design: A Shift-Left Approach to AI Development", "White paper", "Celfocus", "2026/03/Celfocus-Apr-2026-Whitepaper-1-696x860.jpg"),
    ("How Deutsche Telekom easily shares network settings with more than 820 OEMs", "White paper", "GSMA", "2026/02/Ericsson-WP2-feb26-v1-1-696x860.jpg"),
    ("Moving towards intelligent platforms: The new role of OSS/BSS", "White paper", "Appledore Research for Ericsson", "2026/02/Ericsson-WP2-feb26-v1-696x860.jpg"),
    ("Network Digital Twin: The Key Catalyst for Autonomy", "White paper", "Celfocus", "2026/02/Celfocus-Feb-2026-Whitepaper-1-696x860.jpg"),
    ("Navigating the Intelligent Future: 2026 Telco Strategic Trends", "White paper", "Comarch", "2026/01/Comarch-WP-feb26-v1-696x860.jpg"),
]
wp_cards = "".join(
    f'<a class="wp-card" href="#"><div class="cover-p"><img src="{U}{img}" alt=""></div>'
    f'<h3>{e(t)}</h3><div class="wp-meta">{e(kind)} · {e(by)}</div><span class="wp-dl">Download free →</span></a>'
    for t, kind, by, img in WP
)
wp_body = f"""
      <div class="wp-pinned">
        <div class="cover-p"><img src="{U}2026/09/ISS-OnOff-Telecom-Case-Study-3-WP-696x844.jpg" alt=""></div>
        <div class="txt">
          <div class="sp-top"><span class="sp-label">Sponsored</span><span class="pin-inline" data-pin>Pinned post</span></div>
          <h2>There’s a Core for That</h2>
          <div class="wp-meta">White paper · Mavenir</div>
          <p>Turn your mobile network core into a growth engine for new revenue, richer customer experiences and superior network performance.</p>
          <a class="btn red" href="#">Download free</a>
          <a class="pin-cta" href="#" data-pin-cta style="display:block;text-align:left;margin-top:12px">Pin your white paper here →</a>
        </div>
      </div>
      <div class="sh" style="margin-top:34px"><h2>Latest white papers &amp; reports</h2></div>
      <div class="wp-grid">{wp_cards}</div>
      <div style="text-align:center;margin-top:30px"><a class="btn ghost" href="#">Load more</a></div>"""
block_page("white-papers", "White Paper Hub",
           "Free white papers, case studies, handbooks and reports from the companies building EMEA’s networks.",
           ["All", "White papers", "Case studies", "Reports", "Handbooks"], wp_body, RES_CARD)

# Videos ---------------------------------------------------------------------
VIDS = [
    ("Voice AI: monetising voice at scale with new intelligent services – Interview with Tallence", "Interview", "2026/06/Screenshot-2026-06-19-at-13.02.41-1068x668.jpg"),
    ("Beyond AIOps: How knowledge-driven agentic AI enables autonomous network operations", "Interview", "2026/04/Screenshot-2026-04-13-at-10.38.50-1068x668.jpg"),
    ("MWC26: Beyond Cloud-Native – How Wind River Is Accelerating Telco Growth", "MWC26", "2026/03/Screenshot-2026-03-27-at-09.50.41-1068x668.jpg"),
    ("MWC26: Private 5G Networks – Druid Software discuss the future of the market", "MWC26", "2026/03/Screenshot-2026-03-26-at-16.11.42-1068x668.jpg"),
    ("MWC26: Infovista on how Agentic AI is reframing network intelligence", "MWC26", "2026/03/Screenshot-2026-03-23-at-16.42.19-1068x668.jpg"),
    ("MWC26: How Netcracker is Helping Telcos Advance Agentic AI", "MWC26", "2026/03/Screenshot-2026-03-20-at-16.31.23-1068x608.jpg"),
    ("MWC26: From Automation to Agentic Cloud – How Cloud Operations Are Evolving", "MWC26", "2026/03/Screenshot-2026-03-16-at-18.24.19-1068x639.jpg"),
    ("MWC26: Interview with Jonas Lagerquist, Director Product Management, Enea", "MWC26", "2026/03/Screenshot-2026-03-12-at-15.24.01-1068x651.jpg"),
    ("MWC26: From AI vision to Agentic Reality: Amdocs’ Vision for the Future of Telecom", "MWC26", "2026/03/Screenshot-2026-03-12-at-15.16.48-1068x606.jpg"),
    ("MWC26: Interview with Marcin Kaleta, CEO of Comarch Communications", "MWC26", "2026/03/Screenshot-2026-03-12-at-15.06.45-1068x683.jpg"),
    ("Modern OSS/BSS are the key to monetising 5G", "Webinar", "2025/12/Erisson-webinar-dec-2025-vid2-v1-2-1068x601.jpg"),
    ("BSS is the foundation for monetising 5G and fuelling growth beyond connectivity", "Webinar", "2025/12/Ericsson-webinar-DEC25-1-v1--1068x601.jpg"),
    ("Why small cells are set to become a big market", "Webinar", "2025/12/Mavenir-webinar-Nov25-v5--1068x601.jpg"),
    ("AI in Infrastructure 2025 | PANEL: Will AI deliver ROI on 5G?", "Panel", "2025/10/TE-infrastructure-SLIDES-v4_page-0009-1068x601.jpg"),
]
vid_cards = "".join(
    f'<a class="vid-card" href="#"><div class="vthumb"><img src="{U}{img}" alt=""><span class="play" aria-hidden="true"></span>'
    f'<span class="tag">{e(tag)}</span></div><h3>{e(t)}</h3></a>'
    for t, tag, img in VIDS
)
vid_body = f"""
      <a class="vid-hero" href="#">
        <div class="vthumb"><img src="{U}2026/09/Octave-ME-Sept26-1-1068x601.jpg" alt=""><span class="play big" aria-hidden="true"></span></div>
        <div class="txt">
          <div class="kick">Latest video · Partner video</div>
          <h2>Moving from asset-centric to flow-driven network operations: interview with Jean-Francois Allard from Octave</h2>
          <p>Telecom network management is shifting from an asset-centric to a flow-centric approach. What does that mean for operators?</p>
        </div>
      </a>
      <div class="sh" style="margin-top:34px"><h2>More videos</h2></div>
      <div class="vid-grid">{vid_cards}</div>
      <div style="text-align:center;margin-top:30px"><a class="btn ghost" href="#">Load more</a></div>"""
block_page("videos", "Videos",
           "Interviews, event coverage, webinars and panel sessions from Mobile Europe.",
           ["All videos", "Interviews", "MWC26", "Webinars", "Panels"], vid_body, NB_CARD)

# Events ---------------------------------------------------------------------
UPCOMING = [
    ("24 Nov 2026", "AI in Network Optimisation: Finding Forgotten Revenue", "The Briefing · Online", "2026/10/ME-BRIEFING-AI3-ADS-2-v1--600x350.jpg", "briefing-event.html", "brief"),
    ("10 Dec 2026", "Telecoms in Focus", "Mobile Europe event", "2026/07/TELECOMS-FOCUS-logo-event2-600x350.jpg", "#", "me"),
]
ONDEMAND = [
    ("12 Nov 2026", "Can a cloud- and AI-native operator exist?", "2026/10/ME-BRIEFING-cloud2-ADS-v1--600x350.jpg"),
    ("27 Oct 2026", "Does 5G Standalone stand up – is the support role of digital twins key?", "2026/07/ME-BRIEFING-5G-4-ADS-v1-600x350.jpg"),
    ("1 Oct 2026", "Digital sovereignty in telecoms", "2026/07/ME-BRIEFING-SECURITY-2-ADS-v1-600x350.jpg"),
    ("24 Sep 2026", "How telcos can close the cybersecurity gap for small businesses", "2026/07/ME-BRIEFING-SECURITY-1-ADS-v1A-600x350.jpg"),
    ("9 Jul 2026", "Separating telco AI milestones from moonshots", "2026/06/ME-BRIEFING-TELCO-2-ADS-v1-600x350.jpg"),
    ("2 Jul 2026", "How has the techco destination changed?", "2026/05/ME-BRIEFING-TELCO-ADS-v1--600x350.jpg"),
    ("4 Jun 2026", "Transforming enterprises with Private 5G", "2026/04/ME-BRIEFING-5G-1-ADS-v1-2-600x350.jpg"),
    ("28 May 2026", "Adventures in 5G Standalone", "2026/04/ME-BRIEFING-5G-1-ADS-v1--600x350.jpg"),
    ("30 Apr 2026", "What telcos need to achieve with cloud", "2026/02/ME-BRIEFING-cloud1-ADS-v1-2-600x350.jpg"),
]
INDUSTRY = [
    ("6 Nov 2026", "Telco Days 2026: Roadmap to Agentic AI and Safer Networks", "Online · Software Mind", "2026/09/telco-days-sept26.jpg"),
    ("13–15 Oct 2026", "Where Telcos, AI & Networks Converge", "Network X · VIECON, Vienna", "2026/08/networkx-aug26-600x350.jpg"),
]
up_cards = "".join(
    f'<a class="ev-card {kind}" href="{href}"><div class="ethumb"><img src="{U}{img}" alt=""></div>'
    f'<div class="etxt"><div class="edate">{e(d)}</div><h3>{e(t)}</h3><div class="ewhere">{e(w)}</div>'
    f'<span class="ecta">{"Register free →" if kind == "brief" else "View details →"}</span></div></a>'
    for d, t, w, img, href, kind in UPCOMING
)
od_cards = "".join(
    f'<a class="ev-card od" href="#"><div class="ethumb"><img src="{U}{img}" alt=""><span class="play" aria-hidden="true"></span></div>'
    f'<div class="etxt"><div class="edate">The Briefing · {e(d)}</div><h3>{e(t)}</h3><span class="ecta">Watch on demand →</span></div></a>'
    for d, t, img in ONDEMAND
)
ind_cards = "".join(
    f'<a class="ev-card ind" href="#"><div class="ethumb"><img src="{U}{img}" alt=""></div>'
    f'<div class="etxt"><div class="edate">{e(d)}</div><h3>{e(t)}</h3><div class="ewhere">{e(w)}</div><span class="ecta">View details →</span></div></a>'
    for d, t, w, img in INDUSTRY
)
ev_body = f"""
      <div class="ev-pinned">
        <a class="ev-pin-card" href="#">
          <div class="ethumb"><img src="{U}2026/11/mwc27-Event-Theme-cropped.jpg" alt="MWC27"></div>
          <div class="etxt">
            <div class="sp-top"><span class="sp-label">Sponsored</span><span class="pin-inline" data-pin>Pinned post</span></div>
            <div class="edate">1–4 March 2027 · Fira Gran Via, Barcelona</div>
            <h3>MWC Barcelona 2027</h3>
            <p>The world’s largest connectivity event. Meet the Mobile Europe team on site, and follow our live coverage, interviews and video from the show floor.</p>
            <span class="btn red">View event details</span>
          </div>
        </a>
        <a class="pin-cta" href="#" data-pin-cta>Pin your event here →</a>
      </div>
      <div class="sh"><h2>Upcoming &amp; featured</h2><a href="the-briefing.html">All Briefings</a></div>
      <div class="ev-grid two">{up_cards}</div>
      <div class="sh"><h2>On demand</h2><a href="#">All on-demand events</a></div>
      <div class="ev-grid">{od_cards}</div>
      <div class="sh"><h2>Industry events</h2><a href="#">List your event</a></div>
      <div class="ev-grid">{ind_cards}</div>"""
block_page("events", "Events",
           "Mobile Europe’s live Briefings and Telecoms in Focus, on-demand sessions, and the industry events we’re attending.",
           ["All events", "The Briefing", "Telecoms in Focus", "On demand", "Industry events"], ev_body, NB_CARD)

print("Wrote:", ", ".join(p + ".html" for p in ["insights", "cxo", "white-papers", "videos", "events"]))
