"""Generates the inner pages of the NDR Infotech site. Run: python build.py"""
import html, pathlib
from icons import decorate

OUT = pathlib.Path(__file__).parent
PHONE, EMAIL = "+91 87223 55999", "hr@ndrinfotech.com"

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("technologies.html", "Technologies"), ("talent.html", "Talent"), ("contact.html", "Contact")]

LOGO = ('<svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="url(#g)"/>'
        '<path d="M16 48V16l32 32V16" fill="none" stroke="#06101f" stroke-width="6" stroke-linejoin="round"/>'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs></svg>')

ICONS = {1: '<circle cx="21" cy="21" r="11"/><path d="M29 29l11 11"/><path d="M17 21h8M21 17v8"/>', 2: '<path d="M8 40l4-12L34 6l8 8-22 22z"/><path d="M28 12l8 8"/><path d="M8 40l8-3"/>', 3: '<path d="M24 6c8 4 12 12 10 22l-6 6H20l-6-6C12 18 16 10 24 6z"/><circle cx="24" cy="19" r="3"/><path d="M14 32l-6 8 10-3M34 32l6 8-10-3"/>', 4: '<path d="M24 5l16 6v12c0 10-7 17-16 20C15 40 8 33 8 23V11z"/><path d="M17 24l5 5 9-10"/>'}
def num(n):
    n = int(n)
    return f'<span class="num"><i>0{n}</i><svg viewBox="0 0 48 48" aria-hidden="true">{ICONS[n]}</svg></span>'
import re
STEP = re.compile(r'<span>0([1-4])</span>')

SCENES = {"about.html": "network", "services.html": "orbit", "technologies.html": "code", "talent.html": "network",
          "contact.html": "pulse", "svc-cloud.html": "cloud", "svc-data-bi.html": "bars", "svc-development.html": "code",
          "svc-migration.html": "flow", "svc-devops.html": "loop", "svc-consulting.html": "radar"}

def page(fname, title, desc, h1, lead, body, eyebrow=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == fname or (fname.startswith("svc-") and h == "services.html") else ""}>{t}</a>'
        for h, t in NAV[1:-1])
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | NDR Infotech</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#070b16">
<link rel="canonical" href="https://www.ndrinfotech.com/{fname}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230b1226'/%3E%3Cpath d='M16 48V16l32 32V16' fill='none' stroke='%2322d3ee' stroke-width='6' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav solid" id="nav"><div class="wrap nav-in">
<a class="logo" href="index.html" aria-label="NDR Infotech home">{LOGO}<span>NDR <b>Infotech</b></span></a>
<nav id="menu" aria-label="Primary"><a href="index.html">Home</a>{links}<a href="contact.html" class="btn btn-sm">Talk to us</a></nav>
<button class="burger" id="burger" aria-label="Toggle menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
</div></header>
<main id="main">
<section class="page-hero" data-scene="{SCENES.get(fname, 'network')}"><div class="glow g1"></div><div class="glow g2"></div><div class="grid-bg"></div>
<div class="wrap"><p class="eyebrow">{eyebrow or title}</p><h1>{h1}</h1><p class="lead">{lead}</p></div></section>
{body}
<section class="sec cta-band"><div class="wrap"><h2>Ready to talk about your project?</h2>
<p class="muted">Share a short brief and we'll respond to set up a discovery conversation.</p>
<a class="btn" href="contact.html">Contact us</a></div></section>
</main>
<footer class="foot"><div class="wrap foot-in"><p>© <span id="yr"></span> NDR Infotech · Bangalore</p>
<p><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms &amp; Conditions</a></p></div></footer>
<script src="script.js"></script><script src="hero-bg.js"></script></body></html>'''
    doc = decorate(doc)
    if fname == "services.html":
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="head reveal"><p class="eyebrow">Capabilities', '<section class="sec" id="caps"><div class="wrap"><div class="head reveal"><p class="eyebrow">Capabilities', 1)
        doc = doc.replace('<section class="sec alt"><div class="wrap"><div class="head reveal"><p class="eyebrow">Industries', '<section class="sec alt" id="industries"><div class="wrap"><div class="head reveal"><p class="eyebrow">Industries', 1)
        doc = doc.replace('<section class="sec cta-band">', '<section class="sec cta-band reveal" id="svc-cta">', 1)
    if fname == "technologies.html":
        for n, g in enumerate(["Cloud &amp; Infrastructure", "Data &amp; BI", "Application Development", "DevOps &amp; Automation", "AI &amp; Automation"], 1):
            k = doc.index(f"<h2>{g}</h2>")
            s = doc.rindex('<section class="sec', 0, k)
            e = doc.index(">", s)
            doc = doc[:e] + f' id="tg{n}"' + doc[e:]
        doc = doc.replace('<section class="sec cta-band">', '<section class="sec cta-band reveal" id="tg-cta">', 1)
    if fname == "talent.html":
        for n, g in ((1, "Work with us your way"), (2, "Skills we place")):
            k = doc.index(f"<h2>{g}</h2>")
            s = doc.rindex('<section class="sec', 0, k)
            e = doc.index(">", s)
            doc = doc[:e] + f' id="tl{n}"' + doc[e:]
        doc = doc.replace('<section class="sec cta-band">', '<section class="sec cta-band reveal" id="tl-cta">', 1)
        doc = doc.replace("</head>", '<link rel="stylesheet" href="talent-page.css"></head>', 1)
    if fname == "about.html":
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="head reveal"><p class="eyebrow">Approach', '<section class="sec" id="approach"><div class="wrap"><div class="head reveal"><p class="eyebrow">Approach', 1)
        doc = doc.replace('<section class="sec alt"><div class="wrap"><div class="head reveal"><p class="eyebrow">Values', '<section class="sec alt" id="values"><div class="wrap"><div class="head reveal"><p class="eyebrow">Values', 1)
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="two">', '<section class="sec" id="story"><div class="wrap"><div class="two">', 1)
    if fname == "technologies.html":
        doc = doc.replace("</head>", '<link rel="stylesheet" href="tech-modal.css"><link rel="stylesheet" href="tech-page.css"></head>').replace("</body>", '<script src="tech-modal.js"></script></body>')
    doc = STEP.sub(lambda m: num(m.group(1)), doc)
    (OUT / fname).write_text(doc, encoding="utf-8")

def sec(inner, alt=False, narrow=False):
    return f'<section class="sec{" alt" if alt else ""}"><div class="wrap{" narrow" if narrow else ""}">{inner}</div></section>'

def cards(items, feature=None):
    return '<div class="grid3">' + "".join(
        f'<div class="card reveal{" feature" if i == feature else ""}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(items)) + '</div>'

def head(e, t, m=""):
    return f'<div class="head reveal"><p class="eyebrow">{e}</p><h2>{t}</h2>{f"<p class=muted>{m}</p>" if m else ""}</div>'

def flips(items):
    return '<div class="grid3">' + "".join(
        f'<div class="flip reveal" tabindex="0"><div class="flip-in"><div class="face front"><h3>{t}</h3><p>{s}</p><span class="hint">Hover to read more</span></div>'
        f'<div class="face back"><h3>{t}</h3><p>{d}</p></div></div></div>' for t, s, d in items) + '</div>'

def checks(items):
    return '<ul class="checks reveal">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

# ---------------- Services ----------------
SERVICES = {
 "cloud": ("Cloud Implementation", "☁", "Plan, migrate and run workloads on the cloud with security and cost control built in.",
   ["Cloud readiness assessment and landing-zone design", "Lift-and-shift and re-platform migrations", "Identity, networking and security baselines", "Cost monitoring and optimisation", "Backup, disaster recovery and high availability"],
   ["AWS", "Microsoft Azure", "Google Cloud", "Terraform"]),
 "data-bi": ("Data Warehousing & BI", "▦", "Turn scattered data into a trusted warehouse and dashboards leaders actually use.",
   ["Data warehouse and data mart design", "ETL / ELT pipeline development", "Data quality, governance and lineage", "Dashboards and self-service reporting", "Performance tuning of existing BI estates"],
   ["SQL", "ETL", "Power BI", "Tableau"]),
 "development": ("Core Development", "⌘", "Custom web and enterprise software, from requirements to handover.",
   ["Requirement gathering and solution design", "Web and enterprise application development", "API and integration development", "Testing and quality assurance", "Documentation and structured handover"],
   ["Java", ".NET", "Python", "React"]),
 "migration": ("Migration & Modernisation", "⇄", "Move off costly legacy development tools onto modern, maintainable platforms.",
   ["Application and code-base assessment", "Legacy tool and database migration", "Re-architecture and re-platforming", "Parallel runs and rollback planning", "Knowledge transfer to your team"],
   ["Legacy to modern", "Databases", "Cloud", "APIs"]),
 "devops": ("DevOps & Automation", "∞", "Ship faster and keep systems stable with automated pipelines and monitoring.",
   ["CI/CD pipeline design and implementation", "Infrastructure as code", "Containerisation and orchestration", "Monitoring, logging and alerting", "Release and environment automation"],
   ["Docker", "Kubernetes", "Jenkins", "Terraform"]),
 "consulting": ("IT Consulting", "◈", "Independent advice on IT strategy, project management, systems design and deployment.",
   ["Technology strategy and roadmaps", "IT project and programme management", "Systems design and architecture reviews", "Software and hardware deployment", "Vendor and tool selection support"],
   ["Strategy", "Architecture", "PMO", "Deployment"]),
}

def build_services():
    grid = '<div class="grid3">' + "".join(
        f'<a class="card svc reveal" href="svc-{k}.html"><div class="ic">{v[1]}</div><h3>{html.escape(v[0])}</h3><p>{v[2]}</p><span class="more">Learn more →</span></a>'
        for k, v in SERVICES.items()) + "</div>"
    page("services.html", "IT Services & Solutions", "Cloud, data warehousing & BI, development, migration, DevOps and IT consulting from NDR Infotech, Bangalore.",
         "IT solutions &amp; <span class=\"grad\">business services</span>", "Six capability areas delivered by one accountable team.",
         sec(head("Capabilities", "What we do") + grid) +
         sec(head("Industries", "Where we apply it", "Enterprise and financial-services domains, plus any organisation modernising legacy systems.") +
             cards([("Financial services", "Reporting, data platforms and core application support."),
                    ("Enterprise IT", "Modernising internal systems and moving off ageing tools."),
                    ("Growing businesses", "Cloud-first platforms and on-demand engineering capacity.")]), alt=True),
         "Services")
    for k, (name, ic, summ, points, tags) in SERVICES.items():
        others = "".join(f'<a href="svc-{o}.html">{html.escape(v[0])}</a>' for o, v in SERVICES.items() if o != k)
        body = sec('<div class="two"><div class="reveal">' + head("Overview", html.escape(name), summ) +
                   '<p>We start from your goals and constraints, agree a clear scope, and deliver iteratively with regular demos and quality gates.</p>'
                   '</div><div class="card reveal"><h3>What\'s included</h3>' + checks(points) + '</div></div>') + \
               sec(head("Tools & focus", "Typical technologies") + '<div class="chips reveal">' + "".join(f"<span>{t}</span>" for t in tags) + "</div>", alt=True) + \
               sec(head("Explore more", "Other services") + f'<div class="chips reveal links">{others}</div>')
        page(f"svc-{k}.html", name, summ, html.escape(name).replace("&amp;amp;", "&amp;"), summ, body, "Service")

# ---------------- About ----------------
def build_about():
    page("about.html", "About Us", "NDR Infotech is a Bangalore-based product development, software services, financial services and technology consulting company with over 20 years of experience.",
         "Engineering that <span class=\"grad\">earns trust</span>", "A focused product development, software services and technology consulting company based in Bangalore.",
         sec('<div class="two"><div class="reveal">' + head("Our story", "Two decades of delivery") +
             '<p>NDR Infotech has handled projects for over two decades, from requirement gathering through to handover. We combine strategy, analytics and engineering depth to turn ideas into dependable products.</p>'
             '<p>We help enterprises move away from costly legacy development tools to modern platforms, and we stay accountable long after go-live.</p></div>'
             '<div class="cards-s">' + "".join(f'<div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in
              [("Mission", "Empowering businesses for excellence through practical, well-engineered technology."),
               ("Strategy → Execution → Success", "Plan clearly, build carefully, and measure outcomes."),
               ("Where we are", "BTM 2nd Stage, Bangalore, working with clients remotely and on-site.")]) + '</div></div>') +
         sec(head("Values", "How we work") + flips([
              ("Clarity", "Plain-language scope, estimates and status.", "You always know what is being built, what it costs and where it stands. We write scope, estimates and weekly status in plain language, with no jargon and no surprises."),
              ("Ownership", "One accountable team from kickoff to handover.", "A single team owns the outcome end to end. When something needs attention, you have one point of contact who takes responsibility instead of passing it along."),
              ("Quality", "Testing and review built into every iteration.", "Code review, automated tests and demo checkpoints are part of every iteration, so problems are caught early and not at launch."),
              ("Longevity", "Maintainable systems and honest documentation.", "We build systems your team can run and extend years from now, with clear documentation and structured knowledge transfer at handover."),
              ("Partnership", "We act as an extension of your team.", "We work inside your processes and tools, share risks openly, and treat your goals as our own, long after the project ends."),
              ("Pragmatism", "The right tool for the job, not the trendiest.", "We recommend the simplest technology that solves the problem reliably and fits your budget, even when it is not the newest option.")]), alt=True) +
         sec(head("Approach", "From idea to handover") + '<ol class="steps">' + "".join(
              f'<li class="reveal"><span>0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(
              [("Discover", "Goals, constraints, success metrics."), ("Design", "Architecture, roadmap, estimate."),
               ("Deliver", "Iterative builds with demos."), ("Support", "Handover and continuous improvement.")])) + "</ol>"),
         "About us")

# ---------------- Technologies ----------------
def build_tech():
    import json
    from icons import svg
    from techdata import TECH
    groups = [("Cloud & Infrastructure", [("AWS","cloud"),("Microsoft Azure","cloud"),("Google Cloud","cloud"),("Terraform","layers"),("Linux","term")]),
              ("Data & BI", [("SQL","data"),("NoSQL","box"),("ETL / ELT","pipe"),("Data Warehousing","server"),("Power BI","bars"),("Tableau","chart")]),
              ("Application Development", [("Java","code"),(".NET","layers"),("Python","term"),("JavaScript","code"),("React","gear"),("REST APIs","api")]),
              ("DevOps & Automation", [("Docker","box"),("Kubernetes","gear"),("Jenkins","pipe"),("Git","git"),("CI/CD","devops"),("Monitoring","chart")]),
              ("AI & Automation", [("Process automation","gear"),("Analytics","chart"),("Applied AI","spark")])]
    data = {}
    def tiles(g, ts):
        out = []
        for n, ic in ts:
            d, pts = TECH[n]
            data[n] = {"group": g, "desc": d, "points": pts, "icon": svg(ic)}
            out.append(f'<div class="tile" role="button" tabindex="0" aria-haspopup="dialog" data-tech="{html.escape(n, quote=True)}">{svg(ic)}<span>{html.escape(n)}</span><em>View details</em></div>')
        return '<div class="tiles reveal">' + "".join(out) + "</div>"
    body = "".join(sec(head("Stack", html.escape(g)) + tiles(g, ts), alt=i % 2 == 1) for i, (g, ts) in enumerate(groups))
    body += '<script type="application/json" id="tech-data">' + json.dumps(data).replace("</", "<\\/") + "</script>"
    page("technologies.html", "Technologies", "Cloud, data, application development, DevOps and automation technologies used by NDR Infotech.",
         "Technologies blended for <span class=\"grad\">today's business</span>", "Indicative stack. We choose tools to fit each engagement. Click any tile for details.", body, "Technologies")

# ---------------- Talent ----------------
def build_talent():
    page("talent.html", "On-Demand IT Talent", "Staff augmentation, dedicated teams and project delivery from NDR Infotech.",
         "On-demand <span class=\"grad\">IT talent</span>", "Skilled engineers, analysts and project managers, when and how you need them.",
         sec(head("Engagement models", "Work with us your way") + cards([
              ("Staff Augmentation", "Add vetted professionals to your team quickly for short or long assignments."),
              ("Dedicated Team", "A managed team aligned to your roadmap with shared accountability."),
              ("Fixed-Scope Project", "Defined outcomes, timeline and budget for well-scoped initiatives.")], feature=1)) +
         sec('<div class="two"><div class="reveal">' + head("Roles", "Skills we place") +
             checks(["Software engineers (Java, .NET, Python, JavaScript)", "Cloud and DevOps engineers", "Data engineers and BI developers", "QA and test automation", "Project and programme managers", "Business and systems analysts"]) +
             '</div><div class="reveal">' + head("Process", "How it works") +
             '<ol class="steps one"><li><span>01</span><h3>Brief</h3><p>Share role, skills and timeline.</p></li><li><span>02</span><h3>Shortlist</h3><p>We screen and present suitable profiles.</p></li>'
             '<li><span>03</span><h3>Onboard</h3><p>Interview, confirm, and start quickly.</p></li></ol></div></div>', alt=True),
         "Talent")

# ---------------- Contact ----------------
def build_contact():
    body = sec('''<div class="two"><div class="reveal"><h2>Let's build something dependable.</h2>
<p class="muted">Tell us about your project and we'll get back to you.</p>
<ul class="info"><li><b>Phone</b><a href="tel:+918722355999">%s</a></li><li><b>Email</b><a href="mailto:%s">%s</a></li>
<li><b>Address</b><span>#415, 8th Cross, 8th Main, Sunshine Layout, BTM 2nd Stage, Bangalore, Karnataka 560076</span></li></ul>
<a class="btn ghost" href="https://www.google.com/maps/search/?api=1&amp;query=BTM+2nd+Stage+Sunshine+Layout+Bangalore+560076" rel="noopener" target="_blank">Open in Maps</a></div>
<form class="card form reveal" id="form" novalidate>
<label>Name<input name="name" required autocomplete="name"></label>
<label>Work email<input name="email" type="email" required autocomplete="email"></label>
<label>I'm interested in<select name="topic"><option>Cloud</option><option>Data &amp; BI</option><option>Development</option><option>Migration</option><option>DevOps</option><option>IT Talent</option><option>Other</option></select></label>
<label>Message<textarea name="msg" rows="4" required></textarea></label>
<button class="btn" type="submit">Send message</button><p class="note" id="note" role="status"></p></form></div>''' % (PHONE, EMAIL, EMAIL))
    page("contact.html", "Contact", "Contact NDR Infotech, BTM 2nd Stage, Bangalore.", "Get in <span class=\"grad\">touch</span>",
         "A short brief is all we need to start the conversation.", body, "Contact")
    # contact page has its own CTA band that's redundant; strip it
    p = OUT / "contact.html"
    t = p.read_text(encoding="utf-8")
    a = t.index('<section class="sec cta-band">'); b = t.index("</section>", a) + len("</section>")
    p.write_text(t[:a] + t[b:], encoding="utf-8")


# ---------------- Legal pages ----------------
def build_legal():
    from legal import PRIVACY, TERMS, UPDATED
    def render(items):
        toc = "".join(f'<li><a href="#s{i}">{html.escape(t)}</a></li>' for i, (t, _) in enumerate(items, 1))
        out = []
        for i, (t, parts) in enumerate(items, 1):
            inner = ""
            for p in parts:
                if isinstance(p, tuple):
                    inner += "<ul class=\"checks\">" + "".join(f"<li>{x}</li>" for x in p[1]) + "</ul>"
                else:
                    inner += f"<p>{p}</p>"
            out.append(f'<section class="lg" id="s{i}"><h2><span>{i:02d}</span>{html.escape(t)}</h2>{inner}</section>')
        return f'<section class="sec"><div class="wrap legal"><aside class="toc"><p class="eyebrow">On this page</p><ol>{toc}</ol></aside><article class="legal-body"><p class="muted">Last updated: {UPDATED}</p>' + "".join(out) + "</article></div></section>"
    for fname, title, desc, h1, lead, items in (
        ("privacy.html", "Privacy Policy", "How NDR Infotech collects, uses and protects personal information.", "Privacy <span class=\"grad\">Policy</span>", "What we collect, why we collect it and the choices you have.", PRIVACY),
        ("terms.html", "Terms & Conditions", "Terms governing use of the NDR Infotech website and our services.", "Terms &amp; <span class=\"grad\">Conditions</span>", "The ground rules for using this website and working with us.", TERMS)):
        page(fname, title, desc, h1, lead, render(items), html.escape(title))
        p = OUT / fname
        t = p.read_text(encoding="utf-8")
        a = t.index('<section class="sec cta-band">'); e = t.index("</section>", a) + len("</section>")
        p.write_text(t[:a] + t[e:], encoding="utf-8")

if __name__ == "__main__":
    build_services(); build_about(); build_tech(); build_talent(); build_contact(); build_legal()
    print("built")
