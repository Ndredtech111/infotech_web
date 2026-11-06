"""Thin-line SVG icons (48x48 viewBox) and a decorator that adds them to cards."""
import re
P = {
 "cloud": '<path d="M14 34a8 8 0 0 1-1-15.9A11 11 0 0 1 34 16a9 9 0 0 1 1 18z"/><path d="M20 28l4-4 4 4M24 24v10"/>',
 "data": '<ellipse cx="24" cy="12" rx="13" ry="5"/><path d="M11 12v12c0 2.8 5.8 5 13 5s13-2.2 13-5V12M11 24v12c0 2.8 5.8 5 13 5s13-2.2 13-5V24"/>',
 "code": '<path d="M17 15L7 24l10 9M31 15l10 9-10 9M27 10l-6 28"/>',
 "migrate": '<path d="M8 17h28M30 11l6 6-6 6M40 31H12M18 25l-6 6 6 6"/>',
 "devops": '<path d="M24 24c-4-6-8-9-12-9a9 9 0 0 0 0 18c4 0 8-3 12-9s8-9 12-9a9 9 0 0 1 0 18c-4 0-8-3-12-9z"/>',
 "talent": '<circle cx="24" cy="15" r="7"/><path d="M10 41c0-8 6-13 14-13s14 5 14 13"/>',
 "consult": '<circle cx="24" cy="24" r="16"/><path d="M30 18l-4 10-10 4 4-10z"/>',
 "target": '<circle cx="24" cy="24" r="16"/><circle cx="24" cy="24" r="9"/><circle cx="24" cy="24" r="2"/>',
 "path": '<path d="M8 38c0-10 10-6 14-14s-4-14 6-16M36 6l4 4-4 4"/>',
 "globe": '<circle cx="24" cy="24" r="16"/><path d="M8 24h32M24 8c-6 5-6 27 0 32M24 8c6 5 6 27 0 32"/>',
 "pin": '<path d="M24 42S10 30 10 20a14 14 0 0 1 28 0c0 10-14 22-14 22z"/><circle cx="24" cy="20" r="5"/>',
 "eye": '<path d="M4 24s8-13 20-13 20 13 20 13-8 13-20 13S4 24 4 24z"/><circle cx="24" cy="24" r="6"/>',
 "flag": '<path d="M11 42V8M11 9h24l-5 8 5 8H11"/>',
 "badge": '<circle cx="24" cy="20" r="12"/><path d="M18 20l5 5 8-9M17 31l-3 13 10-5 10 5-3-13"/>',
 "hourglass": '<path d="M12 6h24M12 42h24M14 6c0 10 10 12 10 18s-10 8-10 18M34 6c0 10-10 12-10 18s10 8 10 18"/>',
 "partner": '<circle cx="18" cy="24" r="11"/><circle cx="30" cy="24" r="11"/>',
 "wrench": '<path d="M32 8a9 9 0 0 0-8 12L8 36a4 4 0 0 0 6 6l16-16a9 9 0 0 0 12-8l-6 5-6-2-2-6z"/>',
 "userplus": '<circle cx="19" cy="15" r="7"/><path d="M5 41c0-8 6-13 14-13 3 0 6 1 8 3M36 26v14M29 33h14"/>',
 "team": '<circle cx="17" cy="16" r="6"/><circle cx="33" cy="16" r="6"/><path d="M4 40c0-7 5-12 13-12s13 5 13 12M30 29c8 0 14 4 14 11"/>',
 "clip": '<rect x="10" y="8" width="28" height="34" rx="3"/><path d="M18 8V5h12v3M17 20h14M17 27h14M17 34h8"/>',
 "bank": '<path d="M5 18L24 7l19 11zM9 40h30M12 21v15M20 21v15M28 21v15M36 21v15"/>',
 "building": '<path d="M10 42V8h20v34M30 18h8v24M4 42h40M16 15h8M16 23h8M16 31h8"/>',
 "server": '<rect x="7" y="9" width="34" height="12" rx="2"/><rect x="7" y="27" width="34" height="12" rx="2"/><path d="M13 15h2M13 33h2M33 15h2M33 33h2"/>',
 "chart": '<path d="M8 40V8M8 40h34"/><path d="M15 32l8-10 6 6 11-15"/>',
 "bars": '<path d="M8 40h32"/><rect x="11" y="24" width="6" height="16"/><rect x="21" y="14" width="6" height="26"/><rect x="31" y="8" width="6" height="32"/>',
 "pipe": '<circle cx="10" cy="24" r="4"/><circle cx="38" cy="24" r="4"/><path d="M14 24h8M26 24h8M30 20l4 4-4 4"/><rect x="20" y="18" width="8" height="12" rx="1"/>',
 "box": '<path d="M24 5l17 9v20l-17 9-17-9V14zM7 14l17 9 17-9M24 23v20"/>',
 "git": '<circle cx="14" cy="12" r="4"/><circle cx="14" cy="36" r="4"/><circle cx="34" cy="20" r="4"/><path d="M14 16v16M34 24c0 8-20 2-20 8"/>',
 "gear": '<circle cx="24" cy="24" r="6"/><path d="M24 5v6M24 37v6M5 24h6M37 24h6M10.6 10.6l4.2 4.2M33.2 33.2l4.2 4.2M10.6 37.4l4.2-4.2M33.2 14.8l4.2-4.2"/>',
 "api": '<path d="M16 14l-8 10 8 10M32 14l8 10-8 10"/><circle cx="24" cy="24" r="2"/>',
 "term": '<rect x="5" y="9" width="38" height="30" rx="3"/><path d="M12 18l6 6-6 6M23 30h10"/>',
 "layers": '<path d="M24 6l18 9-18 9-18-9zM6 24l18 9 18-9M6 33l18 9 18-9"/>',
 "cpu": '<rect x="13" y="13" width="22" height="22" rx="2"/><rect x="19" y="19" width="10" height="10"/><path d="M19 6v7M29 6v7M19 35v7M29 35v7M6 19h7M6 29h7M35 19h7M35 29h7"/>',
 "spark": '<path d="M24 6l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/><path d="M38 34l1.5 4 4 1.5-4 1.5L38 45l-1.5-4-4-1.5 4-1.5z"/>',
 "orbit": '<circle cx="24" cy="24" r="4"/><ellipse cx="24" cy="24" rx="19" ry="8" transform="rotate(-30 24 24)"/><ellipse cx="24" cy="24" rx="19" ry="8" transform="rotate(30 24 24)"/>',
 "rocket": '<path d="M24 6c8 4 12 12 10 22l-6 6H20l-6-6C12 18 16 10 24 6z"/><circle cx="24" cy="19" r="3"/><path d="M14 32l-6 8 10-3M34 32l6 8-10-3"/>',
}
BY_TITLE = {
 "Cloud Implementation": "cloud", "Data Warehousing & BI": "data", "Core Development": "code",
 "Migration & Modernisation": "migrate", "DevOps & Automation": "devops", "On-Demand Talent": "talent", "IT Consulting": "consult",
 "Mission": "target", "Promise": "path", "Reach": "globe", "Strategy → Execution → Success": "path", "Where we are": "pin",
 "Clarity": "eye", "Ownership": "flag", "Quality": "badge", "Longevity": "hourglass", "Partnership": "partner", "Pragmatism": "wrench",
 "Staff Augmentation": "userplus", "Dedicated Team": "team", "Fixed-Scope Project": "clip",
 "Financial services": "bank", "Enterprise IT": "building", "Growing businesses": "rocket",
}
def svg(name): return f'<svg class="li" viewBox="0 0 48 48" aria-hidden="true">{P[name]}</svg>'
def _norm(t): return t.replace("‑", "-").replace("&amp;", "&")

_CARD = re.compile(r'(<(?:div|a|article) class="(?:card[^"]*|face front)"[^>]*>)(<div class="ic">[^<]*</div>)?<h3>([^<]+)</h3>')
def decorate(doc):
    def f(m):
        name = BY_TITLE.get(_norm(m.group(3)))
        if not name: return m.group(0)
        s = svg(name)
        ic = f'<div class="ic">{s}</div>' if m.group(2) else s
        return f'{m.group(1)}{ic}<h3>{m.group(3)}</h3>'
    return _CARD.sub(f, doc)
