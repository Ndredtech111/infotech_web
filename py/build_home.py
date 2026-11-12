"""Rebuilds the body of index.html (everything after the marquee). Run: py py/build_home.py"""
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
from icons import svg

CHALLENGES = [
 ("Legacy tools cost too much", "migrate", "Migration & Modernisation",
  "Move off ageing development tools and platforms onto maintainable ones, without stopping the business.",
  ["Assess the existing code base and risks", "Migrate in stages with a rollback plan", "Hand over documentation and training"], "svc-migration.html"),
 ("Our data is scattered", "data", "Data Warehousing & BI",
  "Bring data from many systems into one trusted warehouse and give leaders dashboards they can rely on.",
  ["Design the warehouse and data marts", "Build and monitor data pipelines", "Deliver dashboards and self-service reports"], "svc-data-bi.html"),
 ("Releases are slow and risky", "devops", "DevOps & Automation",
  "Automate build, test and deployment so changes reach users faster and with fewer surprises.",
  ["Set up CI/CD pipelines", "Define environments as code", "Add monitoring and alerting"], "svc-devops.html"),
 ("We want to move to the cloud", "cloud", "Cloud Implementation",
  "Plan and run your move to the cloud with security, governance and cost control built in.",
  ["Readiness assessment and landing zone", "Lift-and-shift or re-platform migrations", "Ongoing cost optimisation"], "svc-cloud.html"),
 ("We need engineers quickly", "talent", "On-Demand Talent",
  "Add vetted engineers, analysts and project managers on the engagement model that suits you.",
  ["Staff augmentation for short or long needs", "Dedicated teams aligned to your roadmap", "Fixed-scope projects with clear outcomes"], "talent.html"),
 ("We need a custom application", "code", "Core Development",
  "Take an idea from requirements to a tested, documented application handed over cleanly.",
  ["Requirements and solution design", "Iterative build with regular demos", "Testing, documentation and handover"], "svc-development.html"),
]

BENTO = [
 ("big", "services.html", "orbit", "Services", "Cloud, data, development, migration, DevOps and consulting delivered by one accountable team.", "Explore services"),
 ("", "technologies.html", "layers", "Technologies", "The tools and platforms we work with, and how we use them.", "See the stack"),
 ("", "talent.html", "team", "On-demand talent", "Staff augmentation, dedicated teams and fixed-scope projects.", "Hire talent"),
 ("w2", "about.html", "target", "About NDR", "Twenty-plus years of delivery from Bangalore.", "Our story"),
]


S = 'class="bt-bg" aria-hidden="true" focusable="false"'
BG = {
 # Services: orbiting rings around a core
 "services.html": f'<svg {S} viewBox="0 0 400 300" preserveAspectRatio="xMaxYMin slice"><g fill="none" stroke="#22d3ee" stroke-width="1">'
   '<circle cx="300" cy="120" r="30" opacity=".5"/><circle cx="300" cy="120" r="70" opacity=".3"/><circle cx="300" cy="120" r="115" opacity=".18" stroke-dasharray="3 7"/></g>'
   '<circle cx="300" cy="120" r="6" fill="#22d3ee"/>'
   '<g class="spin s1"><circle cx="370" cy="120" r="5" fill="#8b5cf6"/></g>'
   '<g class="spin s2"><circle cx="300" cy="50" r="4" fill="#22d3ee"/></g>'
   '<g class="spin s3"><circle cx="185" cy="120" r="3.5" fill="#8b5cf6"/></g></svg>',
 # Technologies: drifting code grid
 "technologies.html": f'<svg {S} viewBox="0 0 400 300" preserveAspectRatio="xMaxYMin slice"><defs><pattern id="pl" width="26" height="26" patternUnits="userSpaceOnUse">'
   '<path d="M13 9v8M9 13h8" stroke="#22d3ee" stroke-width="1" opacity=".55"/></pattern></defs>'
   '<rect class="drift" x="-40" y="-40" width="520" height="380" fill="url(#pl)"/>'
   '<text x="250" y="70" fill="#8b5cf6" opacity=".5" font-family="monospace" font-size="22">{ }</text>'
   '<text x="318" y="130" fill="#22d3ee" opacity=".45" font-family="monospace" font-size="20">&lt;/&gt;</text></svg>',
 # Talent: people network
 "talent.html": f'<svg {S} viewBox="0 0 400 300" preserveAspectRatio="xMaxYMin slice"><g stroke="#22d3ee" stroke-width="1" opacity=".35" fill="none">'
   '<path d="M250 60L320 100L370 50M320 100L300 170M320 100L390 150M300 170L370 200M250 60L230 130L300 170"/></g>'
   '<g fill="#22d3ee"><circle class="pn" cx="250" cy="60" r="5"/><circle class="pn d1" cx="320" cy="100" r="6" fill="#8b5cf6"/><circle class="pn d2" cx="370" cy="50" r="4"/>'
   '<circle class="pn d3" cx="300" cy="170" r="5"/><circle class="pn" cx="390" cy="150" r="4" fill="#8b5cf6"/><circle class="pn d2" cx="230" cy="130" r="4"/><circle class="pn d1" cx="370" cy="200" r="5"/></g></svg>',
 # About: pulsing target rings (our focus)
 "about.html": f'<svg {S} viewBox="0 0 400 300" preserveAspectRatio="xMaxYMid slice"><g fill="none" stroke="#8b5cf6" stroke-width="1.2">'
   '<circle class="ring" cx="330" cy="150" r="40"/><circle class="ring r2" cx="330" cy="150" r="40"/><circle class="ring r3" cx="330" cy="150" r="40"/></g>'
   '<circle cx="330" cy="150" r="5" fill="#22d3ee"/></svg>',
 # Contact: ripples from a signal point
 "contact.html": f'<svg {S} viewBox="0 0 800 200" preserveAspectRatio="xMaxYMid slice"><g fill="none" stroke="#22d3ee" stroke-width="1.2">'
   '<circle class="ring big" cx="680" cy="100" r="30"/><circle class="ring big r2" cx="680" cy="100" r="30"/><circle class="ring big r3" cx="680" cy="100" r="30"/></g>'
   '<circle cx="680" cy="100" r="6" fill="#22d3ee"/></svg>',
}

def challenges():
    tabs, panels = [], []
    for i, (q, ic, title, desc, pts, href) in enumerate(CHALLENGES):
        sel = i == 0
        tabs.append(f'<button class="ch-tab{" on" if sel else ""}" role="tab" id="tab{i}" aria-selected="{str(sel).lower()}" aria-controls="pan{i}" tabindex="{0 if i == 0 else -1}">'
                    f'<span class="ch-n">0{i+1}</span><span>{html.escape(q)}</span></button>')
        lis = "".join(f"<li>{html.escape(p)}</li>" for p in pts)
        panels.append(f'<div class="ch-pan{" on" if sel else ""}" role="tabpanel" id="pan{i}" aria-labelledby="tab{i}"{"" if sel else " hidden"}>'
                      f'{svg(ic)}<p class="eyebrow">Our answer</p><h3>{html.escape(title)}</h3><p class="ch-d">{html.escape(desc)}</p>'
                      f'<ul class="checks">{lis}</ul><a class="btn" href="{href}">See how we do it</a></div>')
    icons = "".join(
        f'<button class="ch-ic{" on" if i == 0 else ""}" type="button" aria-label="{html.escape(c[2])}" title="{html.escape(c[2])}">{svg(c[1])}</button>'
        for i, c in enumerate(CHALLENGES))
    return ('<section class="sec" id="challenges"><div class="wrap"><div class="head reveal"><p class="eyebrow">Where do you need help?</p>'
            '<h2>Start with the problem, not the product.</h2><p class="muted">Pick the situation closest to yours.</p></div>'
            '<div class="ch reveal"><div class="ch-side"><div class="ch-tabs" role="tablist" aria-orientation="vertical">' + "".join(tabs) + '</div>'
            '<div class="ch-icons" aria-label="Quick pick">' + icons + '</div></div>'
            '<div class="ch-panels">' + "".join(panels) + '</div></div></div></section>')

def statement():
    return ('<section class="statement" aria-label="Our approach"><div class="wrap">'
            '<p class="st reveal"><span>Strategy.</span> <span>Execution.</span> <span class="grad">Success.</span></p>'
            '<p class="st-sub reveal">One accountable team from the first conversation to the final handover.</p></div></section>')

def bento():
    cells = "".join(
        f'<a class="bt {cls}" href="{href}">{BG.get(href, "")}{svg(ic)}<h3>{t}</h3><p>{d}</p><span class="more">{cta} →</span></a>'
        for cls, href, ic, t, d, cta in BENTO)
    return ('<section class="sec alt" id="explore"><div class="wrap"><div class="head reveal"><p class="eyebrow">Explore</p>'
            '<h2>Everything in one place</h2></div><div class="bento">' + cells + '</div></div></section>')

def build():
    t = open(ROOT / "index.html", encoding="utf-8").read()
    a = t.index("</section>", t.index('class="marquee"')) + len("</section>")
    b = t.index("</main>")
    body = "\n\n" + challenges() + "\n\n" + statement() + "\n\n" + bento() + "\n"
    open(ROOT / "index.html", "w", encoding="utf-8").write(t[:a] + body + t[b:])
    # make sure home.js is loaded once
    t = open(ROOT / "index.html", encoding="utf-8").read()
    if "home.js" not in t:
        t = t.replace('<script src="js/hero-bg.js"></script>', '<script src="js/hero-bg.js"></script>\n<script src="js/home.js"></script>', 1)
        open(ROOT / "index.html", "w", encoding="utf-8").write(t)

if __name__ == "__main__":
    build(); print("home built")
