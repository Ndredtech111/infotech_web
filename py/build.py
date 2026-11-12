"""Generates the inner pages of the NDR Infotech site. Run: py py/build.py"""
import html, pathlib
from icons import decorate

OUT = pathlib.Path(__file__).resolve().parent.parent
PHONE, EMAIL = "+91 87223 55999", "hr@ndrinfotech.com"

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("technologies.html", "Technologies"), ("talent.html", "Talent"), ("wealth.html", "Wealth"), ("contact.html", "Contact")]

LOGO = '<img class="logo-img" src="images/logo-mark.png" alt="" width="46" height="54">'

ICONS = {5: '<path d="M12 6v36"/><path d="M12 8h24l-6 8 6 8H12"/>', 1: '<circle cx="21" cy="21" r="11"/><path d="M29 29l11 11"/><path d="M17 21h8M21 17v8"/>', 2: '<path d="M8 40l4-12L34 6l8 8-22 22z"/><path d="M28 12l8 8"/><path d="M8 40l8-3"/>', 3: '<path d="M24 6c8 4 12 12 10 22l-6 6H20l-6-6C12 18 16 10 24 6z"/><circle cx="24" cy="19" r="3"/><path d="M14 32l-6 8 10-3M34 32l6 8-10-3"/>', 4: '<path d="M24 5l16 6v12c0 10-7 17-16 20C15 40 8 33 8 23V11z"/><path d="M17 24l5 5 9-10"/>'}
def num(n):
    n = int(n)
    return f'<span class="num"><i>0{n}</i><svg viewBox="0 0 48 48" aria-hidden="true">{ICONS[n]}</svg></span>'
import re
STEP = re.compile(r'<span>0([1-5])</span>')

SCENES = {"about.html": "network", "services.html": "orbit", "technologies.html": "code", "talent.html": "network",
          "contact.html": "pulse", "wealth.html": "bars", "svc-cloud.html": "cloud", "svc-data-bi.html": "bars", "svc-development.html": "code",
          "svc-migration.html": "flow", "svc-devops.html": "loop", "svc-consulting.html": "radar"}

def page(fname, title, desc, h1, lead, body, eyebrow=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == fname or (fname.startswith("svc-") and h == "services.html") else ""}>{t}</a>'
        for h, t in NAV[1:-1])
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} | NDR Infotech</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="https://www.ndrinfotech.com/{fname}">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png"><link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
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
<footer class="foot"><div class="wrap foot-in"><p>© <span id="yr">2022</span> NDR Infotech · Bangalore</p>
<p><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms &amp; Conditions</a></p></div></footer>
<script src="js/script.js"></script><script src="js/hero-bg.js"></script></body></html>'''
    doc = decorate(doc)
    if fname == "services.html":
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="head reveal"><p class="eyebrow">Capabilities', '<section class="sec" id="caps"><div class="wrap"><div class="head reveal"><p class="eyebrow">Capabilities', 1)
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
        doc = doc.replace("</head>", '<link rel="stylesheet" href="css/talent-page.css"></head>', 1)
    if fname == "about.html":
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="head reveal"><p class="eyebrow">Approach', '<section class="sec" id="approach"><div class="wrap"><div class="head reveal"><p class="eyebrow">Approach', 1)
        doc = doc.replace('<section class="sec alt"><div class="wrap"><div class="head reveal"><p class="eyebrow">Values', '<section class="sec alt" id="values"><div class="wrap"><div class="head reveal"><p class="eyebrow">Values', 1)
        doc = doc.replace('<section class="sec"><div class="wrap"><div class="two">', '<section class="sec" id="story"><div class="wrap"><div class="two">', 1)
    if fname == "technologies.html":
        doc = doc.replace("</head>", '<link rel="stylesheet" href="css/tech-modal.css"><link rel="stylesheet" href="css/tech-page.css"></head>').replace("</body>", '<script src="js/tech-modal.js"></script></body>')
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
    why = ('<div class="two"><div class="reveal">' + head("Why choose us", "Our passion to innovate, devise your solutions") +
           '<p>We never compromise on quality and punctuality. Our own growth depends on our clients, which is why we are so clear about what we deliver and when.</p>'
           '<p>One accountable team takes you from requirements to handover, and stays with you after go-live.</p></div>'
           '<div class="cards-s">' + "".join(f'<div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in [
               ("Quality, uncompromised", "Code review, testing and demo checkpoints are built into every iteration."),
               ("On time, every time", "Realistic estimates, visible milestones and weekly status, so deadlines are kept."),
               ("Your growth is ours", "We measure success by what your business achieves, not by hours billed."),
               ("Clear on what and when", "Plain-language scope and delivery dates agreed up front, with no surprises.")]) + '</div></div>')
    more_items = [
        ("AI, ML, IoT &amp; RPA", "Automate repetitive work and find patterns in your data with applied AI, machine learning, connected-device (IoT) solutions and robotic process automation.", None),
        ("Application Innovation", "Modernise and extend your applications with new features, a better user experience and cleaner architecture.", "svc-development.html"),
        ("Big Data &amp; Analytics", "Collect, process and analyse large volumes of data to produce insight your teams can act on.", "svc-data-bi.html"),
        ("Cloud &amp; Digital Services", "Plan, move and run workloads in the cloud, and digitise customer-facing and internal processes.", "svc-cloud.html"),
        ("Corporate Training", "Practical, role-based training that brings your teams up to speed on the tools and technologies you adopt.", None),
        ("DevOps Services", "Automated pipelines, infrastructure as code and monitoring for faster, safer releases.", "svc-devops.html"),
        ("Staffing &amp; Recruitment", "Skilled engineers, analysts and project managers matched to your needs, on contract or permanent.", "talent.html"),
        ("Testing &amp; Automation", "Functional, regression and performance testing with automation to catch defects before your users do.", None),
        ("Technology Operations &amp; Support", "Monitoring, maintenance and support that keep systems stable and issues resolved quickly after go-live.", None)]
    more = '<div class="grid3 xgrid">' + "".join(
        (f'<a class="card svc reveal" href="{h}"><h3>{n}</h3><p>{d}</p><span class="more">Learn more →</span></a>' if h else f'<div class="card reveal"><h3>{n}</h3><p>{d}</p></div>')
        for n, d, h in more_items) + '</div>'
    ind_items = [
        ("E-Commerce", "Catalogue, order and payment platforms, plus analytics and integrations that scale with demand."),
        ("Financial Services", "Reporting, data platforms and core application support for banks, insurers and wealth firms."),
        ("Government", "Reliable, well-documented systems and modernisation of legacy applications for public-sector needs."),
        ("Healthcare", "Application and data support for providers and health organisations, with care for sensitive information."),
        ("Manufacturing", "Operations, supply-chain reporting and automation that give planners a clear picture."),
        ("Retail", "Inventory, sales and customer analytics that help retailers stock and sell smarter."),
        ("Telecom", "Data, reporting and platform support for high-volume telecom environments.")]
    industries = '<div class="xind">' + "".join(f'<div class="card reveal"><h3>{n}</h3><p>{d}</p></div>' for n, d in ind_items) + '</div>'
    life_items = [
        ("ACORD Applications", "Capture and process standard application forms accurately for commercial and personal lines."),
        ("Quotations", "Prepare carrier quotes quickly and compare options side by side."),
        ("Proposals", "Turn selected quotes into clear, client-ready proposals."),
        ("Bind Orders", "Prepare and submit bind orders once the client accepts."),
        ("Binders", "Issue binders so cover is confirmed while the policy is being finalised."),
        ("Policies", "Check and issue the final policy documents accurately and on time.")]
    life = '<ol class="xlife reveal">' + "".join(f'<li><b>{i:02d}</b><h3>{n}</h3><p>{d}</p></li>' for i, (n, d) in enumerate(life_items, 1)) + '</ol>'
    sam = ('<div class="two"><div class="reveal">' + head("Small accounts management", "Grow your small-business books") +
           '<p>Our Small Accounts Management solution integrates seamlessly with your agency. It helps you manage and grow your property &amp; casualty (P&amp;C) and employee benefits (EB) small-business books, while you retain your Agency of Record (AOR) status.</p></div>'
           '<div class="card reveal"><h3>What you get</h3>' + checks([
               "Seamless integration with your agency's existing processes",
               "Management of P&amp;C and EB small-business books",
               "Support to grow the book without adding headcount",
               "You retain your Agency of Record (AOR) status"]) + '</div></div>')
    ag_items = [("Audits", "Premium and policy audits handled end to end."), ("Cancellation", "Cancellation requests processed and confirmed."),
        ("Claims Processing", "Claims logged, tracked and followed up."), ("COI", "Certificates of insurance issued quickly on request."),
        ("Data Management", "Clean, consistent data inside your agency software and applications."), ("E-Delivery", "Policy documents delivered electronically."),
        ("Endorsement Processing", "Mid-term changes processed accurately."), ("Invoicing", "Invoices prepared and reconciled."),
        ("Loss Runs", "Loss runs requested, collected and organised."), ("Quotations / Re-shop", "Fresh quotes gathered to keep clients competitively placed."),
        ("Policy Checking", "Issued policies checked against what was bound."), ("Policy Issuance", "Policies issued completely and on time."),
        ("Renewals", "Renewals tracked and processed ahead of expiry."), ("Reinsurance", "Reinsurance placement and administration support.")]
    agency = '<div class="xag">' + "".join(f'<div class="card reveal"><h3>{n}</h3><p>{d}</p></div>' for n, d in ag_items) + '</div>'
    page("services.html", "IT Services & Solutions", "Cloud, data, AI, DevOps, testing, staffing, training and insurance back-office services from NDR Infotech, Bangalore.",
         "IT solutions &amp; <span class=\"grad\">business services</span>", "Core capability areas, specialist services and insurance operations, delivered by one accountable team.",
         sec(why, alt=True) +
         sec(head("Capabilities", "What we do") + grid) +
         sec(head("More services", "Specialist services around your technology", "Nine ways we support your teams, from AI to training to day-to-day operations.") + more, alt=True) +
         sec(head("Industries", "Where we apply it", "Seven sectors where our teams have experience, plus any organisation modernising legacy systems.") + industries) +
         sec(head("Insurance processing", "Commercial &amp; personal lines, from application to policy", "Six steps of the policy lifecycle that we handle for agencies.") + life, alt=True) +
         sec(sam) +
         sec(head("Services for agencies", "Brokers, MGAs &amp; carriers", "Fourteen operational services that take routine work off your team's desk.") + agency, alt=True),
         "Services")
    p = OUT / "services.html"
    d = p.read_text(encoding="utf-8")
    for n, g in enumerate(["Our passion to innovate, devise your solutions", "Specialist services around your technology", "Where we apply it",
                           "Commercial &amp; personal lines, from application to policy", "Grow your small-business books", "Brokers, MGAs &amp; carriers"], 1):
        k = d.index(f"<h2>{g}</h2>")
        a = d.rindex('<section class="sec', 0, k)
        e = d.index(">", a)
        d = d[:a] + d[a:e].replace('class="sec', 'class="xsec sec', 1) + f' id="x{n}"' + d[e:]
    d = d.replace("</head>", '<link rel="stylesheet" href="css/services-page.css"></head>', 1)
    p.write_text(d, encoding="utf-8")
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
    body = sec('''<div class="two"><div class="reveal"><div class="c-tech"><svg class='c-orbit' viewBox='-106 -106 212 212' aria-hidden='true'><circle class='rip r1' r='66'/><circle class='rip r2' r='66'/><circle class='rip r3' r='66'/><circle class='tk' r='85'/><circle class='dd' r='76'/><g transform='rotate(0)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:0.00s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:0.00s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(45)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:0.45s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:0.30s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(90)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:0.90s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:0.60s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(135)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:1.35s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:0.90s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(180)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:1.80s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:1.20s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(225)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:2.25s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:1.50s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(270)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:2.70s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:1.80s' cx='7' cy='-97' r='2.4'/></g><g transform='rotate(315)'><path class='tr' d='M0 -70V-80L7 -87V-97'/><path class='pk' style='animation-delay:3.15s' d='M0 -70V-80L7 -87V-97'/><circle class='nd' style='animation-delay:2.10s' cx='7' cy='-97' r='2.4'/></g><g class='orb o1'><circle cx='0' cy='-102' r='3.2'/></g><g class='orb o2'><circle cx='0' cy='-90' r='2.6'/></g><g class='orb o3'><circle cx='0' cy='-80' r='2.2'/></g></svg><div class="c-logo"><img src="images/logo-full.png" alt="NDR Infotech logo" width="86" height="106"></div></div><h2>Let's build something dependable.</h2>
<p class="muted">Tell us about your project and we'll get back to you.</p>
<ul class="info"><li><b>Phone</b><a href="tel:+918722355999">%s</a></li><li><b>Email</b><a href="mailto:%s">%s</a></li>
<li><b>Address</b><span>#415, 8th Cross, 8th Main, Sunshine Layout, BTM 2nd Stage, Bangalore, Karnataka 560076</span></li></ul>
<a class="btn ghost" href="https://www.google.com/maps/place/NDR+INFOTECH/@12.9134507,77.6048044,1069m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3bae15682da3fe69:0x737fbd1a094a2ebf!8m2!3d12.9134455!4d77.6073793!16s%%2Fg%%2F11swl478k1" rel="noopener" target="_blank">Open in Maps</a></div>
<form class="card form reveal" id="form" novalidate>
<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0;height:0;width:0">
<label>Name<input name="name" required autocomplete="name"></label>
<label>Work email<input name="email" type="email" required autocomplete="email"></label>
<label>I'm interested in<select name="topic"><option>Cloud</option><option>Data &amp; BI</option><option>Development</option><option>Migration</option><option>DevOps</option><option>IT Talent</option><option>Wealth Management</option><option>Other</option></select></label>
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

# ---------------- Wealth ----------------
def build_wealth():
    provide = cards([
        ("Portfolio monitoring &amp; rebalancing", "Track every holding in one view, review performance against your goals and rebalance when allocations drift from plan."),
        ("Investments, done right", "Mutual funds, NPS, PPF, FD/RD and more, chosen for your goals, time horizon and risk comfort rather than for the latest trend."),
        ("Tax saving, optimised", "Plan investments, deductions and timing so you keep more of what you earn, within the rules."),
        ("Goals, achieved", "Retirement, a home, children's education or a business: each goal gets an amount, a deadline and a monthly path to reach it."),
        ("Loans, suitably availed", "Compare options and structure borrowing so EMIs fit comfortably within your cash flow and long-term plan."),
        ("Insurance &amp; protection", "Review life and health cover so an unexpected event does not derail the goals you are building towards.")])
    steps = ('<ol class="steps wsteps reveal">'
        '<li><span>01</span><h3>Assess your financial position</h3><p>We review income, expenses, assets and liabilities to see exactly where you stand today.</p></li>'
        '<li><span>02</span><h3>Set your financial goals</h3><p>Define how much money you need, and by when, for each goal that matters to you.</p></li>'
        '<li><span>03</span><h3>Assess your risk</h3><p>A short psychometric risk-assessment test shows how much market movement you can comfortably live with.</p></li>'
        '<li><span>04</span><h3>Generate your financial plan</h3><p>You receive recommendations across mutual funds, NPS, PPF, FD/RD, insurance, loans and tax-saving schemes, including when and how much to invest.</p></li>'
        '<li><span>05</span><h3>Execute your financial plan</h3><p>Execute on any platform you prefer. You can also use our own free platform for the recommended mutual fund investments, with no commission.</p></li></ol>')
    stages = ('<ol class="steps reveal">'
        '<li><span>01</span><h3>Assessment</h3><p>A representative completes a questionnaire on your current financial position, goals and preferences.</p></li>'
        '<li><span>02</span><h3>Preparation</h3><p>Our analysts study the information and prepare a detailed action plan built around your goals.</p></li>'
        '<li><span>03</span><h3>Execution</h3><p>Portfolio managers and back-end staff carry out the investments and paperwork on your behalf.</p></li>'
        '<li><span>04</span><h3>Monitor &amp; adjust</h3><p>We track performance regularly and adjust the plan as markets, income or life goals change.</p></li></ol>')
    advisory = flips([
        ("Investment Advisory", "Portfolio management for high-net-worth clients.", "Tracking and consolidation of all holdings, tax management, performance dashboards and ongoing advice tailored to large and complex portfolios."),
        ("Retirement Planning", "Plan today for a comfortable tomorrow.", "We estimate the corpus you will need, build the savings path to reach it and structure post-retirement income and withdrawals so your money lasts."),
        ("Financial Planning Lite", "A quick, clear picture of your finances.", "A focused assessment of present and future finances that forecasts cash flow, highlights gaps and gives you practical next steps."),
        ("Tax Planning", "Reduce liability, maximise savings.", "We analyse your complete financial situation and recommend the right instruments and timing to lower your tax outgo legitimately."),
        ("Child Education Plan", "Fund your child's future without stress.", "We estimate future education costs, including inflation, and set up a goal-based investment plan with a monthly amount and timeline."),
        ("Estate Planning", "Protect and pass on what you have built.", "Guidance on managing, transferring and disposing of your estate, both during your lifetime and after, so your family is provided for."),
        ("Corporate Offering", "Advisory for companies and their treasuries.", "Investment advisory for corporate surplus funds, covering liquidity needs, risk and overall financial performance."),
        ("Family Office Services", "Integrated advice for wealthy families.", "Coordinated wealth advice for families and family businesses, with tax and legal specialists involved where needed.")])
    why = checks([
        "Goal-based planning: every recommendation traces back to a goal you set",
        "Psychometric risk profiling, so the plan fits you and not an average investor",
        "Commission-free mutual fund execution on our own platform",
        "Platform-agnostic: execute wherever you are comfortable",
        "Dedicated analysts and portfolio managers, not a call centre",
        "Regular reviews with clear, plain-language reporting"])
    faq_items = [
        ("Who is this for?", "Salaried professionals, business owners, families and corporates who want a structured plan instead of scattered investments. We have a lighter plan for simple needs and a full advisory service for larger portfolios."),
        ("How long does it take to get a plan?", "After the questionnaire and risk assessment, our analysts prepare your plan and walk you through it. Timelines depend on how many accounts and goals are involved; we will confirm them in the first conversation."),
        ("Do I have to invest through you?", "No. You can execute the plan through any platform. If you prefer, you can use our own free platform for recommended mutual fund investments, which carries no commission."),
        ("Will you keep reviewing my plan?", "Yes. In the Monitor &amp; adjust stage we track performance and update the plan when markets or your circumstances change."),
        ("What do I need to get started?", "Basic details of your income, expenses, existing investments, loans and goals. Share a short brief and we will take it from there.")]
    faq = '<div class="faq reveal">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq_items) + '</div>'
    page("wealth.html", "Wealth Management & Financial Planning", "Complete financial planning from NDR Infotech: goal-based investment advice, tax planning, retirement, estate and corporate advisory.",
         "Complete <span class=\"grad\">financial planning</span>, in one place", "Investment advice, tax saving, goals and loans, planned around you and reviewed as your life changes.",
         sec(head("What we provide", "Everything your money needs", "One team for planning, investing, protecting and growing your wealth.") + provide) +
         sec(head("Our process", "Five steps to your financial plan") + steps, alt=True) +
         sec(head("Our stages", "How we work with you", "From the first questionnaire to ongoing reviews.") + stages) +
         sec(head("Advisory services", "Services for every stage of life", "Hover or tap a card to read more.") + advisory, alt=True) +
         sec('<div class="two"><div class="reveal">' + head("Why NDR", "A plan built around you") + why + '</div><div class="reveal">' + head("FAQ", "Common questions") + faq + '</div></div>') +
         sec('<p class="muted reveal">Investments are subject to market risks. The information on this page is general in nature and is not a guarantee of returns. Please read all scheme-related documents carefully, and speak with us about your individual situation.</p>', narrow=True),
         "Wealth management")
    p = OUT / "wealth.html"
    t = p.read_text(encoding="utf-8")
    for n, g in enumerate(["Everything your money needs", "Five steps to your financial plan", "How we work with you", "Services for every stage of life", "A plan built around you"], 1):
        k = t.index(f"<h2>{g}</h2>")
        a = t.rindex('<section class="sec', 0, k)
        e = t.index(">", a)
        t = t[:a] + t[a:e].replace('class="sec', 'class="wsec sec', 1) + f' id="w{n}"' + t[e:]
    t = t.replace('<section class="sec cta-band">', '<section class="sec cta-band reveal" id="w-cta">', 1)
    t = t.replace("</head>", '<link rel="stylesheet" href="css/wealth-page.css"></head>', 1).replace("</body>", '<script src="js/wealth-page.js"></script></body>', 1)
    t = t.replace("<h2>Ready to talk about your project?</h2>", "<h2>Get your personalised financial plan</h2>").replace("Share a short brief and we'll respond to set up a discovery conversation.", "Tell us about your goals and we will set up a no-obligation conversation.").replace(">Contact us</a>", ">Get my plan</a>", 1)
    p.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    build_services(); build_about(); build_tech(); build_talent(); build_wealth(); build_contact(); build_legal()
    print("built")
