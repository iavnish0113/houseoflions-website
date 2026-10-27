#!/usr/bin/env python3
"""Builds the House of Lions static site (content taken from houseoflions.in).

  python3 build.py            -> writes the pages into ./ (GitHub Pages ready)
  python3 build.py --preview  -> also writes ./_preview/ for the Claude artifact preview
"""
import math, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
V = "6"  # bump to bust browser caches after CSS/JS changes

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@300..700&display=swap">')

NAV = [("about.html", "About", "about"), ("solutions.html", "Solutions", "solutions"),
       ("insights.html", "Insights", "insights"), ("contact.html", "Contact", "contact")]

EMAIL = "amit@houseoflions.in"
PHONE = "+91 88829 77667"
PHONE_TEL = "+918882977667"
CONSULT = "+91 99994 92649"
CONSULT_TEL = "+919999492649"
LINKEDIN = "https://www.linkedin.com/company/houseoflions/"
INSTAGRAM = "https://www.instagram.com/houseoflions_consultancy/"
FACEBOOK = "https://www.facebook.com/www.houseoflions.net"
PORTFOLIO = "https://www.houseoflions.in/_files/ugd/04e63d_a045211deaec47aa8413aea8f163c6d7.pdf"
PROFILE = "https://www.houseoflions.in/_files/ugd/04e63d_12c48e3e2cae4ffea04cd1f5bf3c1c03.pdf"

# ---------- Images (served from the existing Wix media library, cropped/resized on the fly) ----------
def wix(mid, w, h, name="img.jpg"):
    return f"https://static.wixstatic.com/media/{mid}/v1/fill/w_{w},h_{h},al_c,q_85,enc_auto/{name}"

LOGO = ("https://static.wixstatic.com/media/04e63d_7d29c68701a64dadaddee5354e5945ee~mv2.png"
        "/v1/crop/x_148,y_370,w_710,h_337/fill/w_420,h_199,al_c,q_95,enc_auto/house-of-lions-logo.png")
IMG = {
    "lounge": "14fa59_f99e2ea1f4354d7e83e3adb6ec6ddd5d~mv2.jpeg",
    "plants": "14fa59_6ecb2494b52748908ec6164873610f17~mv2.jpeg",
    "mural": "14fa59_0c7e75a9db2d4aa9ba33d9058c2e7819~mv2.jpeg",
    "cafe": "14fa59_b28b664203f041388d007f3ee7823721~mv2.jpg",
    "floor": "04e63d_fe3a8106897b4e4f9944d8b4ad260d3f~mv2.jpg",
    "reception": "14fa59_6893c5d2d56e4da491b873346fa76cc8~mv2.jpg",
    "tiger": "14fa59_0c31d828c88c47c6a62fa3ec0a610676~mv2.jpeg",
    "bw1": "14fa59_bb8df49b9d04365bbdfd101c73ea54b~mv2.jpg",
    "bw2": "14fa59_209bae400b514ea687ceccf6038f314c~mv2.jpg",
    "amit": "04e63d_7351255698e243cc9eac6503fb4d2f06~mv2.png",
    "yukti": "04e63d_474b5f89ec844f8faf6a9a6cc9f05b69~mv2.jpeg",
    "sameer": "04e63d_ca46727cd58c4b22b503e96c1ca0f475~mv2.jpg",
    "anita": "04e63d_f9ab37bd5108455fa85941f740cedf92~mv2.jpeg",
    "akhil": "04e63d_66fefaf928e64272ae14b50343b3639f~mv2.jpeg",
    "divya": "04e63d_2d7628466fb148599c7b3e8e73247460~mv2.jpg",
    "narula": "04e63d_573df02858374016bc5109844fffe893~mv2.jpg",
    "upadhyay": "14fa59_2464f1f539a44382820a37266ee9fa08~mv2.jpg",
    "nikhil": "55b722_5997bfa594874080aa13cbb5b6d0451b~mv2.jpeg",
    "mukherjee": "14fa59_210351912893464e8adfffbf5c9019b6~mv2.jpg",
    "cubhouse": "04e63d_50a37c45830349f9b2ae4c87c3eb5a46~mv2.png",
    "mavcomm": "04e63d_3580eb47773346d29363e4734c2e8035~mv2.png",
    "tabb": "04e63d_30a52f84018545f78e835a8e20dae1b8~mv2.png",
}


def photo(key, w, h, alt, cls="ph", eager=False):
    return (f'<div class="{cls}"><img src="{wix(IMG[key], w, h)}" alt="{alt}" width="{w}" height="{h}"'
            f'{"" if eager else " loading=\"lazy\""} decoding="async"></div>')


def header(active):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    mlinks = "".join(
        f'<li><a href="{h}">{t}<span>0{i + 1}</span></a></li>' for i, (h, t, k) in enumerate(NAV))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="./" aria-label="House of Lions, home"><img src="{LOGO}" alt="House of Lions" width="420" height="199"></a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <a class="nav-cta" href="contact.html"><span class="dot" aria-hidden="true"></span>Contact us</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu"><span class="label">Menu</span><span class="bars" aria-hidden="true"></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <ul><li><a href="./">Home<span>00</span></a></li>{mlinks}</ul>
  <div class="mm-foot"><span>{EMAIL}</span><span>{PHONE}</span><span>Delhi, Gurugram, Mumbai, Paris</span></div>
</div>'''


def closing():
    return f'''<section class="band band-ink closing" aria-labelledby="closing-title">
  <div class="wrap grid">
    <div class="closing-left">
      <p class="eyebrow">Brands boldly amplified</p>
      <h2 id="closing-title">Scripting <em>success.</em></h2>
    </div>
    <div class="closing-right">
      <p>Call for a free consultation</p>
      <p class="phone">{CONSULT}</p>
      <div class="dl-row"><a class="btn" href="contact.html">Contact us <span class="arr" aria-hidden="true">&#8599;</span></a><a class="link-arrow" href="{PORTFOLIO}" target="_blank" rel="noopener">Download portfolio <span class="arr" aria-hidden="true">&#8599;</span></a></div>
      <div class="mane-panel"><canvas aria-hidden="true"></canvas><p class="mane-caption"><span>Move to wake the lion. Tap to roar.</span></p></div>
    </div>
  </div>
</section>'''


def footer():
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t, k in [("./", "Home", "")] + NAV)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-col"><img class="foot-logo" src="{LOGO}" alt="House of Lions" width="420" height="199" loading="lazy"></div>
      <div class="foot-col"><h4>Address</h4><address>1st Floor, VI John Tower<br>393, Udyog Vihar Phase 3 Road<br>Phase II, Udyog Vihar, Sector 20<br>Gurugram, Haryana 122016</address></div>
      <div class="foot-col"><h4>Talk to us</h4><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="tel:{CONSULT_TEL}">{CONSULT}</a></div>
      <div class="foot-col"><h4>Explore</h4>{nav}<span style="height:8px"></span><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram</a><a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a></div>
    </div>
    <div class="foot-mark" aria-hidden="true">House of <em>Lions</em></div>
    <div class="foot-bottom"><span>&copy; <span data-year>2026</span> House of Lions. Delhi, Gurugram, Mumbai, Paris.</span><span>Scripting success</span></div>
  </div>
</footer>'''


def page(slug, title, desc, body, active=None):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{LOGO}">
<meta name="theme-color" content="#F0ECE4">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/style.css?v={V}">
</head>
<body class="p-{slug}">
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/main.js?v={V}"></script>
</body>
</html>
'''


# ---------- Client-story art (no project photography exists on the old site) ----------
def contours():
    paths = []
    for k in range(14):
        pts = []
        base = 40 + k * 34
        for j in range(0, 361, 6):
            a = math.radians(j)
            r = base * (1 + 0.13 * math.sin(3 * a + k * .55) + 0.07 * math.sin(5 * a - k * .3))
            pts.append((560 + math.cos(a) * r * 1.35, 230 + math.sin(a) * r))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
        op = .55 if k % 4 else .95
        paths.append(f'<path d="{d}" fill="none" stroke="#EFE8D8" stroke-opacity="{op}" stroke-width="{1.6 if k % 4 == 0 else 1}"/>')
    return f'<svg viewBox="0 0 700 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{"".join(paths)}<circle cx="560" cy="230" r="6" fill="#F4A51C"/></svg>'


ART = {
    "vibes": lambda: '<div class="art art-vibes" role="img" aria-label="Vibes: soft glowing forms in blush and lilac"><span class="tag">Client: Vibes</span><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span><span class="big"><small>Clinics across India and Bangladesh</small>31</span></div>',
    "monteria": lambda: f'<div class="art art-monteria" role="img" aria-label="Monteria Village: topographic contour lines on forest green"><span class="tag">Client: Monteria Village</span>{contours()}<span class="big"><small>Acres, near Mumbai</small>36</span></div>',
    "baxy": lambda: '<div class="art art-baxy" role="img" aria-label="Baxy: marigold road stripes and a wheel on cobalt"><span class="stripes"></span><span class="tag">Client: Baxy</span><span class="wheel"></span><span class="big"><small>Leader in three-wheelers</small>3</span></div>',
}

# Client stories: wording from houseoflions.in/solutions
STORIES = [
    dict(key="vibes", client="Vibes", sector="Beauty and wellness",
         about="VIBES is a leading beauty and wellness brand with 31 clinics across India and Bangladesh. With a mix of offerings, it is one of the fastest-growing brands in its vertical.",
         challenge="The beauty and wellness market is a cluttered one. With no or less brand differentiator, the price point was the only crucial factor. Vibes was struggling to engage and differentiate.",
         solution="We implemented a comprehensive range of initiatives, including a refreshed branding approach, a go-to-market (GTM) plan, established rules of engagement, and various forms of content such as reels and bytes. We also conducted influencer campaigns, gathered testimonials and employed innovative creative strategies alongside a robust digital marketing effort."),
    dict(key="monteria", client="Monteria Village", sector="Hospitality",
         about="India’s first sustainable, eco-friendly village retreat offering curated traditional experiences. Spread over 36 acres near Mumbai, Monteria Village is a journey that takes you back to your roots.",
         challenge="Despite heavy foot traffic from schools, it did not attract many weekend travellers or corporates looking for off-site events and launches. It suffered from poor positioning and lacked motivation for the desired target audience.",
         solution="A new positioning statement that placed the brand firmly and securely as a must-visit destination. We also revamped the GTM plan, brand manual, marcom templates, and their website and digital presence."),
    dict(key="baxy", client="Baxy", sector="Automotive",
         about="A leading name in three-wheelers, recognised as an industry leader in India. Their vehicles deliver on the promise of highest fuel efficiency, low maintenance, load-carrying ability and cost effectiveness.",
         challenge="Baxy was experiencing a glass ceiling. Inconsistent branding efforts hindered its ability to gain substantial traction, and the absence of a comprehensive long-term brand roadmap affected its organic growth.",
         solution="We provided the brand with a refreshed identity, incorporating a new colour scheme, typography and comprehensive guidelines, maintaining symmetry across platforms, from the showroom to the service centre and from print to digital. The initiative was positively received and resulted in favourable outcomes for their financial performance."),
]

# Services: wording from the houseoflions.in homepage ("Breaking through the noise")
SERVICES = [
    ("Personal Branding", "Own your spotlight with our well-crafted narratives that amplify your unique voice. Your brand isn’t just personal, it’s power. Let’s redefine your legacy.", "#E3DBCC", None),
    ("Branding", "Fearless identities that roar, fresh vibes and unstoppable energy. Let’s make your brand the king.", "#EBDCD3", None),
    ("Social Media", "Welcome to The Cub House, our social media agency. Strategy, creativity and swagger: your brand’s pride starts here.", "#F6D9A6", "The Cub House"),
    ("Performance Marketing", "Data-driven strategies, ROI-focused campaigns and relentless optimisation to maximise your growth. We don’t just market, we deliver measurable success. Let’s outperform.", "#DDE2E6", "TABB Solutions"),
    ("Public Relations", "Elevate your brand with our integrated PR endeavour: bold strategies, unmatched creativity and results-driven campaigns that amplify your story. Turning your vision into a global conversation.", "#E3DBCC", "Mavcomm"),
]

WHY = ["Exposure to managing global brands", "The right mix of IQ and EQ", "Integrated execution",
       "Strategically aggressive", "A perfect blend of youth and experience", "Pro-active, strategic with creative panache"]

QUOTES = [
    ("A highly energetic and passionate team always up for a new challenge, walking the extra mile to ensure seamless client servicing and delight!", "Yukti Nagpal", "Director, Gulshan Group", "yukti"),
    ("Their collaborative approach, open communication, and commitment to our success made working with them productive and enjoyable.", "Sameer Malhotra", "CEO, Shriram Automall", "sameer"),
    ("What sets them apart is their heart. They helped me find my voice, and I will always be grateful for that. Thank you for turning my dreams into reality!", "Anita Ajwani", "Founder, Memsaheb", "anita"),
]

# Non-political posts from houseoflions.in/insights
POSTS = [
    ("Are you vibing?", "Do you know Chris Martin? Or Guy Berryman? Or, for that matter, Will Champion? Yet the BookMyShow website and app crashed…", "Jan 8, 2025", "https://www.houseoflions.in/post/are-you-vibing"),
    ("Life, not a bed of roses", "SN Subrahmanyan, the Chairman and Managing Director of L&amp;T, a multi-billion-dollar conglomerate encompassing engineering, infrastructure…", "Jan 13, 2025", "https://www.houseoflions.in/post/life-not-a-bed-of-roses"),
    ("Mediocrity, thou art supreme", "It is in the air now. Mediocrity has straddled us and has seeped into our lives, making us emotionally, mentally and physically…", "Jan 8, 2025", "https://www.houseoflions.in/post/mediocrity-thou-art-supreme"),
]

MENTORS = [
    ("Akhil Bakhshi", "Creative Mentor", "An internationally acclaimed photographer, his career spans over 30 years in over 15 countries. He has worked with top agencies, brands and models.", "akhil"),
    ("Dr Divya Tanwar", "Empowerment Mentor", "A distinguished academician and cyber security specialist. A Professor (Adj) at Somaiya Vidyavihar University, Mumbai, with a PhD in Computer Science, MPhil, MCA, MTech and MBA. She has authored several books on MIS and database management systems.", "divya"),
    ("Siddharth Narula", "Business Mentor", "As Chief Revenue Officer at Zee Digital-OTT and Culture Machine, he has been at the forefront of the digital revolution. Successful stints at Walt Disney and Bloomberg UTV, and roles at CNBC, NDTV, ESPN and Sony TV.", "narula"),
    ("Siddhartha Upadhyay", "Creative Mentor", "Founder of Mavcomm Consulting, India’s premier PR consultancy, he has handled PR, image building and crisis management for leading national and multinational brands.", "upadhyay"),
    ("Nikhil Malhotra", "Digital Mentor", "A gifted entrepreneur and a deft digital marketeer with a keen interest in ROI. Apart from being the Co-founder of House of Lions, he also runs a successful fragrance brand, Air Roma.", "nikhil"),
    ("Amit Mukherjee", "Creative Mentor", "A brilliant brand and communication practitioner with an enviable pedigree. A Delhi College of Arts graduate, he has worked with India’s top agencies: Saatchi &amp; Saatchi, O&amp;M and Dentsu.", "mukherjee"),
]

SOP = ["Brand objective", "Audience insight mining", "Strategy development", "Story development", "Mood boards",
       "Design and content creation", "Execution", "Monitoring", "Review", "Reporting and recommendations"]


def services_list(link=True):
    out = ""
    for i, (name, text, tint, unit) in enumerate(SERVICES):
        note = f'<span class="cap-note">Delivered by {unit}</span>' if unit else ""
        out += f'''<li class="cap-row"><a href="{"solutions.html#services" if link else "contact.html"}" style="--tint:{tint}">
  <span class="cap-num">{i + 1:02d}</span>
  <span class="cap-title">{name}</span>
  <span class="cap-desc"><p>{text}</p>{note}</span>
  <span class="cap-arrow" aria-hidden="true">&#8599;</span>
</a></li>'''
    return out


def story_teaser(s, flip):
    return f'''<a class="case{" flip" if flip else ""}" href="solutions.html#{s["key"]}">
  <div class="case-art">{ART[s["key"]]()}</div>
  <div class="case-text">
    <p class="case-client">{s["sector"]}</p>
    <h3>{s["client"]}</h3>
    <p>{s["about"]}</p>
    <span class="link-arrow">Read the client story <span class="arr" aria-hidden="true">&#8599;</span></span>
  </div>
</a>'''


# ---------- HOME ----------
def home():
    tick = ["Brands boldly amplified", "Designing connections", "Communicate. Engage. Convert.", "Scripting success"]
    t = "".join(f'<span class="ticker-item">{x}<span class="x" aria-hidden="true">&#10033;</span></span>' for x in tick)
    stories = "".join(story_teaser(s, i % 2 == 1) for i, s in enumerate(STORIES))
    why = "".join(f'<li><span class="n">{i + 1:02d}</span><b>{w}</b></li>' for i, w in enumerate(WHY))
    voices = "".join(f'''<figure class="voice"><blockquote>“{q}”</blockquote>
<figcaption><img src="{wix(IMG[img], 160, 160)}" alt="{n}" width="56" height="56" loading="lazy"><span><b>{n}</b>{r}</span></figcaption></figure>''' for q, n, r, img in QUOTES)
    ins = "".join(f'<a href="{u}" target="_blank" rel="noopener"><span class="meta"><span>{d}</span><span>2 min read</span></span><h3>{h}</h3><p>{x}</p></a>' for h, x, d, u in POSTS)

    body = f'''
<section class="hero">
  <div class="wrap grid hero-grid">
    <div class="hero-copy">
      <p class="eyebrow rise">House of Lions &nbsp;/&nbsp; Brand and communication consultancy</p>
      <h1 class="rise d1">EV to café, beauty to real estate, Gurugram to <em>Paris.</em></h1>
      <p class="hero-sub rise d2">We are an Indian agency taking the world by storm.</p>
      <div class="actions rise d3">
        <a class="btn btn-primary" href="tel:{CONSULT_TEL}">Call for free consultation <span class="arr" aria-hidden="true">&#8599;</span></a>
        <a class="link-arrow" href="{PORTFOLIO}" target="_blank" rel="noopener">Download portfolio <span class="arr" aria-hidden="true">&#8599;</span></a>
      </div>
    </div>
    <div class="hero-aside rise d2">
      <div class="photo-stack">
        {photo("plants", 900, 1125, "The House of Lions studio in Gurugram", "p1", True)}
        {photo("mural", 600, 800, "Hand-painted portrait in the studio", "p2", True)}
      </div>
    </div>
  </div>
</section>

<div class="ticker" aria-label="Brands boldly amplified. Designing connections. Communicate. Engage. Convert. Scripting success.">
  <div class="ticker-track" aria-hidden="true">{t}{t}</div>
</div>

<section class="band band-ink section" aria-labelledby="amp-title">
  <div class="wrap grid statement">
    <div class="st-text">
      <p class="eyebrow">What we do</p>
      <h2 id="amp-title" class="d-xl">Brands boldly <em>amplified.</em></h2>
      <p class="big muted">Discover the art and science of crafting compelling narrative that sets the brand temperature soaring high, with better traction, engagement and ROI.</p>
      <div class="sub-statement"><h3>Designing connections</h3><p class="muted">Out-of-the-box, vertical defining and future ready.</p></div>
    </div>
    <div class="st-media">{photo("tiger", 900, 1125, "A bold tiger mural in the House of Lions studio")}</div>
  </div>
</section>

<section class="section" aria-labelledby="cec-title">
  <div class="wrap grid statement flip">
    <div class="st-text">
      <h2 id="cec-title" class="d-xl">Communicate. Engage. <em>Convert.</em></h2>
      <p class="big">As India’s leading integrated communication agency, we devise intricate and effective narrative that accentuates your brand growth and presence.</p>
      <div class="sub-statement"><h3>It’s simple…</h3><p class="muted">We are the new-age storytellers, adept at the art of creating compelling sagas, ensuring top-of-the-mind recall, engagement and traction.</p></div>
    </div>
    <div class="st-media"><div class="duo">{photo("lounge", 700, 875, "The studio lounge")}{photo("cafe", 600, 800, "The studio café")}</div></div>
  </div>
</section>

<section class="section band band-paper" id="services" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="svc-title" class="d-xl">Breaking through the <em>noise.</em></h2>
      <div class="intro"><a class="link-arrow" href="solutions.html">All solutions <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
    <ul class="cap-list">{services_list()}</ul>
  </div>
</section>

<section class="section" id="work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="work-title" class="d-xl">Client <em>stories.</em></h2>
      <p class="intro">We aim to overwhelm them with our IQ and EQ, going the extra mile every time and delivering every single time.</p>
    </div>
    <div class="work-list">{stories}</div>
  </div>
</section>

<section class="band band-sage section" aria-labelledby="why-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="why-title" class="d-xl">Why <em>us?</em></h2></div>
    <ul class="whyus">{why}</ul>
  </div>
</section>

<section class="section" aria-labelledby="founder-title">
  <div class="wrap grid founder">
    <div class="f-photo">{photo("amit", 900, 1125, "Amit Shankar, founder of House of Lions")}</div>
    <div class="f-text">
      <p class="eyebrow">Founder</p>
      <h2 id="founder-title" class="d-l">Amit Shankar</h2>
      <blockquote>Turning your brand narrative into big-stage success is his craft and forte.</blockquote>
      <p class="muted body-l">A master storyteller, he is a best-selling author and visiting faculty at top management and design institutes.</p>
      <div><a class="link-arrow" href="about.html#mentors">Meet our mentors <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
  </div>
</section>

<section class="section band band-paper" aria-labelledby="voice-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="voice-title" class="d-xl">It’s all about a <em>dialogue.</em></h2>
      <p class="intro">A few words from our clients.</p>
    </div>
    <div class="voices">{voices}</div>
  </div>
</section>

<section class="section" aria-labelledby="ins-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="ins-title" class="d-xl">Insights</h2>
      <div class="intro" style="display:grid;gap:18px;justify-items:start"><p>Short. Precise. Effective.</p><a class="link-arrow" href="insights.html">All insights <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
    <div class="ins">{ins}</div>
  </div>
</section>

{closing()}
'''
    return page("home", "House of Lions", "House of Lions is an integrated brand and communication consultancy. EV to café, beauty to real estate, Gurugram to Paris.", body, "home")


# ---------- ABOUT ----------
def about():
    sop = "".join(f'<li><span class="n">{i + 1:02d}</span><span>{s}</span></li>' for i, s in enumerate(SOP))
    m = "".join(f'''<article class="mentor"><div class="m-photo"><img src="{wix(IMG[k], 640, 800)}" alt="{n}" width="640" height="800" loading="lazy"></div><p class="role">{r}</p><h3>{n}</h3><p>{b}</p></article>''' for n, r, b, k in MENTORS)
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Our story</p>
    <h1 class="rise d1">India’s finest brand <em>storytellers.</em></h1>
    <div class="ph-copy rise d2">
      <p>Our communication is always rooted in insight, and we believe in telling stories that stand the test of time.</p>
      <p>Our team is the right mix of experience and adrenaline, sanity and bold moves.</p>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap photo-band">
    {photo("floor", 1400, 900, "The House of Lions studio floor")}
    {photo("reception", 700, 525, "Studio reception")}
    {photo("lounge", 700, 525, "Studio lounge")}
  </div>
</section>

<section class="band band-ink section" aria-labelledby="num-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="num-title" class="d-xl">Us in <em>numbers.</em></h2></div>
    <div class="facts" style="border-top-color:rgba(240,236,228,.4)">
      <div style="border-left-color:rgba(240,236,228,.14)"><b>4</b><span class="muted">Offices: Delhi, Gurugram, Mumbai and Paris</span></div>
      <div style="border-left-color:rgba(240,236,228,.14)"><b>4</b><span class="muted">Verticals</span></div>
      <div style="border-left-color:rgba(240,236,228,.14)"><b>100+</b><span class="muted">Campaign-experienced team</span></div>
      <div style="border-left-color:rgba(240,236,228,.14)"><b>80+</b><span class="muted">Team size</span></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="sop-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="sop-title" class="d-xl">Our <em>approach.</em></h2>
      <p class="intro">We follow the below-stated SOP to ensure campaign success.</p>
    </div>
    <ol class="sop">{sop}</ol>
  </div>
</section>

<section class="section band band-paper" id="mentors" aria-labelledby="m-title">
  <div class="wrap">
    <div class="founder grid" style="margin-bottom:clamp(64px,8vw,120px)">
      <div class="f-photo">{photo("amit", 900, 1125, "Amit Shankar")}</div>
      <div class="f-text">
        <p class="eyebrow">Founder</p>
        <h2 class="d-l">Amit Shankar</h2>
        <blockquote>Turning your brand narrative into big-stage success is his craft and forte.</blockquote>
        <p class="muted body-l">A master storyteller, he is a best-selling author and visiting faculty at top management and design institutes.</p>
      </div>
    </div>
    <div class="sec-head"><h2 id="m-title" class="d-xl">Our <em>mentors.</em></h2></div>
    <div class="mentor-grid photos">{m}</div>
  </div>
</section>

{closing()}
'''
    return page("about", "About, House of Lions", "India’s finest brand storytellers. Our story, our approach, our numbers and our mentors.", body, "about")


# ---------- SOLUTIONS ----------
def solutions():
    units = [("The Cub House", "Social media", "From strategy to storytelling, we craft insight-driven campaigns, engage audiences and drive measurable results. Our creative flair amplifies your brand’s voice across every platform. Trust us to make your social presence impactful.", "cubhouse"),
             ("Mavcomm", "Public relations", "Elevating brands and captivating audiences, we specialise in media relations, influencer partnerships, crisis management and brand PR strategy. Whether launching a new product, managing a reputation or building long-term brand awareness, we have a track record of success and a passion for innovation.", "mavcomm"),
             ("TABB Solutions", "Digital", "A leading provider of comprehensive digital solutions, empowering businesses of all sizes to thrive in the digital age. From digital marketing to website development, SEO to performance, we provide it all.", "tabb")]
    u = "".join(f'<article class="unit" style="background:var(--paper)"><div class="unit-logo"><img src="https://static.wixstatic.com/media/{IMG[k]}/v1/fit/w_600,h_340,q_90,enc_auto/{k}.png" alt="{n} logo" loading="lazy"></div><p class="role">{r}</p><h3>{n}</h3><p>{b}</p></article>' for n, r, b, k in units)
    cs = ""
    for s in STORIES:
        cs += f'''<article class="cs" id="{s["key"]}">
  <div class="cs-head"><p class="cat"><b>Client: {s["client"]}</b><span>{s["sector"]}</span></p><h2>{s["client"]}</h2><p>{s["about"]}</p></div>
  {ART[s["key"]]()}
  <div class="story-cols"><div><h4>The challenge</h4><p>{s["challenge"]}</p></div><div><h4>Solution</h4><p>{s["solution"]}</p></div></div>
</article>'''
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Solutions</p>
    <h1 class="rise d1">We got you <em>covered.</em></h1>
    <div class="ph-copy rise d2">
      <p>Integrated, robust and time-tested.</p>
      <p>While House of Lions is a brand and communication consultancy undertaking consultancy projects, we have specialised and integrated agencies delivering specialised services too.</p>
    </div>
  </div>
</section>

<section class="section" id="services" style="padding-top:0" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="svc-title" class="d-l">Breaking through the <em>noise.</em></h2></div>
    <ul class="cap-list">{services_list(False)}</ul>
  </div>
</section>

<section class="section band band-sage" aria-labelledby="units-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="units-title" class="d-xl">Our specialist <em>agencies.</em></h2></div>
    <div class="unit-grid">{u}</div>
  </div>
</section>

<section class="section" aria-labelledby="cs-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="cs-title" class="d-xl">Client <em>stories.</em></h2><p class="intro">We aim to overwhelm them with our IQ and EQ, going the extra mile every time and delivering every single time.</p></div>
    {cs}
  </div>
</section>

{closing()}
'''
    return page("solutions", "Solutions, House of Lions", "Personal branding, branding, social media, performance marketing and PR, with The Cub House, Mavcomm and TABB Solutions.", body, "solutions")


# ---------- INSIGHTS ----------
def insights():
    ins = "".join(f'<a href="{u}" target="_blank" rel="noopener"><span class="meta"><span>{d}</span><span>2 min read</span></span><h3>{h}</h3><p>{x}</p><span class="link-arrow" style="justify-self:start">Read on houseoflions.in <span class="arr" aria-hidden="true">&#8599;</span></span></a>' for h, x, d, u in POSTS)
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Insights</p>
    <h1 class="rise d1">Short. Precise. <em>Effective.</em></h1>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="ins">{ins}</div>
  </div>
</section>
{closing()}
'''
    return page("insights", "Insights, House of Lions", "Short. Precise. Effective. Insights from House of Lions.", body, "insights")


# ---------- CONTACT ----------
def contact():
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Contact</p>
    <h1 class="rise d1">Contact <em>us.</em></h1>
    <div class="ph-copy rise d2"><p>Call for a free consultation on {CONSULT}, or leave us a note below.</p></div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap grid contact-grid">
    <div class="contact-form">
      <form id="enquiry" novalidate>
        <div style="display:grid;gap:32px">
          <div class="two">
            <div class="field"><label for="f-name">First name *</label><input id="f-name" name="first_name" autocomplete="given-name"></div>
            <div class="field"><label for="f-last">Last name *</label><input id="f-last" name="last_name" autocomplete="family-name"></div>
          </div>
          <div class="two">
            <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
            <div class="field"><label for="f-industry">Industry</label><input id="f-industry" name="industry"></div>
          </div>
          <div class="field"><label for="f-company">Company / Organization</label><input id="f-company" name="company" autocomplete="organization"></div>
          <div class="field"><label for="f-msg">Message *</label><textarea id="f-msg" name="message" rows="4"></textarea></div>
          <p class="form-error" role="alert" hidden></p>
          <div class="actions"><button class="btn btn-primary" type="submit">Submit <span class="arr" aria-hidden="true">&#8599;</span></button></div>
        </div>
      </form>
      <div class="form-done" hidden aria-live="polite">
        <h2>Thank you, <span data-first></span>.</h2>
        <p>We’ll be in touch soon. For anything urgent, call {PHONE}.</p>
      </div>
    </div>
    <aside class="contact-side">
      <div class="side-block"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="side-block"><h3>Phone</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
      <div class="side-block"><h3>Free consultation</h3><p><a href="tel:{CONSULT_TEL}">{CONSULT}</a></p></div>
      <div class="side-block"><h3>Address</h3><address>1st Floor, VI John Tower<br>393, Udyog Vihar Phase 3 Road<br>Phase II, Udyog Vihar, Sector 20<br>Gurugram, Haryana 122016</address></div>
      <div class="side-block"><h3>Downloads</h3><p><a href="{PORTFOLIO}" target="_blank" rel="noopener">Portfolio (PDF)</a> &nbsp; <a href="{PROFILE}" target="_blank" rel="noopener">Profile (PDF)</a></p></div>
    </aside>
  </div>
</section>
'''
    return page("contact", "Contact House of Lions", "Contact House of Lions: amit@houseoflions.in, +91 88829 77667. VI John Tower, Udyog Vihar, Gurugram.", body, "contact")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#17140F"/>'
           '<text x="32" y="42" font-family="Georgia,serif" font-size="24" text-anchor="middle" fill="#F0ECE4">HOL</text></svg>')

PAGES = {"index.html": home, "about.html": about, "solutions.html": solutions,
         "insights.html": insights, "contact.html": contact}


def main():
    with open(os.path.join(ROOT, "assets", "favicon.svg"), "w") as f:
        f.write(FAVICON)
    for old in ("capabilities.html", "work.html", "perspectives.html"):
        p = os.path.join(ROOT, old)
        if os.path.exists(p):
            os.remove(p)
    built = {}
    for name, fn in PAGES.items():
        html = fn()
        built[name] = html
        with open(os.path.join(ROOT, name), "w") as f:
            f.write(html)
    if "--preview" in sys.argv:
        pv = os.path.join(ROOT, "_preview")
        shutil.rmtree(pv, ignore_errors=True)
        os.makedirs(os.path.join(pv, "assets"))
        for a in os.listdir(os.path.join(ROOT, "assets")):
            shutil.copy(os.path.join(ROOT, "assets", a), os.path.join(pv, "assets", a))
        for name, html in built.items():
            if name == "index.html":
                head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
                head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*', "", head)
                bm = re.search(r"<body([^>]*)>(.*)</body>", html, re.S)
                cls = re.search(r'class="([^"]+)"', bm.group(1)).group(1)
                html = head + f"\n<script>document.body.classList.add('{cls}')</script>\n" + bm.group(2)
            with open(os.path.join(pv, name), "w") as f:
                f.write(html)
    print("built", ", ".join(built))


if __name__ == "__main__":
    main()
