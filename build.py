#!/usr/bin/env python3
"""Builds the House of Lions static site.

  python3 build.py            -> writes the six pages into ./ (GitHub Pages ready)
  python3 build.py --preview  -> also writes ./_preview/ for the Claude artifact preview
"""
import math, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800&family=Geist:wght@300..700&display=swap">')

NAV = [("about.html", "About", "about"), ("capabilities.html", "Capabilities", "capabilities"),
       ("work.html", "Work", "work"), ("perspectives.html", "Perspectives", "perspectives"),
       ("contact.html", "Contact", "contact")]

EMAIL = "amit@houseoflions.in"
PHONE = "+91 88829 77667"
PHONE_TEL = "+918882977667"
LINKEDIN = "https://www.linkedin.com/company/houseoflions/"
INSTAGRAM = "https://www.instagram.com/houseoflions_consultancy/"


def mark(size=34, face="var(--marigold)", rays="currentColor"):
    """The House of Lions mark: a mane of rays around a marigold face."""
    lines = []
    n = 28
    for i in range(n):
        a = i / n * 2 * math.pi - math.pi / 2
        r1, r2 = 9.5, (15.5 if i % 2 == 0 else 13.2)
        lines.append(f'<line x1="{20 + math.cos(a) * r1:.2f}" y1="{20 + math.sin(a) * r1:.2f}" '
                     f'x2="{20 + math.cos(a) * r2:.2f}" y2="{20 + math.sin(a) * r2:.2f}"/>')
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true">'
            f'<g stroke="{rays}" stroke-width="1.4" stroke-linecap="round">{"".join(lines)}</g>'
            f'<circle cx="20" cy="20" r="7.4" fill="{face}"/>'
            f'<ellipse cx="17.3" cy="19.6" rx=".9" ry=".5" fill="#17140F"/><ellipse cx="22.7" cy="19.6" rx=".9" ry=".5" fill="#17140F"/></svg>')


def header(active):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    mlinks = "".join(
        f'<li><a href="{h}">{t}<span>0{i + 1}</span></a></li>' for i, (h, t, k) in enumerate(NAV))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="./" aria-label="House of Lions, home">{mark()}<span class="brand-name">House of Lions<small>Brand &amp; Communications</small></span></a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <a class="nav-cta" href="contact.html"><span class="dot" aria-hidden="true"></span>Start a conversation</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu"><span class="label">Menu</span><span class="bars" aria-hidden="true"></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <ul>{mlinks}</ul>
  <div class="mm-foot"><span>{EMAIL}</span><span>{PHONE}</span><span>Gurugram · Delhi · Mumbai · Paris</span></div>
</div>'''


def closing(title="Let’s make your next move matter.", eyebrow="Have a good challenge?"):
    return f'''<section class="band band-ink closing" aria-labelledby="closing-title">
  <div class="wrap grid">
    <div class="closing-left">
      <p class="eyebrow">{eyebrow}</p>
      <h2 id="closing-title">{title}</h2>
    </div>
    <div class="closing-right">
      <p>A new brand. A difficult brief. A launch that needs to land. Tell us what you are trying to achieve and we will tell you how we would think about it.</p>
      <div><a class="btn" href="contact.html">Start a conversation <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
  </div>
</section>'''


def footer():
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t, k in NAV)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-col"><h4>Studio</h4><address>1st Floor, VI John Tower<br>393, Udyog Vihar Phase 3<br>Sector 20, Gurugram<br>Haryana 122016</address></div>
      <div class="foot-col"><h4>Talk to us</h4><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
      <div class="foot-col"><h4>Explore</h4>{nav}</div>
      <div class="foot-col"><h4>Follow</h4><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram</a></div>
    </div>
    <div class="foot-mark" aria-hidden="true">House of Lions</div>
    <div class="foot-bottom"><span>&copy; <span data-year>2026</span> House of Lions. Gurugram, Delhi, Mumbai, Paris.</span><span>Scripting success, since day one.</span></div>
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
<meta name="theme-color" content="#F0ECE4">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/style.css?v=3">
</head>
<body class="p-{slug}">
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/main.js?v=3"></script>
</body>
</html>
'''


# ---------- Case-study art ----------
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
    "vibes": lambda: '<div class="art art-vibes" role="img" aria-label="Soft overlapping glowing forms in blush and lilac"><span class="tag">Vibes Healthcare</span><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span><span class="big condensed"><small>Clinics across India and Bangladesh</small>31</span></div>',
    "monteria": lambda: f'<div class="art art-monteria" role="img" aria-label="Topographic contour lines on deep forest green"><span class="tag">Monteria Village</span>{contours()}<span class="big condensed"><small>Acres, near Mumbai</small>36</span></div>',
    "baxy": lambda: '<div class="art art-baxy" role="img" aria-label="Marigold road stripes and a wheel on cobalt blue"><span class="stripes"></span><span class="tag">Baxy Mobility</span><span class="wheel"></span><span class="big condensed"><small>Wheels, one consistent brand</small>3</span></div>',
}

CASES = [
    dict(key="monteria", client="Monteria Village", cat="Property &amp; Place",
         meta=["Hospitality", "Positioning", "Go-to-market"],
         title="Turning a school-trip stop into a destination.",
         short="India’s first sustainable village retreat had footfall from schools but little pull with weekend travellers and corporates. We repositioned it as a must-visit destination.",
         challenge="Spread over 36 acres near Mumbai, the retreat drew steady school groups but few weekend travellers or corporate off-sites. Its positioning gave the right audiences no reason to choose it.",
         insight="Urban families and teams are not looking for another resort. They want a real reason to slow down and reconnect with where they come from.",
         idea="A new positioning that placed Monteria firmly as a destination worth the drive, built around curated, traditional experiences.",
         execution="Positioning statement, revamped go-to-market plan, brand manual, marketing templates, a new website and a refreshed digital presence.",
         outcome=None),
    dict(key="vibes", client="Vibes Healthcare", cat="Beauty &amp; Wellness",
         meta=["Brand refresh", "Content", "Influencer", "Digital"],
         title="Giving a crowded category a reason to choose.",
         short="With 31 clinics across India and Bangladesh, Vibes was competing on price in a cluttered market. We rebuilt how the brand shows up and speaks.",
         challenge="Beauty and wellness is a crowded market with few real differentiators, so price had become the deciding factor. Vibes was struggling to engage and to stand apart.",
         insight="When every clinic promises the same results, people choose the one they trust. Trust is built by voices, not by discounts.",
         idea="A refreshed brand with clear rules of engagement, led by real people: clients, experts and creators telling the Vibes story.",
         execution="Brand refresh, go-to-market plan, rules of engagement, reels and short-form content, influencer campaigns, testimonials and a sustained digital marketing programme.",
         outcome=None),
    dict(key="baxy", client="Baxy Mobility", cat="Mobility &amp; Innovation",
         meta=["Identity", "Brand guidelines", "Retail"],
         title="One brand, from showroom to service bay.",
         short="An industry leader in three-wheelers had hit a glass ceiling, held back by inconsistent branding. We gave it a refreshed identity and the system to hold it together.",
         challenge="Baxy led its category on fuel efficiency and reliability, but inconsistent branding and no long-term brand roadmap were holding back its organic growth.",
         insight="For a dealer network, consistency is credibility. A buyer should feel the same brand in the showroom, the service centre and the ad.",
         idea="A refreshed identity designed as a system, so every touchpoint reinforces the same promise.",
         execution="New colour scheme and typography, comprehensive brand guidelines, and a consistent rollout from showroom to service centre and from print to digital.",
         outcome="The refreshed identity was well received across the network, and the client reported a positive effect on financial performance."),
]


def case_teaser(c, flip=False):
    meta = "".join(f"<span>{m}</span>" for m in c["meta"])
    return f'''<a class="case{" flip" if flip else ""}" href="work.html#{c["key"]}">
  <div class="case-art">{ART[c["key"]]()}</div>
  <div class="case-text">
    <p class="case-client">{c["client"]}</p>
    <h3>{c["title"]}</h3>
    <p>{c["short"]}</p>
    <p class="case-meta">{meta}</p>
    <span class="link-arrow">Read the case <span class="arr" aria-hidden="true">&#8599;</span></span>
  </div>
</a>'''


CAPS = [
    dict(id="strategy", n="01", verb="Define", name="Brand Strategy &amp; Identity", tint="#E3DBCC",
         short="Find your difference. Define your position. Build a brand system that stays coherent as you grow.",
         tags="Positioning, naming, identity, brand architecture",
         h="Find your reason to stand apart.",
         problem="Most brands are not short of activity. They are short of a clear, ownable reason to be chosen. Without it, every campaign starts from zero.",
         pov="Positioning is a decision, not a sentence. We help leadership make that decision, then build an identity and architecture that make it visible everywhere.",
         services=["Audience insight", "Positioning", "Naming", "Visual identity", "Brand architecture", "Brand guidelines", "GTM strategy"],
         proof=("baxy", "Baxy Mobility", "A refreshed identity, held together from showroom to service centre.")),
    dict(id="creative", n="02", verb="Express", name="Creative &amp; Storytelling", tint="#EBDCD3",
         short="Turn business objectives into sharp ideas, distinctive narratives and campaigns that give people a reason to care.",
         tags="Campaigns, content, film, art direction",
         h="Make the idea impossible to ignore.",
         problem="Attention is expensive and forgettable work is the most expensive of all. Content without an idea behind it adds volume, not value.",
         pov="We start with the story and earn the format. One strong platform idea, expressed with craft across film, content and campaign, outperforms a hundred disconnected posts.",
         services=["Campaign platforms", "Copywriting", "Art direction", "Film and reels", "Content systems", "Influencer-led storytelling"],
         proof=("vibes", "Vibes Healthcare", "A people-led content and influencer programme for 31 clinics.")),
    dict(id="reputation", n="03", verb="Influence", name="Communications &amp; Reputation", tint="#DDE2E6",
         short="Shape how people see you, what they hear about you and the conversations your brand earns.",
         tags="PR, media relations, influencers, reputation",
         h="Build influence that lasts.",
         problem="Reputation is built slowly and lost quickly. Brands that only speak when they need something rarely get heard when it matters.",
         pov="Earned attention comes from having something worth saying. We shape the narrative, find the right voices and prepare you for the moments you cannot schedule.",
         services=["Media relations", "Thought leadership", "Founder and leadership profiles", "Influencer partnerships", "Crisis communication"],
         proof=None),
    dict(id="digital", n="04", verb="Grow", name="Digital &amp; Performance", tint="#F6D9A6",
         short="Connect audience insight, digital experiences and measurable campaigns to turn attention into action.",
         tags="Digital strategy, social, paid media, SEO, analytics",
         h="Turn attention into action.",
         problem="Performance marketing can buy clicks, but it cannot fix a brand problem. Without a clear story, every rupee works harder than it should.",
         pov="We plan brand and performance together, so the same idea earns attention and converts it. Then we measure, learn and keep improving the work.",
         services=["Social strategy", "Paid media", "SEO", "Websites", "Analytics and reporting", "Optimisation"],
         proof=("vibes", "Vibes Healthcare", "Brand refresh joined up with a sustained digital programme.")),
    dict(id="launch", n="05", verb="Activate", name="Go-to-Market &amp; Launches", tint="#E3DBCC",
         short="Build market entry and launch programmes that align the proposition, communication and customer journey.",
         tags="GTM, launch strategy, integrated campaigns, experiences",
         h="Give ambition a market-ready expression.",
         problem="Launches fail in the gaps between teams: the proposition says one thing, the campaign another and the customer experience a third.",
         pov="We bring proposition, communication and the customer journey into one plan, so the launch lands as one idea with one voice.",
         services=["Go-to-market planning", "Launch strategy", "Integrated campaigns", "Events and experiences", "Sales enablement"],
         proof=("monteria", "Monteria Village", "New positioning and GTM that turned a stop into a destination.")),
]

QUOTES = [
    ("A highly energetic and passionate team, always up for a new challenge, walking the extra mile to ensure seamless client servicing and delight.", "Yukti Nagpal", "Director, Gulshan Group"),
    ("What sets them apart is their heart. They helped me find my voice, and I will always be grateful for that.", "Anita Ajwani", "Founder, Memsaheb"),
    ("Their collaborative approach, open communication and commitment to our success made working with them productive and enjoyable.", "Sameer Malhotra", "CEO, Shriram Automall"),
]

POSTS = [
    dict(cat="strategy", label="Brand strategy", title="Positioning is a decision, not a sentence", dek="Why most positioning statements fail before anyone reads them, and what leadership has to give up to get one right.", mins=6, art="#E3DBCC", word="Choose."),
    dict(cat="story", label="The art of storytelling", title="The thirty-second test for your brand story", dek="If your own team tells your story five different ways, your customers are hearing none of them.", mins=5, art="#17140F", fg="#F4A51C", word="Say it once."),
    dict(cat="digital", label="Digital &amp; the future", title="Performance marketing cannot fix a brand problem", dek="Spend is rising and returns are flattening. The fix usually sits upstream of the media plan.", mins=7, art="#2C46D6", fg="#F0ECE4", word="ROI &ne; reach"),
    dict(cat="culture", label="Culture &amp; consumers", title="The new Indian consumer does not want to be sold to", dek="From tier-two cities to Paris, audiences reward brands that act like hosts, not hawkers.", mins=6, art="#EBCFC6", word="Host, don’t hawk."),
    dict(cat="reputation", label="Leadership &amp; reputation", title="Reputation is built in the quiet months", dek="The brands that survive a crisis are the ones that were talking long before they needed to.", mins=5, art="#22362A", fg="#EFE8D8", word="Before the storm."),
    dict(cat="creativity", label="Advertising &amp; creativity", title="Consistency is the most underrated creative idea", dek="Lessons from a three-wheeler brand on why the showroom matters as much as the ad.", mins=4, art="#F4A51C", word="Again. Again."),
]


def post_card(p, cls="post"):
    fg = p.get("fg", "#17140F")
    return f'''<a class="{cls}" href="perspectives.html" data-post="{p["cat"]}">
  <div class="post-art" style="background:{p["art"]};color:{fg}"><span class="condensed">{p["word"]}</span></div>
  <p class="post-meta"><span>{p["label"]}</span><span>{p["mins"]} min read</span></p>
  <h3>{p["title"]}</h3>
  <p>{p["dek"]}</p>
</a>'''


# ---------- HOME ----------
def home():
    ticker_items = ["EV to café", "Beauty to real estate", "Gurugram to Paris", "Strategy", "Story", "Design", "Growth"]
    t = "".join(f'<span class="ticker-item">{x}<span class="x" aria-hidden="true">&#10033;</span></span>' for x in ticker_items)
    caps = "".join(f'''<li class="cap-row"><a href="capabilities.html#{c["id"]}" style="--tint:{c["tint"]}">
  <span class="cap-num">{c["n"]}<b>{c["verb"]}</b></span>
  <span class="cap-title">{c["name"]}</span>
  <span class="cap-desc"><p>{c["short"]}</p><span class="cap-tags">{c["tags"]}</span></span>
  <span class="cap-arrow" aria-hidden="true">&#8599;</span>
</a></li>''' for c in CAPS)
    cases = "".join(case_teaser(c, i % 2 == 1) for i, c in enumerate(CASES))
    steps = [("Understand", "The business, the audience and the real challenge behind the brief."),
             ("Find the insight", "The tension, truth or opportunity others have overlooked."),
             ("Define the idea", "A clear strategic direction and a narrative people can believe."),
             ("Make it real", "Creative work across the channels that matter, crafted properly."),
             ("Measure and evolve", "Learn from performance and keep making the work better.")]
    steps_html = "".join(f'<li><span class="n">{i + 1:02d}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps))
    why = [("We think beyond the brief.", "We look at the business problem, not just the communication task."),
           ("We connect the dots.", "Brand, creative, PR and digital work harder when they work together, under one roof."),
           ("We use both sides of the brain.", "Insight and imagination belong at the same table. So do IQ and EQ."),
           ("We care about what changes.", "Good work builds distinction, relevance and business value. That is how we judge it.")]
    why_html = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in why)
    quotes = "".join(f'<figure class="quote"><blockquote>“{q}”</blockquote><figcaption><b>{n}</b>, {r}</figcaption></figure>' for q, n, r in QUOTES[:3])
    posts = "".join(post_card(p) for p in POSTS[:3])

    body = f'''
<section class="hero">
  <div class="wrap grid hero-grid">
    <div class="hero-copy">
      <p class="eyebrow rise">Brand &amp; communications consultancy</p>
      <h1><span class="line rise d1">We build</span><span class="line rise d2">brands that</span><span class="line rise d3">mean business.</span></h1>
      <div class="hero-support rise d4">
        <p>Strategy gives a brand direction. Story gives it meaning. Creativity makes it impossible to ignore.</p>
        <p>House of Lions brings all three together for ambitious companies, from first idea to the campaign that changes the conversation.</p>
      </div>
      <div class="actions rise d5">
        <a class="btn btn-primary" href="contact.html">Let’s talk about your brand <span class="arr" aria-hidden="true">&#8599;</span></a>
        <a class="link-arrow" href="#work">See the work <span class="arr down" aria-hidden="true">&#8595;</span></a>
      </div>
    </div>
    <div class="hero-aside rise d3">
      <div class="mane-panel">
        <canvas aria-hidden="true"></canvas>
        <p class="mane-caption"><span>Move to wake the lion. Tap to roar.</span><span>Est. Gurugram</span></p>
      </div>
    </div>
  </div>
</section>

<div class="ticker" aria-label="EV to café, beauty to real estate, Gurugram to Paris. Strategy, story, design, growth.">
  <div class="ticker-track" aria-hidden="true">{t}{t}</div>
</div>

<section class="band band-ink section" aria-labelledby="pos-title">
  <div class="wrap grid position-grid">
    <h2 id="pos-title" class="d-xl">Not another agency. A thinking partner.</h2>
    <div class="position-copy">
      <p>Markets are crowded. Attention is expensive. Being seen is no longer enough.</p>
      <p class="muted">Brands need a clear point of view, a story worth repeating and a connected strategy that holds across every touchpoint.</p>
      <p class="muted">That is where we come in. We challenge the obvious, find the opportunity and turn strategic thinking into work people notice, remember and act on.</p>
    </div>
    <div class="position-art">
      <div class="board" style="color:var(--ink)">
        <div class="board-top"><span>Working wall</span><span>Week one</span></div>
        <div class="board-word"><span class="strike">Louder.</span><br>Clearer.</div>
        <div class="board-notes">
          <div><b>Insight</b>What do people actually believe about you today?</div>
          <div><b>Idea</b>The one thing only you can own and say.</div>
          <div><b>Impact</b>Distinction, relevance, growth. In that order.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="cap-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="cap-title" class="d-xl">Different disciplines. One connected ambition.</h2>
      <p class="intro">We connect the thinking behind a brand with the work that takes it into the world. One team, one plan, one voice.</p>
    </div>
    <ul class="cap-list">{caps}</ul>
    <p class="units">Delivered with our specialist teams: <b>The Cub House</b> for social, <b>Mavcomm</b> for PR and <b>TABB Solutions</b> for digital.</p>
  </div>
</section>

<section class="section band-paper band" id="work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="work-title" class="d-xl">The work speaks for itself.</h2>
      <p class="intro">Different businesses, different challenges. One constant: finding the idea that makes the difference.</p>
    </div>
    <div class="work-list">{cases}</div>
    <div style="margin-top:clamp(64px,8vw,112px)"><a class="btn btn-primary" href="work.html">Explore all work <span class="arr" aria-hidden="true">&#8599;</span></a></div>
  </div>
</section>

<section class="band band-sage section" aria-labelledby="app-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="app-title" class="d-xl">Good work begins with better questions.</h2>
      <p class="intro">A simple process, followed with discipline. It is how we keep ambitious ideas tied to real business outcomes.</p>
    </div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="why-title" class="d-xl">Strategy with instinct. Creativity with intent.</h2>
      <p class="intro">Boardroom-ready thinking with the creative confidence of an independent studio. A perfect blend of experience and adrenaline.</p>
    </div>
    <div class="why">{why_html}</div>
    <p class="principle"><b>Strategically aggressive.</b> We push for the bolder idea, and we can tell you exactly why it will work.</p>
  </div>
</section>

<section class="section band band-paper" aria-labelledby="lead-title">
  <div class="wrap grid lead-grid">
    <div class="lead-intro">
      <h2 id="lead-title" class="d-l">Experience brings perspective. Curiosity keeps it moving.</h2>
      <p class="muted body-l">House of Lions is guided by people who understand both the craft of communication and the realities of business, backed by mentors from advertising, media, PR and digital.</p>
      <div><a class="link-arrow" href="about.html#people">Meet the people <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
    <div class="lead-people">
      <div class="person lead"><span class="person-mark" style="background:var(--marigold)">AS</span><div><h3>Amit Shankar</h3><p class="role">Founder</p><p class="bio">A storyteller who turns brand narratives into big-stage success. Best-selling author and visiting faculty at leading management and design institutes.</p></div></div>
      <div class="person"><span class="person-mark" style="background:var(--sage)">NM</span><div><h3>Nikhil Malhotra</h3><p class="role">Co-founder, digital</p></div></div>
      <div class="person"><span class="person-mark" style="background:var(--clay)">SU</span><div><h3>Siddhartha Upadhyay</h3><p class="role">Mentor, founder of Mavcomm Consulting</p></div></div>
      <div class="person"><span class="person-mark" style="background:var(--powder)">SN</span><div><h3>Siddharth Narula</h3><p class="role">Business mentor, former CRO, Zee Digital</p></div></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="voice-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="voice-title" class="d-l">Trust is earned in the work.</h2></div>
    <div class="quotes">{quotes}</div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="persp-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="persp-title" class="d-xl">Thinking beyond the brief.</h2>
      <div class="intro" style="display:grid;gap:18px;justify-items:start"><p>Essays on brand building, storytelling and the business of staying relevant.</p><a class="link-arrow" href="perspectives.html">All perspectives <span class="arr" aria-hidden="true">&#8599;</span></a></div>
    </div>
    <div class="posts">{posts}</div>
  </div>
</section>

{closing()}
'''
    return page("home", "House of Lions", "House of Lions is a brand and communications consultancy in Gurugram, Delhi, Mumbai and Paris. Strategy, storytelling, creative, PR and digital, joined up.", body, "home")


# ---------- ABOUT ----------
def about():
    mentors = [
        ("Akhil Bakhshi", "Creative mentor", "An internationally acclaimed photographer whose career spans more than 30 years and 15 countries, working with leading agencies, brands and models."),
        ("Siddharth Narula", "Business mentor", "Former Chief Revenue Officer at Zee Digital-OTT and Culture Machine, with earlier roles at Walt Disney, Bloomberg UTV, CNBC, NDTV, ESPN and Sony TV."),
        ("Siddhartha Upadhyay", "Creative mentor", "Founder of Mavcomm Consulting, a leading PR consultancy handling image building and crisis management for national and multinational brands."),
        ("Amit Mukherjee", "Creative mentor", "A brand and communication practitioner trained at Delhi College of Art, with years at Saatchi &amp; Saatchi, Ogilvy and Dentsu."),
        ("Dr Divya Tanwar", "Empowerment mentor", "Academic and cyber-security specialist, adjunct professor in Mumbai and author of several books on information and database systems."),
        ("Nikhil Malhotra", "Co-founder and digital mentor", "Entrepreneur and digital marketer with a sharp eye for ROI. He also runs the fragrance brand Air Roma."),
    ]
    m = "".join(f'<article class="mentor"><p class="role">{r}</p><h3>{n}</h3><p>{b}</p></article>' for n, r, b in mentors)
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">About House of Lions</p>
    <h1 class="rise d1">Good brands are built on good thinking.</h1>
    <div class="ph-copy rise d2">
      <p>The strongest communication begins long before the first piece of creative is made. It begins with understanding the business, finding the truth that sets it apart and shaping a story people can believe in.</p>
      <p>We bring strategy, storytelling, creativity and integrated execution together to help ambitious brands move forward.</p>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="philosophy">
      <div><b>Insight before output.</b><span>We earn the right to make things by understanding first.</span></div>
      <div><b>Ideas before assets.</b><span>A strong idea makes every format easier and every rupee go further.</span></div>
      <div><b>Purpose before noise.</b><span>Being heard matters more than being loud.</span></div>
    </div>
  </div>
</section>

<section class="band band-ink section" aria-labelledby="story-title">
  <div class="wrap grid split">
    <div class="left"><p class="eyebrow">Our story</p><h2 id="story-title" class="d-l" style="margin-top:20px">Experience and adrenaline. Sanity and bold moves.</h2></div>
    <div class="right">
      <p class="lede" style="max-width:none">House of Lions started with a simple frustration: too many brands were being sold activity when what they needed was clarity.</p>
      <p class="muted">So we built a consultancy that thinks like a strategy firm and makes like a creative studio. Our work is always rooted in insight, and our stories are designed to last longer than the campaign.</p>
      <p class="muted">Today the House brings together brand strategy, creative, PR and digital, with specialist teams in The Cub House, Mavcomm and TABB Solutions, working for clients from EV to café, beauty to real estate.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="facts">
      <div><b>4</b><span>Offices in Gurugram, Delhi, Mumbai and Paris</span></div>
      <div><b>80+</b><span>Strategists, writers, designers and media people</span></div>
      <div><b>3</b><span>Specialist teams for social, PR and digital</span></div>
      <div><b>10</b><span>Steps from brand objective to reporting, every time</span></div>
    </div>
  </div>
</section>

<section class="section band band-paper" id="people" aria-labelledby="people-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="people-title" class="d-xl">The people behind the pride.</h2>
      <p class="intro">Leadership with decades across advertising, media, PR and digital, and a team young enough to stay restless.</p>
    </div>
    <div class="person lead" style="border-top:1px solid var(--line-strong);margin-bottom:48px">
      <span class="person-mark" style="background:var(--marigold)">AS</span>
      <div><h3 style="font-size:clamp(28px,3vw,40px)">Amit Shankar</h3><p class="role">Founder</p><p class="bio" style="font-size:17px">Amit leads brand strategy, storytelling and communications at House of Lions. A best-selling author and visiting faculty at leading management and design institutes, he has spent his career turning brand narratives into big-stage success.</p></div>
    </div>
    <div class="mentor-grid">{m}</div>
  </div>
</section>

<section class="section" aria-labelledby="pr-title">
  <div class="wrap grid split">
    <div class="left"><h2 id="pr-title" class="d-l">What we hold ourselves to.</h2></div>
    <div class="right">
      <div class="principles"><span>Curiosity</span><span>Clarity</span><span>Courage</span><span>Collaboration</span><span>Accountability</span></div>
      <p class="muted body-l">These are not wall posters. They are how we decide what to recommend, what to make and what to push back on.</p>
    </div>
  </div>
</section>

{closing("Let’s build something worth talking about.", "Work with us")}
'''
    return page("about", "About House of Lions", "Our point of view, our people and how we think. House of Lions is a brand and communications consultancy.", body, "about")


# ---------- CAPABILITIES ----------
def capabilities():
    blocks = ""
    for c in CAPS:
        svc = "".join(f"<span>{s}</span>" for s in c["services"])
        if c["proof"]:
            k, n, line = c["proof"]
            proof = f'<a class="cd-proof" href="work.html#{k}"><span>Related work</span><b>{n}</b><span>{line}</span></a>'
        else:
            proof = '<div class="cd-proof"><span>Delivered with</span><b>Mavcomm</b><span>Our specialist PR team for media relations, influencer partnerships and crisis management.</span></div>'
        blocks += f'''<section class="cap-detail" id="{c["id"]}" style="--tint:{c["tint"]}">
  <div class="cd-head"><p class="k">{c["n"]} / {c["verb"].upper()}</p><h2>{c["h"]}</h2><p class="muted">{c["name"]}</p></div>
  <div class="cd-body">
    <div class="cd-block"><h4>The problem</h4><p>{c["problem"]}</p></div>
    <div class="cd-block"><h4>How we see it</h4><p>{c["pov"]}</p></div>
    <div class="cd-block"><h4>What’s involved</h4><div class="cd-services">{svc}</div></div>
    {proof}
    <div><a class="link-arrow" href="contact.html">Talk to us about {c["name"].split(" &amp;")[0].lower()} <span class="arr" aria-hidden="true">&#8599;</span></a></div>
  </div>
</section>'''
    units = [("The Cub House", "Social", "Strategy to storytelling for social. Insight-driven campaigns that engage audiences and drive measurable results on every platform."),
             ("Mavcomm", "Public relations", "Media relations, influencer partnerships, crisis management and brand PR, for launches, reputation and long-term awareness."),
             ("TABB Solutions", "Digital", "Digital marketing, website development, SEO and performance, with the depth to deliver for businesses of every size.")]
    u = "".join(f'<article class="unit"><p class="role">{r}</p><h3>{n}</h3><p>{b}</p></article>' for n, r, b in units)
    nav = "".join(f'<a class="link-arrow" href="#{c["id"]}" style="border-bottom-width:1px">{c["name"]}</a>' for c in CAPS)
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Capabilities</p>
    <h1 class="rise d1">Different disciplines. One connected ambition.</h1>
    <div class="ph-copy rise d2">
      <p>We sell thinking first and deliverables second. Every capability starts with the business problem, and every one of them works better alongside the others.</p>
      <div class="actions" style="gap:12px 24px;margin-top:12px">{nav}</div>
    </div>
  </div>
</section>
<div class="wrap">{blocks}</div>
<section class="section band band-paper" aria-labelledby="units-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="units-title" class="d-l">Specialist teams, one House.</h2><p class="intro">Our integrated agencies bring depth in social, PR and digital, led by one strategy and one point of contact.</p></div>
    <div class="unit-grid">{u}</div>
  </div>
</section>
{closing()}
'''
    return page("capabilities", "Capabilities, House of Lions", "Brand strategy, creative and storytelling, communications and reputation, digital and performance, and go-to-market.", body, "capabilities")


# ---------- WORK ----------
def work():
    out = ""
    for c in CASES:
        steps = [("The challenge", c["challenge"]), ("The insight", c["insight"]), ("The idea", c["idea"]),
                 ("The execution", c["execution"]),
                 ("The outcome", c["outcome"] or '<span class="pending">Results to be added with the client’s approval.</span>')]
        fw = "".join(f'<li><h4><span>{i + 1:02d}</span>{a}</h4><p>{b}</p></li>' for i, (a, b) in enumerate(steps))
        meta = " ".join(f"<span>{m}</span>" for m in c["meta"])
        out += f'''<article class="cs" id="{c["key"]}">
  <div class="cs-head">
    <p class="cat"><b>{c["cat"]}</b>{meta}</p>
    <h2>{c["title"]}</h2>
    <p>{c["client"]}. {c["short"]}</p>
  </div>
  {ART[c["key"]]()}
  <ol class="framework">{fw}</ol>
</article>'''
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Selected work</p>
    <h1 class="rise d1">Different businesses. One constant.</h1>
    <div class="ph-copy rise d2"><p>Every brief is different, but the job is the same: find the idea that makes the difference, then make it real everywhere it needs to be.</p></div>
  </div>
</section>
<div class="wrap">{out}</div>
{closing("Your brand could be the next case study.", "Start a project")}
'''
    return page("work", "Work, House of Lions", "Selected case studies from House of Lions: Monteria Village, Vibes Healthcare and Baxy Mobility.", body, "work")


# ---------- PERSPECTIVES ----------
def perspectives():
    cats = [("all", "All")] + [(p["cat"], p["label"]) for p in POSTS]
    seen, btns = set(), ""
    for k, l in cats:
        if k in seen: continue
        seen.add(k)
        btns += f'<button type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>'
    f = POSTS[0]
    feature = f'''<a class="feature" href="perspectives.html" data-post="{f["cat"]}">
  <div class="post-art" style="background:#17140F;color:#F4A51C"><span class="condensed">{f["word"]}</span></div>
  <div class="ft"><p class="post-meta"><span>{f["label"]}</span><span>{f["mins"]} min read</span><span>By Amit Shankar</span></p><h2>{f["title"]}</h2><p>{f["dek"]}</p><span class="link-arrow">Read the essay <span class="arr" aria-hidden="true">&#8599;</span></span></div>
</a>'''
    grid = "".join(post_card(p) for p in POSTS[1:])
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Perspectives</p>
    <h1 class="rise d1">Thinking beyond the brief.</h1>
    <div class="ph-copy rise d2"><p>Ideas worth sharing and questions worth asking, on the changing relationship between brands, people and culture.</p></div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter by topic">{btns}</div>
    {feature}
    <div class="posts all">{grid}</div>
  </div>
</section>
{closing("Have a question worth asking?", "Start a conversation")}
'''
    return page("perspectives", "Perspectives, House of Lions", "Essays on brand strategy, storytelling, creativity, culture, reputation and digital from House of Lions.", body, "perspectives")


# ---------- CONTACT ----------
def contact():
    helps = ["Brand strategy", "Creative &amp; content", "PR &amp; reputation", "Digital &amp; performance", "A launch", "Not sure yet"]
    chips = "".join(f'<label><input type="checkbox" name="help" value="{h}"><span>{h}</span></label>' for h in helps)
    body = f'''
<section class="page-hero">
  <div class="wrap grid">
    <p class="eyebrow rise">Contact</p>
    <h1 class="rise d1">Tell us what you’re trying to change.</h1>
    <div class="ph-copy rise d2"><p>Building a new brand, rethinking an existing one or preparing for your next big move? We’d like to hear about it. Expect a reply from a senior person within two working days.</p></div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap grid contact-grid">
    <div class="contact-form">
      <form id="enquiry" novalidate>
        <div style="display:grid;gap:32px">
          <div class="two">
            <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name"></div>
            <div class="field"><label for="f-email">Work email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
          </div>
          <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization"></div>
          <fieldset class="field"><legend>What do you need help with?</legend><div class="chips">{chips}</div></fieldset>
          <div class="field"><label for="f-msg">Tell us a little about the challenge</label><textarea id="f-msg" name="message" rows="4"></textarea></div>
          <p class="form-error" role="alert" hidden></p>
          <div class="actions"><button class="btn btn-primary" type="submit">Start the conversation <span class="arr" aria-hidden="true">&#8599;</span></button><span class="form-note">No long questionnaires. We’ll take it from here.</span></div>
        </div>
      </form>
      <div class="form-done" hidden aria-live="polite">
        <h2>Thanks, <span data-first></span>. We’re on it.</h2>
        <p>Someone senior from the House will reply within two working days. If it’s urgent, call us on {PHONE}.</p>
      </div>
    </div>
    <aside class="contact-side">
      <div class="side-block"><h3>Write to us</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="side-block"><h3>Call</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
      <div class="side-block"><h3>Visit the studio</h3><address>1st Floor, VI John Tower<br>393, Udyog Vihar Phase 3<br>Sector 20, Gurugram, Haryana 122016</address></div>
      <div class="side-block"><h3>Offices</h3><p>Gurugram, Delhi, Mumbai, Paris</p></div>
      <div class="side-block"><h3>Follow</h3><p><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &nbsp; <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></p></div>
    </aside>
  </div>
</section>
'''
    return page("contact", "Contact House of Lions", "Start a conversation with House of Lions in Gurugram, Delhi, Mumbai or Paris.", body, "contact")


FAVICON = mark(64, rays="#17140F").replace('width="64" height="64" ', 'xmlns="http://www.w3.org/2000/svg" width="64" height="64" ')

PAGES = {"index.html": home, "about.html": about, "capabilities.html": capabilities,
         "work.html": work, "perspectives.html": perspectives, "contact.html": contact}


def main():
    with open(os.path.join(ROOT, "assets", "favicon.svg"), "w") as f:
        f.write(FAVICON)
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
                body = bm.group(2)
                html = head + f"\n<script>document.body.classList.add('{cls}')</script>\n" + body
            with open(os.path.join(pv, name), "w") as f:
                f.write(html)
    print("built", ", ".join(built))


if __name__ == "__main__":
    main()
