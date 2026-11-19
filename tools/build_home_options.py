"""Version 2: homepage options built around people meeting at Mobile Europe's Briefings and events.

Run from the repo root:  python3 tools/build_home_options.py
Writes me-redesign-v2/home-voices.html (A), home-agenda.html (B) and home-room.html (C).
All names, roles, quotes, photos and stories are real, taken from mobileeurope.co.uk.
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "me-redesign-v2"
U = "https://www.mobileeurope.co.uk/wp-content/uploads/"
V = "?v=80"


def e(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- people (real speakers)
BRIEFING = [  # The Briefing, 24 Nov 2026: AI in Network Optimisation
    ("Jasdip Sensi", "Editor", "Mobile Europe", "2026/07/Jasdip-Sensi-300x300.jpg"),
    ("David Palmer", "Strategy & Innovation Lead", "Stonesthro", "2026/11/David-Palmer-1-150x150.jpg"),
    ("Larbi Belkhit", "Principal Analyst", "ABI Research", "2026/07/Larbi-Belkhit-1010x1024.jpg"),
    ("Nektaria Efthymiou", "Network Platform & Security Research Director", "BT", "2026/10/Nektaria-Efthymiou.jpg"),
    ("Andy Linham", "Principal Strategy Manager", "Vodafone Business", "2026/06/Andy-Linham-1024x1024.jpg"),
    ("Prasenjit Sinha", "Head of Product", "Anritsu", "2026/08/Prasenjit-Sinha.jpg"),
    ("Brian Murray", "Head of Marketing", "Anritsu", "2026/08/Brian-Murray.jpg"),
]
TIF = [  # Telecoms in Focus, 10 Dec 2026
    ("Colin Bannon", "CTO", "BT Business", "2025/12/Colin-Bannon-150x150.jpg"),
    ("Philippe Ensarguet", "VP Cloud & Software Engineering", "Orange", "2025/11/Philippe-Ensarguet-150x150.jpg"),
    ("Francesca Serravalle", "Head of Network Monetisation Strategy", "Vodafone", "2026/10/Francesca-Serravalle-150x150.jpg"),
    ("Antonietta Mastroianni", "CIO UAE", "e&", "2026/09/Antonietta-Mastroianni-150x150.jpg"),
    ("Mariam Kaynia", "Chief Data & Information Officer", "Eutelsat", "2026/11/Mariam-Kaynia-150x150.jpg"),
    ("George Robinson", "Head of Government Affairs", "VodafoneThree", "2026/11/George-Robinson-150x150.jpg"),
    ("Kenneth Hardat", "Head of Strategy & Product", "Proximus Global", "2026/11/Kenneth-Hardat-150x150.jpg"),
    ("Martin Rückert", "Chief AI Officer", "Tallence", "2026/10/Martin-Ruckert-150x150.jpg"),
    ("Osvaldo Aldao", "CTO", "ENEA", "2026/11/Osvaldo-Aldao-150x150.jpg"),
    ("Tom Rebbeck", "Research Partner", "Analysys Mason", "2026/09/Tom-Rebbeck-150x150.webp"),
    ("Phil Laidler", "MD, Consulting", "STL Partners", "2026/09/Phil-Laidler-150x150.jpg"),
    ("Robert Curran", "Consulting Analyst", "Appledore Research", "2026/07/Robert-Curran-150x150.jpg"),
    ("Bruno Silva Santos", "Executive Director", "Celfocus", "2026/10/Bruno-Santos-150x150.jpg"),
    ("Rimma Iontel", "Senior Principal Chief Architect", "Red Hat", "2026/11/Rimma-Iontel-150x150.jpeg"),
    ("Aleksandar Gichevski", "Head of IT Services & Architecture", "A1 Telekom Austria", "2026/09/Aleksandar-Gichevski-150x150.png"),
]
P = {p[0]: p for p in BRIEFING + TIF}

# ---------------------------------------------------------------- real quotes from Mobile Europe interviews
QUOTES = [
    ("The future of AI won’t just be about building bigger infrastructure. It will be about deploying the right infrastructure in the right places.",
     "Rob Coupland", "CEO, Pulsant", "2026/11/Rob-Coupland-ME.png"),
    ("AI-RAN represents an exciting next step in the evolution of our network, using AI to make connectivity more intelligent, responsive and efficient.",
     "Iain Milligan", "Network Development & Infrastructure Director, VodafoneThree", None),
    ("This collaboration with VodafoneThree is an important step in moving AI-RAN from industry ambition toward commercial reality.",
     "Emma Falck", "President of Mobile Infrastructure, Nokia", None),
    ("Real businesses doing real things, without fanfare, are driving transformation, including in traditional segments of the UK economy.",
     "Rob Coupland", "CEO, Pulsant", "2026/11/Rob-Coupland-ME.png"),
]

MPU = '<div><div class="ad-label">Advertisement</div><div class="ad ad-mpu">MPU {n}<small>300×250 · GAM</small></div></div>'
BB = '<div class="bb-zone"><div class="ad-label">Advertisement</div><div class="ad ad-bb">Billboard (BB)<small>970×250 · GAM · 300×250 on mobile</small></div></div>'
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Mobile Europe mockup</title>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto:wght@300;400;500;600;700;800&family=Roboto+Slab:wght@400;500;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css{v}">
</head>
<body data-page="home">
<div id="site-header"></div>
"""
FOOT = """
<div id="site-footer"></div>
<script src="shared.js{v}"></script>
</body>
</html>
"""


def initials(name):
    return "".join(w[0] for w in name.split()[:2])


def face(name, size="m", show_role=True):
    n, role, org, img = P[name]
    pic = f'<img src="{U}{img}" alt="">' if img else f'<span class="ini">{initials(n)}</span>'
    meta = f'<small>{e(role)}</small><em>{e(org)}</em>' if show_role else f'<em>{e(org)}</em>'
    return f'<div class="face {size}"><span class="fpic">{pic}</span><b>{e(n)}</b>{meta}</div>'


def stack(names, more=None):
    pics = "".join(f'<span class="sp" title="{e(P[n][0])}, {e(P[n][2])}"><img src="{U}{P[n][3]}" alt=""></span>' for n in names)
    extra = f'<span class="sp more">+{more}</span>' if more else ""
    return f'<span class="stack">{pics}{extra}</span>'


def card(t, img, tag, date, cls="card"):
    return (f'<a class="{cls}" href="article.html"><div class="pic"><img src="{U}{img}" alt="">'
            f'<span class="tag">{e(tag)}</span></div><h3>{e(t)}</h3><div class="date">{e(date)}</div></a>')


def quote_card(q, who, role, img, big=False):
    pic = f'<img src="{U}{img}" alt="">' if img else f'<span class="ini">{initials(who)}</span>'
    return (f'<figure class="qcard{" big" if big else ""}"><blockquote>“{e(q)}”</blockquote>'
            f'<figcaption><span class="fpic">{pic}</span><span><b>{e(who)}</b><small>{e(role)}</small></span></figcaption></figure>')


def write(name, title, body):
    (OUT / name).write_text(HEAD.format(title=title, v=V) + body + FOOT.format(v=V))


# =====================================================================================
# Option A · Voices  (evolution: the current homepage + voices and faces)
# =====================================================================================
base = (OUT / "index.html").read_text()
voices = f"""
      <section class="voices">
        <div class="sh"><h2>Voices this week</h2><a href="insights.html">All interviews</a></div>
        <div class="voices-row">
          {quote_card(*QUOTES[0])}
          {quote_card(*QUOTES[1])}
          {quote_card(*QUOTES[2])}
        </div>
      </section>
"""
onstage = f"""
<section class="onstage">
  <div class="wrap">
    <div class="onstage-hd">
      <div><span class="kicker-w">Where the conversation goes live</span><h2>On stage next</h2></div>
      <a class="btn white" href="events.html">All events</a>
    </div>
    <div class="onstage-grid">
      <a class="os-card brief" href="briefing-event.html">
        <span class="os-when"><b>24</b>Nov</span>
        <div><small>The Briefing · Online · 09:30 GMT</small><h3>AI in Network Optimisation: Finding Forgotten Revenue</h3>
        <div class="os-faces">{''.join(face(n, 's', False) for n in ['Nektaria Efthymiou', 'Andy Linham', 'Larbi Belkhit', 'David Palmer'])}</div>
        <span class="os-cta">Join them live · Register free →</span></div>
      </a>
      <a class="os-card tif" href="events.html">
        <span class="os-when"><b>10</b>Dec</span>
        <div><small>Telecoms in Focus · Virtual conference</small><h3>2026 in focus, 2027 and beyond</h3>
        <div class="os-faces">{''.join(face(n, 's', False) for n in ['Colin Bannon', 'Philippe Ensarguet', 'Francesca Serravalle', 'Antonietta Mastroianni'])}</div>
        <span class="os-cta">{stack(['Mariam Kaynia', 'George Robinson', 'Kenneth Hardat', 'Tom Rebbeck', 'Phil Laidler'], 10)} and more speakers · Register →</span></div>
      </a>
    </div>
  </div>
</section>
"""
a = base.replace('<body data-page="home">', '<body data-page="home">', 1)
a = a.replace('      <div class="sh"><h2>More latest news</h2>', voices + '      <div class="sh"><h2>More latest news</h2>', 1)
a = a.replace('<!-- ===== INDEPENDENT RESEARCH BAND ===== -->', onstage + '\n<!-- ===== INDEPENDENT RESEARCH BAND ===== -->', 1)
a = a.replace('<title>Mobile Europe – Homepage mockup</title>', '<title>Option A · Voices – Mobile Europe mockup</title>')
a = re.sub(r'(styles\.css|shared\.js)\?v=\d+', lambda m: m.group(1) + V, a)
assert 'Voices this week' in a and 'On stage next' in a
(OUT / "home-voices.html").write_text(a)

# =====================================================================================
# Option B · The Agenda  (issue-led: stories + people + live event + report per issue)
# =====================================================================================
ISSUES = [
    {
        "kicker": "Burning issue #1", "title": "Finding the money in AI",
        "intro": "Operators have invested heavily in networks and data centres. Now they need AI to pay its way.",
        "lead": ("VodafoneThree, Nokia partner to trial AI-powered mobile networks", "2026/11/Nokia-VodafoneThree.png", "Automation/AI", "18 Nov 2026"),
        "more": [("Mavenir CRO on why AI is putting the mobile core back in focus", "2026/10/Dejan-Leskaoski.png", "Interview", "20 Oct 2026"),
                 ("Nokia, Nscale and Telia partner to build Nordic AI Gigafactory", "2026/11/Nokia-Telia.png", "Financial/Regulation", "16 Nov 2026")],
        "quote": QUOTES[1],
        "people": ["Nektaria Efthymiou", "Andy Linham", "Larbi Belkhit", "David Palmer"],
        "event": ("The Briefing · 24 Nov", "AI in Network Optimisation: Finding Forgotten Revenue", "briefing-event.html", "Register free"),
        "report": ("Agentic AI: Achieving autonomous network operations", "2026/03/ME-Report-Celfocus26-COVER.jpg"),
        "tone": "pink",
    },
    {
        "kicker": "Burning issue #2", "title": "Sovereignty, security and who you trust",
        "intro": "Networks are now critical national infrastructure, with governments and defence moving closer to operators.",
        "lead": ("Telefónica lands 5G contract for military defence centre in Slovakia", "2026/09/Telefonica-696x464.png", "Security", "12 Nov 2026"),
        "more": [("CrowdStrike launches sovereign cloud in Saudi Arabia", "2026/09/Saudi-Arabia-696x464.png", "Security", "9 Nov 2026"),
                 ("UK govt targets subsea cable threats with tougher penalties", "2026/07/subsea-cable-July-2026-AdobeStock_1722897327-Cropped-696x464.jpg", "Optical/IP", "26 Oct 2026")],
        "quote": None,
        "people": ["Robert Curran", "Colin Bannon", "Antonietta Mastroianni", "Osvaldo Aldao"],
        "event": ("Telecoms in Focus · 10 Dec", "Panel: Digital sovereignty, from policy debate to operational reality", "events.html", "Register"),
        "report": ("Advancing location intelligence for emergency services in Europe", "2025/06/ME-Report-SS8-COVER-TINT-v2-1024x724.jpg"),
        "tone": "navy",
    },
    {
        "kicker": "Burning issue #3", "title": "The AI infrastructure race",
        "intro": "Bigger campuses grab the headlines, but where should the capacity really go?",
        "lead": ("Data centres must look beyond the ‘bragawatts’ race, says Pulsant CEO", "2026/11/Rob-Coupland-ME.png", "Interview", "11 Nov 2026"),
        "more": [("Deutsche Telekom invests €250m to expand AI factory in Munich", "2026/11/DT.png", "Financial/Regulation", "10 Nov 2026"),
                 ("Amazon unveils €16bn investment in Germany for 2027", "2026/10/Amazon-Germany.png", "Automation/AI", "22 Oct 2026")],
        "quote": QUOTES[0],
        "people": ["Philippe Ensarguet", "Rimma Iontel", "Martin Rückert"],
        "event": ("Telecoms in Focus · 10 Dec", "Keynote: 2027 in focus, what awaits operators", "events.html", "Register"),
        "report": ("OSS: Why trusted data matters as a catalyst for AI modernisation", "2026/10/ME-Report-BLUEPLANET-COVER-v1.jpg"),
        "tone": "red",
    },
    {
        "kicker": "Burning issue #4", "title": "Where will growth come from?",
        "intro": "Consolidation, job cuts and new business models: can telecoms enter a new era of growth?",
        "lead": ("Can BT fix TalkTalk – and is the brand worth saving?", "2026/10/TalkTalk-BT-AI.png", "Analysis", "8 Oct 2026"),
        "more": [("Telia acquires Telavox’s Nordic MVNO business in $380m deal", "2026/11/Telia-ME.png", "Financial/Regulation", "12 Nov 2026"),
                 ("Report: VMO2 plans thousands of job cuts amid £22bn debt concerns", "2026/09/vmo2-virgin-media-o2-696x464.png", "Financial/Regulation", "2 Nov 2026")],
        "quote": None,
        "people": ["Tom Rebbeck", "Kenneth Hardat", "Mariam Kaynia", "Francesca Serravalle", "Bruno Silva Santos"],
        "event": ("Telecoms in Focus · 10 Dec", "Panel: 2026 and beyond, can telecoms enter a new era of growth?", "events.html", "Register"),
        "report": ("Solving the profit puzzle of P5G networks", "2026/03/ME-Report-Druid-COVER-v1.jpg"),
        "tone": "navy",
    },
]


def issue_block(i, x):
    q = quote_card(*x["quote"]) if x["quote"] else ""
    lt, li, ltag, ld = x["lead"]
    more = "".join(f'<a class="is-more" href="article.html"><img src="{U}{img}" alt=""><span><b>{e(t)}</b><small>{e(d)}</small></span></a>' for t, img, tag, d in x["more"])
    people = "".join(face(n, "s") for n in x["people"])
    ek, et, eh, ecta = x["event"]
    rt, rimg = x["report"]
    return f"""
  <section class="issue tone-{x['tone']}" id="issue-{i}">
    <div class="issue-hd"><span class="kicker">{e(x['kicker'])}</span><h2>{e(x['title'])}</h2><p>{e(x['intro'])}</p></div>
    <div class="issue-grid">
      <div class="is-news">
        <a class="is-lead" href="article.html"><span class="pic"><img src="{U}{li}" alt=""><span class="tag">{e(ltag)}</span></span><b>{e(lt)}</b><small>{e(ld)}</small></a>
        <div class="is-list">{more}</div>
        {q}
      </div>
      <div class="is-people">
        <h3>Who’s debating it</h3>
        <div class="faces-col">{people}</div>
        <a class="is-event" href="{eh}"><small>{e(ek)}</small><b>{e(et)}</b><span class="btn pink">{e(ecta)}</span></a>
        <a class="is-report" href="research.html"><img src="{U}{rimg}" alt=""><span><small>Independent Research</small><b>{e(rt)}</b></span></a>
      </div>
    </div>
  </section>"""


nav_issues = "".join(f'<a href="#issue-{i}"><span>#{i + 1}</span>{e(x["title"])}</a>' for i, x in enumerate(ISSUES))
latest = [("Orange pledges extra €250m to support emerging tech startups", "18 Nov"), ("SES, ITU expand partnership to improve digital education in Africa", "18 Nov"),
          ("Belgium confirms 2G shutdown plans for 2028/29", "17 Nov"), ("Orange Jordan replaces 17-year-old billing platform with Ericsson system", "17 Nov"),
          ("AO revives Phones4u after 12-year absence", "17 Nov"), ("MTN exits Syrian market as Zain prepares to take over", "16 Nov"),
          ("Nokia to develop ISAC technology for US military drone detection project", "16 Nov")]
latest_html = "".join(f'<a href="article.html"><time>{d}</time><b>{e(t)}</b></a>' for t, d in latest)
b_body = f"""
<main class="wrap">
  <section class="agenda-hero">
    <div><span class="kicker">The Mobile Europe agenda · week of 16 November</span>
      <h1>The issues telecoms leaders are debating right now</h1>
      <p>Our reporting, the people on stage at our Briefings and events, and the research behind the arguments, organised by the questions that matter.</p></div>
    <nav class="issue-nav" aria-label="This week's issues">{nav_issues}</nav>
  </section>

  <div class="with-rail agenda-layout">
    <div>{''.join(issue_block(i, x) for i, x in enumerate(ISSUES[:2]))}</div>
    <aside class="rail"><div class="sticky">
      {MPU.format(n=1)}
      <div class="latest-box"><h3>Latest news</h3>{latest_html}<a class="all" href="news.html">All news →</a></div>
      {MPU.format(n=2)}
    </div></aside>
  </div>
</main>
{BB}
<main class="wrap">
  <div class="with-rail agenda-layout">
    <div>{''.join(issue_block(i + 2, x) for i, x in enumerate(ISSUES[2:]))}</div>
    <aside class="rail"><div class="sticky">{MPU.format(n=3)}{MPU.format(n=4)}</div></aside>
  </div>
</main>
"""
write("home-agenda.html", "Option B · The Agenda", b_body)

# =====================================================================================
# Option C · The Room  (event-led: who you'll meet, then the news)
# =====================================================================================
wall = "".join(face(n[0], "m") for n in TIF[:12])
c_body = f"""
<section class="room-hero">
  <div class="wrap">
    <div class="rh-copy">
      <span class="kicker-w">Mobile Europe · Briefings &amp; events</span>
      <h1>Where telecoms leaders meet to settle the big questions</h1>
      <p>Operators, vendors and analysts, live and on the record. Read the news, then come and argue it out.</p>
      <div class="rh-next">
        <a class="rh-ev" href="briefing-event.html"><small>Next · The Briefing · Tue 24 Nov, 09:30 GMT</small><b>AI in Network Optimisation: Finding Forgotten Revenue</b>
          <span class="rh-row">{stack(['Nektaria Efthymiou', 'Andy Linham', 'Larbi Belkhit', 'David Palmer', 'Prasenjit Sinha'])}<span>BT, Vodafone Business, ABI Research and more</span></span>
          <span class="btn white">Register free</span></a>
        <div class="count" data-cd></div>
      </div>
    </div>
    <div class="rh-wall">
      <div class="rh-wall-hd"><b>On stage at Telecoms in Focus</b><span>10 December · Virtual</span></div>
      <div class="wall">{wall}</div>
      <a class="rh-wall-cta" href="events.html">See all speakers and register →</a>
    </div>
  </div>
</section>

<main class="wrap">
  <div class="with-rail" style="margin-top:30px">
    <div>
      <div class="sh" style="margin-top:0"><h2>Today’s agenda</h2><a href="news.html">All news</a></div>
      <div class="lead">
        <a class="lead-main" href="article.html">
          <div class="pic"><img src="{U}2026/11/Rob-Coupland-ME.png" alt=""><span class="tag ins">Interview</span></div>
          <h1>Data centres must look beyond the ‘bragawatts’ race, says Pulsant CEO</h1>
          <p>The data centre industry has become “obsessed with bragawatts” and the race to build bigger AI campuses, according to Pulsant CEO Rob Coupland.</p>
          <div class="date">11 November 2026</div>
        </a>
        <div class="lead-side">
          {card('Orange pledges extra €250m to support emerging tech startups', '2022/09/Orange-Spain-Metaverse-Shop-e1666341211856-1068x661.png', 'Financial/Regulation', '18 Nov 2026')}
          {card('VodafoneThree, Nokia partner to trial AI-powered mobile networks', '2026/11/Nokia-VodafoneThree.png', 'Automation/AI', '18 Nov 2026')}
          {card('Belgium confirms 2G shutdown plans for 2028/29', '2026/11/Belgium.png', '5G & Beyond', '17 Nov 2026')}
        </div>
      </div>
    </div>
    <aside class="rail">{MPU.format(n=1)}</aside>
  </div>

  <section class="heard">
    <div class="sh"><h2>Heard at Mobile Europe</h2><a href="insights.html">All interviews</a></div>
    <div class="heard-grid">
      {quote_card(*QUOTES[0], big=True)}
      <div class="heard-side">{quote_card(*QUOTES[1])}{quote_card(*QUOTES[2])}</div>
    </div>
  </section>
</main>
{BB}
<main class="wrap">
  <div class="with-rail">
    <div>
      <div class="sh" style="margin-top:0"><h2>The questions on stage</h2><a href="events.html">Full programmes</a></div>
      <div class="qs">
        <a class="q-item" href="briefing-event.html"><span class="q-date"><b>24</b>Nov</span><span><small>The Briefing · Panel</small><b>Where we are today: successes, challenges and future opportunities for AI</b>{stack(['Larbi Belkhit', 'Nektaria Efthymiou', 'Andy Linham', 'Brian Murray'])}</span></a>
        <a class="q-item" href="events.html"><span class="q-date"><b>10</b>Dec</span><span><small>Telecoms in Focus · Panel</small><b>Digital sovereignty: from policy debate to operational reality</b>{stack(['Robert Curran', 'Colin Bannon', 'Antonietta Mastroianni', 'Osvaldo Aldao'])}</span></a>
        <a class="q-item" href="events.html"><span class="q-date"><b>10</b>Dec</span><span><small>Telecoms in Focus · Panel</small><b>2026 and beyond: can telecoms enter a new era of growth?</b>{stack(['Tom Rebbeck', 'Kenneth Hardat', 'Mariam Kaynia', 'Francesca Serravalle', 'Bruno Silva Santos'])}</span></a>
        <a class="q-item" href="events.html"><span class="q-date"><b>10</b>Dec</span><span><small>Telecoms in Focus · Panel</small><b>The road to 6G: evolution rather than revolution?</b>{stack(['Phil Laidler', 'George Robinson', 'Rimma Iontel'])}</span></a>
      </div>

      <div class="sh"><h2>More latest news</h2><a href="news.html">All news</a></div>
      <div class="grid3">
        {card('SES, ITU expand partnership to improve digital education in Africa', '2026/11/SES.png', 'Middle East & Africa', '18 Nov 2026')}
        {card('Orange Jordan replaces 17-year-old billing platform with Ericsson system', '2025/03/Orange-poland-AdobeStock_833458545.jpeg', 'BSS/OSS/CX', '17 Nov 2026')}
        {card('Nokia to develop ISAC technology for US military drone detection project', '2026/09/Nokia-defence.png', 'RAN', '16 Nov 2026')}
      </div>
    </div>
    <aside class="rail"><div class="sticky">{MPU.format(n=2)}{MPU.format(n=3)}</div></aside>
  </div>

  <div class="sh"><h2>People in the news</h2><a href="cxo.html">CxO Zone</a></div>
  <div class="grid4 people-news">
    {card('Google poaches Samsung VP Annika Bizon to lead TMT team', '2026/11/Google-Annika-Bizon.png', 'Appointment', '6 Nov 2026')}
    {card('Telus names ex-EE and ex-KPMG chiefs to board', '2026/11/Telus.png', 'Boardroom', '9 Nov 2026')}
    {card('Celfocus’ Carla Penedo joins Mobile Europe’s Editorial Advisory Board', '2026/11/CELFOCUS-.png', 'Appointment', '4 Nov 2026')}
    {card('Telenet CEO John Porter exits after 13 years', '2026/10/TELENET-CEO.png', 'Leadership', '15 Oct 2026')}
  </div>
</main>
"""
write("home-room.html", "Option C · The Room", c_body)
print("Wrote home-voices.html, home-agenda.html, home-room.html")
