#!/usr/bin/env python3
"""
Builds the static Maple Dental Vancouver site.

Shared pieces (head, header, footer, CTA band, icons) live here once; each page
is written to <root>/<slug>/index.html. Run from anywhere:

    python3 src/build.py

Edit the CONFIG block below to swap in real URLs once the client supplies them.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- CONFIG
SITE_URL = "https://mapledental.info"
PHONE_DISPLAY = "(604) 261-4607"
PHONE_TEL = "tel:+16042614607"
EMAIL = "welcome@mapledental.info"
# [ONLINE BOOKING URL] — replace with the real booking link when ready.
BOOKING_URL = PHONE_TEL
# [CORRECT GOOGLE REVIEWS URL] — replace with the clinic's Google Business Profile reviews link.
# Interim: a correctly spelled Google Maps search for the clinic.
REVIEWS_URL = "https://www.google.com/maps/search/?api=1&query=Maple+Dental+Vancouver+2025+W+42nd+Ave+Vancouver"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=2025+W+42nd+Ave+Unit+230+Vancouver+BC+V6M+2B5"
MAP_EMBED = "https://www.google.com/maps?q=Maple+Dental+Vancouver,+2025+W+42nd+Ave+%23230,+Vancouver,+BC+V6M+2B5&output=embed"
# [FORM ENDPOINT] — set to a form handler URL (e.g. Formspree, Netlify Forms). "#" keeps the form inactive.
FORM_ACTION = "#"
CDCP_URL = "https://www.canada.ca/en/services/benefits/dental/dental-care-plan.html"

ADDRESS_HTML = "2025 W 42nd Ave, Unit 230 (2nd floor)<br>Vancouver, BC V6M 2B5"

# ---------------------------------------------------------------- ICONS (stroke, 24px grid)
_I = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M9 12h6M9 16h4"/>',
    "tools": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor"/>',
    "tooth": '<path d="M7.5 3C5 3 3 5 3 7.7c0 2.2.8 3.6 1.4 5.4.7 2.1.8 7.9 2.6 7.9 1.6 0 1.7-3.8 2.4-5.3.4-.8.9-1.2 1.6-1.2h2c.7 0 1.2.4 1.6 1.2.7 1.5.8 5.3 2.4 5.3 1.8 0 1.9-5.8 2.6-7.9.6-1.8 1.4-3.2 1.4-5.4C21 5 19 3 16.5 3c-1.9 0-2.8 1-4.5 1S9.4 3 7.5 3z"/>',
    "implant": '<path d="M8 2.5h8c1.4 0 2.2 1.2 1.8 2.5l-.9 3H7.1l-.9-3C5.8 3.7 6.6 2.5 8 2.5z"/><path d="M8 11h8M8.5 14h7M9 17h6M10 20h4M9.5 8l-.5 3M14.5 8l.5 3M9 11l1 9M15 11l-1 9"/>',
    "implants": '<path d="M3 3h6l-.6 3H3.6zM15 3h6l-.6 3h-4.8z"/><path d="M4 9h4M4.5 12h3M5 15h2M16 9h4M16.5 12h3M17 15h2M4 6l.5 11h2L8 6M16 6l.5 11h2L20 6"/>',
    "arch": '<path d="M4 20c0-8.8 3.6-15 8-15s8 6.2 8 15"/><path d="M4.6 15h2.6M5.7 10.6l2.3 1.2M8.5 7.3l1.6 2M15.5 7.3l-1.6 2M18.3 10.6 16 11.8M19.4 15h-2.6"/><path d="M8 20v2M12 20v2M16 20v2" />',
    "denture": '<path d="M3 9c0-2 2-4 9-4s9 2 9 4v2c0 1-1 2-2 2H5c-1 0-2-1-2-2z"/><path d="M7 13v2M12 13v2M17 13v2M5 15h14l-1 3H6z"/><path d="M8 18v3M16 18v3"/>',
    "general": '<path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/><circle cx="12" cy="12" r="3"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


def ph(text):
    """Inline client-content placeholder."""
    return f'<span class="ph">[{text}]</span>'


def ph_block(text):
    return f'<p class="ph-block">[{text}]</p>'


def ph_img(text, extra=""):
    return f'<div class="ph-img {extra}" role="img" aria-label="Placeholder: {text}">{icon("image")}<span>[{text}]</span></div>'


def eyebrow(text):
    return f'<p class="eyebrow">{text}</p>'


# ---------------------------------------------------------------- NAV
NAV = [
    ("home", "Home", "/"),
    ("about", "About", "/about/"),
    ("services", "Services", "/services/"),
    ("new-patients", "New Patients", "/new-patients/"),
    ("contact", "Contact", "/contact/"),
]
SERVICES = [
    ("single-tooth-implants", "Single-Tooth Implants"),
    ("multiple-implants", "Multiple Implants"),
    ("all-on-x", "All-on-X Full-Arch Treatment"),
    ("implant-supported-dentures", "Implant-Supported Dentures"),
]

# ---------------------------------------------------------------- SCHEMA
SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Dentist",
    "@id": SITE_URL + "/#dentist",
    "name": "Maple Dental Vancouver",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/assets/img/maple-dental-logo.png",
    "image": SITE_URL + "/assets/img/dr-stephen-li.jpg",
    "telephone": "+1-604-261-4607",
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "2025 W 42nd Ave, Unit 230",
        "addressLocality": "Vancouver",
        "addressRegion": "BC",
        "postalCode": "V6M 2B5",
        "addressCountry": "CA",
    },
    "areaServed": "Kerrisdale, Vancouver, BC",
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00",
        "closes": "17:00",
    }],
    "knowsLanguage": ["en", "fr", "zh", "ar"],
    "availableService": [{"@type": "MedicalProcedure", "name": n} for _, n in SERVICES],
    "employee": {
        "@type": "Person",
        "name": "Dr. Stephen Li",
        "jobTitle": "Dentist",
        "honorificSuffix": "DMD, AFAAID, FICOI",
    },
}


# ---------------------------------------------------------------- LAYOUT
def head(title, desc, path, schema=False):
    canonical = SITE_URL + path
    s = f'\n  <script type="application/ld+json">{json.dumps(SCHEMA, ensure_ascii=False)}</script>' if schema else ""
    return f"""<!doctype html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Maple Dental Vancouver">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/assets/img/dr-stephen-li.jpg">
  <meta property="og:locale" content="en_CA">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0f3b44">
  <link rel="icon" type="image/png" href="/assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script>document.documentElement.classList.add('js')</script>{s}
</head>"""


def header(active):
    cur = ' aria-current="page"'
    links = "\n".join(
        f'          <li><a class="nav__link" href="{href}"{cur if key == active else ""}>{label}</a></li>'
        for key, label, href in NAV)
    return f"""<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <div class="announce" data-announce>
    <div class="container announce__inner">
      <ul class="announce__list" aria-label="Clinic highlights">
        <li>Same-day appointments when you call 9am to 1pm</li>
        <li>Free phone consult with our dentist</li>
        <li>CDCP provider</li>
      </ul>
      <button class="announce__close" type="button" data-announce-close aria-label="Dismiss announcement">{icon("x")}</button>
    </div>
  </div>

  <header class="site-header">
    <div class="container header__inner">
      <a class="brand" href="/" aria-label="Maple Dental Vancouver, home">
        <img src="/assets/img/maple-dental-logo.png" width="720" height="223" alt="Maple Dental Vancouver logo">
      </a>
      <nav class="nav" id="site-nav" aria-label="Main">
        <ul class="nav__list">
{links}
        </ul>
        <div class="nav__mobile-cta">
          <a class="btn btn--primary" href="{BOOKING_URL}">{icon("calendar")}Book a Visit</a>
          <a class="btn btn--outline" href="{PHONE_TEL}">{icon("phone")}Call {PHONE_DISPLAY}</a>
        </div>
      </nav>
      <div class="header__actions">
        <a class="header__phone" href="{PHONE_TEL}" aria-label="Call {PHONE_DISPLAY}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a>
        <!-- [ONLINE BOOKING URL]: set BOOKING_URL in src/build.py -->
        <a class="btn btn--primary btn--sm" href="{BOOKING_URL}">Book a Visit</a>
      </div>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        {icon("menu", "icon-open")}{icon("x", "icon-close")}
      </button>
    </div>
  </header>

  <main id="main">"""


def cta_band():
    return f"""
    <section class="cta-band on-dark" aria-labelledby="cta-title">
      <div class="container cta-band__inner reveal">
        <div>
          <h2 id="cta-title">Ready to book your visit?</h2>
          <p>Call between 9am and 1pm for a same-day appointment.</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--primary" href="{BOOKING_URL}">{icon("calendar")}Book a Visit</a>
          <a class="btn btn--outline-light" href="{PHONE_TEL}">{icon("phone")}Call {PHONE_DISPLAY}</a>
        </div>
      </div>
    </section>"""


def footer():
    quick = "\n".join(f'            <li><a href="{h}">{l}</a></li>' for _, l, h in NAV)
    svc = "\n".join(f'            <li><a href="/services/#{a}">{n}</a></li>' for a, n in SERVICES)
    return f"""
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="footer__logo" href="/" aria-label="Maple Dental Vancouver, home">
            <img src="/assets/img/maple-dental-logo.png" width="720" height="223" alt="Maple Dental Vancouver logo" loading="lazy">
          </a>
          <p>Personal dental and implant care in Kerrisdale, Vancouver, with the same dentist every visit.</p>
          <p class="footer__social">{ph("SOCIAL LINKS")}</p>
        </div>
        <nav aria-label="Footer quick links">
          <h2>Quick links</h2>
          <ul>
{quick}
          </ul>
        </nav>
        <nav aria-label="Footer services">
          <h2>Services</h2>
          <ul>
{svc}
          </ul>
        </nav>
        <div>
          <h2>Contact</h2>
          <ul class="footer__contact">
            <li>{icon("pin")}<address><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS_HTML}</a></address></li>
            <li>{icon("phone")}<a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
            <li>{icon("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>{icon("clock")}<span>Tuesday to Friday, 9am to 5pm</span></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <p>&copy; <span data-year>2026</span> Maple Dental Vancouver. All rights reserved.</p>
        <ul>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <div class="mobile-bar" aria-label="Quick actions">
    <a class="btn btn--outline" href="{PHONE_TEL}">{icon("phone")}Call</a>
    <a class="btn btn--primary" href="{BOOKING_URL}">{icon("calendar")}Book</a>
  </div>

  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def page_hero(eb, h1, intro):
    return f"""
    <section class="page-hero">
      <div class="container">
        <div class="page-hero__inner">
          {eyebrow(eb)}
          <h1>{h1}</h1>
          <p>{intro}</p>
        </div>
      </div>
    </section>"""


def hours_table():
    return """<table class="hours-table">
                  <caption class="sr-only">Clinic hours</caption>
                  <tbody>
                    <tr><th scope="row">Tuesday to Friday</th><td>9am to 5pm</td></tr>
                    <tr><th scope="row" class="closed">Saturday to Monday</th><td class="closed">Closed</td></tr>
                  </tbody>
                </table>"""


def dr_li_picture(eager=False, cls="portrait"):
    lazy = "" if eager else ' loading="lazy" decoding="async"'
    return f"""<div class="{cls}">
            <picture>
              <source srcset="/assets/img/dr-stephen-li.webp" type="image/webp">
              <img src="/assets/img/dr-stephen-li.jpg" width="1200" height="1630"{lazy}
                   alt="Dr. Stephen Li, dentist at Maple Dental Vancouver, smiling in a white clinic coat in a treatment room">
            </picture>
          </div>"""


def map_iframe(title="Map showing Maple Dental Vancouver at 2025 W 42nd Ave, Vancouver"):
    return f'<div class="map-frame"><iframe src="{MAP_EMBED}" title="{title}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>'


# ================================================================ HOME
def home():
    trust = [
        ("user", "Same dentist every visit"),
        ("award", "500+ hours of implant training"),
        ("globe", "4 languages spoken"),
        ("shield", "Canadian Dental Care Plan provider"),
    ]
    trust_html = "\n".join(f'          <li class="trust__item reveal">{icon(i)}<span>{t}</span></li>' for i, t in trust)

    svc_cards = [
        ("tooth", "Single-Tooth Implants", "single-tooth-implants",
         "Replace one missing tooth with an implant and crown that look and function like a natural tooth."),
        ("implants", "Multiple Implants", "multiple-implants",
         "Restore several missing teeth with implants planned around your bite and the teeth you still have."),
        ("arch", "All-on-X Full-Arch Treatment", "all-on-x",
         "A complete set of replacement teeth supported by strategically placed implants."),
        ("denture", "Implant-Supported Dentures", "implant-supported-dentures",
         "A more secure alternative to traditional removable dentures."),
    ]
    cards = "\n".join(f"""          <article class="card reveal">
            <span class="icon-tile">{icon(i)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <a class="link-arrow" href="/services/#{a}">Learn more<span class="sr-only"> about {t}</span>{icon("arrow")}</a>
          </article>""" for i, t, a, d in svc_cards)

    why = [
        ("user", "The same dentist, every time",
         "You see Dr. Stephen Li at every visit. Continuity of care means he knows your history, your goals and how you like to be treated."),
        ("chat", "A direct line to your dentist",
         f"Ask for Dr. Li whenever you need to talk. A phone conversation is often all it takes to answer a question or ease a worry, and you can reach us after hours, on weekends and on holidays. {ph('CONFIRM after-hours process')}"),
        ("globe", "We speak your language",
         "Our team speaks English, French, Chinese and Arabic, so you can discuss your care in the language you are most comfortable with."),
        ("check-circle", "Treatment only when it helps you",
         "Dentistry offers many options. We explain them clearly and recommend only what benefits your oral and overall health."),
    ]
    why_html = "\n".join(f"""          <div class="feature reveal">
            <h3>{icon(i)}{t}</h3>
            <p>{d}</p>
          </div>""" for i, t, d in why)

    steps = [
        ("Call or book online", f"Call {PHONE_DISPLAY} or book online. Call between 9am and 1pm for a same-day appointment."),
        ("Free phone consult", "Talk through your concerns with Dr. Li by phone, at no charge, before you come in."),
        ("Exam and personal plan", "We get to know you, find what you need and build a plan around your goals."),
        ("Treatment and follow-up", "Dr. Li provides your treatment and stays with you through follow-up and future visits."),
    ]
    steps_html = "\n".join(f"""          <article class="card step-card reveal">
            <span class="step-num">{n:02d}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>""" for n, (t, d) in enumerate(steps, 1))

    review = f"""          <article class="card review-card reveal">
            <div class="stars" aria-hidden="true">{icon("star")*5}</div>
            <blockquote><p>{ph("PASTE REAL GOOGLE REVIEW TEXT")}</p></blockquote>
            <footer>{ph("REVIEWER NAME")} &middot; Google review</footer>
          </article>"""

    return head(
        "Maple Dental Vancouver | Kerrisdale Dentist & Dental Implants",
        "Kerrisdale dentist Dr. Stephen Li offers dental implant care with the same dentist every visit. We speak English, French, Chinese and Arabic and are a CDCP provider.",
        "/", schema=True) + header("home") + f"""

    <!-- 1. Hero -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="container hero__grid">
        <div class="reveal">
          {eyebrow("Kerrisdale, Vancouver &middot; Dental &amp; implant care")}
          <h1 id="hero-title">Personal dental care with the same dentist, every visit</h1>
          <p class="hero__sub">Implant-trained dentist Dr. Stephen Li and a team that speaks English, French, Chinese and Arabic.</p>
          <div class="btn-row">
            <a class="btn btn--primary" href="{BOOKING_URL}">{icon("calendar")}Book a Visit</a>
            <a class="btn btn--outline" href="{PHONE_TEL}">{icon("phone")}Call {PHONE_DISPLAY}</a>
          </div>
        </div>
        <div class="hero__media reveal">
          <img class="hero__img" src="/assets/img/clinic-reception.jpg" width="399" height="501" fetchpriority="high"
               alt="Bright reception area with a curved white front desk, warm ring pendant lights and an illuminated tooth logo on the wall">
          <!-- Hero photo is only 399x501px; replace with a 1000px+ wide version for sharp display. -->

          <div class="float-card">
            <div class="float-card__item"><span class="float-card__icon">{icon("shield")}</span>CDCP Provider</div>
            <div class="float-card__item"><span class="float-card__icon">{icon("phone")}</span>Free phone consult</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Trust strip -->
    <section class="trust" aria-label="Why patients trust us">
      <div class="container">
        <ul class="trust__list" data-stagger>
{trust_html}
        </ul>
      </div>
    </section>

    <!-- 3. Quick info -->
    <section class="section section--tight section--cream" aria-labelledby="info-title">
      <div class="container">
        <h2 id="info-title" class="sr-only">Clinic information</h2>
        <div class="info-grid reveal">
          <div class="info-item">
            <span class="icon-tile">{icon("pin")}</span>
            <div><h3>Location</h3><address><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS_HTML}<span class="sr-only"> (opens Google Maps)</span></a></address></div>
          </div>
          <div class="info-item">
            <span class="icon-tile">{icon("clock")}</span>
            <div><h3>Hours</h3><p>Tuesday to Friday<br>9am to 5pm</p></div>
          </div>
          <div class="info-item">
            <span class="icon-tile">{icon("phone")}</span>
            <div><h3>Phone</h3><p><a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></p></div>
          </div>
          <div class="info-item">
            <span class="icon-tile">{icon("mail")}</span>
            <div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Meet your dentist -->
    <section class="section" aria-labelledby="dentist-title">
      <div class="container split split--5-7">
        <div class="reveal">
          {dr_li_picture()}
        </div>
        <div class="reveal">
          {eyebrow("Meet your dentist")}
          <h2 id="dentist-title">Dr. Stephen Li, DMD, AFAAID, FICOI</h2>
          <p>Dr. Li has completed more than 500 hours of continuing education in implant dentistry and holds fellowships with the American Academy of Implant Dentistry and the International Congress of Oral Implantologists. {ph("EDUCATION AND YEARS IN PRACTICE")}</p>
          <blockquote class="pull-quote">
            <p>&ldquo;We value individualized care, with my participation every step of the way. From your cleanings to your treatments, your wishes and concerns guide our approach.&rdquo;</p>
            <cite>Dr. Stephen Li</cite>
          </blockquote>
          <a class="link-arrow" href="/about/#dr-li">More about Dr. Li{icon("arrow")}</a>
        </div>
      </div>
    </section>

    <!-- 5. Stats -->
    <section class="section section--dark section--tight on-dark" aria-label="Maple Dental at a glance" style="padding:64px 0">
      <div class="container">
        <dl class="stats" data-stagger>
          <div class="stat reveal"><dt>Hours of implant education</dt><dd>500+</dd></div>
          <div class="stat reveal"><dt>Implant fellowships</dt><dd>2</dd></div>
          <div class="stat reveal"><dt>Languages spoken</dt><dd>4</dd></div>
          <div class="stat reveal"><dt>Dentist, every visit</dt><dd>1</dd></div>
        </dl>
      </div>
    </section>

    <!-- 6. Services -->
    <section class="section section--cream" aria-labelledby="services-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Our services")}
          <h2 id="services-title">Implant dentistry, planned around you</h2>
          <p>From a single missing tooth to a full arch, each treatment is planned around your oral health, how you eat and speak, and how you want your smile to look.</p>
        </div>
        <div class="cards cards--4" data-stagger>
{cards}
        </div>
        <!-- Fifth card "General & Preventive Care": add ONLY once the client confirms [CONFIRM: cleanings, exams, fillings?] -->
        <div class="section-foot"><a class="btn btn--outline" href="/services/">View all services{icon("arrow")}</a></div>
      </div>
    </section>

    <!-- 7. Why Maple Dental -->
    <section class="section" aria-labelledby="why-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Why Maple Dental")}
          <h2 id="why-title">Dental care the way we would want to be treated</h2>
        </div>
        <div class="feature-grid" data-stagger>
{why_html}
        </div>
      </div>
    </section>

    <!-- 8. How it works -->
    <section class="section section--cream" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Your first visit")}
          <h2 id="steps-title">Getting started is simple</h2>
        </div>
        <div class="cards cards--4" data-stagger>
{steps_html}
        </div>
      </div>
    </section>

    <!-- 9. Reviews -->
    <section class="section" aria-labelledby="reviews-title">
      <div class="container">
        <div class="section-head section-head--center reveal">
          {eyebrow("Patient reviews")}
          <h2 id="reviews-title">What our patients say</h2>
          <p>{ph("PASTE REAL REVIEWS or Google reviews embed. Use only genuine Google reviews supplied by the clinic.")}</p>
        </div>
        <div class="cards cards--3" data-stagger>
{review}
{review}
{review}
        </div>
        <!-- [CORRECT GOOGLE REVIEWS URL]: set REVIEWS_URL in src/build.py -->
        <div class="section-foot"><a class="btn btn--outline" href="{REVIEWS_URL}" target="_blank" rel="noopener">Read all reviews on Google<span class="sr-only"> (opens in a new tab)</span>{icon("arrow")}</a></div>
      </div>
    </section>

    <!-- 10. Coverage -->
    <section class="section section--tint" aria-labelledby="coverage-title">
      <div class="container coverage">
        <div class="reveal">
          {eyebrow("Coverage")}
          <h2 id="coverage-title">We accept the Canadian Dental Care Plan</h2>
          <p class="lead">Maple Dental Vancouver is a Canadian Dental Care Plan (CDCP) provider. If you are enrolled in the plan, let us know when you book.</p>
          <p><a href="{CDCP_URL}" target="_blank" rel="noopener">Learn about the CDCP on Canada.ca<span class="sr-only"> (opens in a new tab)</span></a></p>
        </div>
        <div class="stack reveal">
          <div class="badge-card">
            <span class="icon-tile">{icon("shield")}</span>
            <div><h3>Insurance and direct billing</h3><p>{ph("DIRECT BILLING / INSURANCE DETAILS")}</p></div>
          </div>
          <div class="badge-card">
            <span class="icon-tile">{icon("card")}</span>
            <div><h3>Payment options</h3><p>{ph("PAYMENT OR FINANCING OPTIONS")}</p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 11. Location -->
    <section class="section" aria-labelledby="location-title">
      <div class="container split split--top">
        <div class="reveal">
          {eyebrow("Visit us")}
          <h2 id="location-title">Find us in Kerrisdale</h2>
          <div class="detail-list">
            <div class="detail">{icon("pin")}<div><h3>Address</h3><address><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS_HTML}<span class="sr-only"> (opens Google Maps)</span></a></address></div></div>
            <div class="detail">{icon("clock")}<div><h3>Hours</h3>{hours_table()}</div></div>
            <div class="detail">{icon("map")}<div><h3>Getting here</h3><p>{ph("PARKING / TRANSIT / ELEVATOR ACCESS")}</p></div></div>
          </div>
          <a class="btn btn--outline" href="{MAPS_URL}" target="_blank" rel="noopener">Get directions<span class="sr-only"> (opens Google Maps)</span>{icon("arrow")}</a>
        </div>
        <div class="reveal">
          {map_iframe()}
        </div>
      </div>
    </section>
""" + cta_band() + footer()


# ================================================================ ABOUT
def about():
    approach = [
        ("users", "Get to know you", "We start by learning about you, your history and what matters to you."),
        ("search", "Find what you need", "Together, we identify the areas of your oral health that need attention."),
        ("clipboard", "Build a plan together", "We agree on a plan toward your goals and adjust it as your needs and dental care evolve."),
        ("tools", "Give you the tools", "We share the knowledge and habits that help you prevent problems at home."),
        ("smile", "Take the stress out of visits", "Clear explanations and a familiar face make every appointment easier."),
        ("heart", "Care you can count on", "A consistent team you can rely on for the long term."),
    ]
    approach_html = "\n".join(f"""          <article class="card reveal">
            <span class="icon-tile">{icon(i)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>""" for i, t, d in approach)
    team = "\n".join(f"""          <article class="team-card reveal">
            {ph_img("TEAM PHOTO")}
            <h3>{ph("NAME")}</h3>
            <p>{ph("ROLE AND LANGUAGES SPOKEN")}</p>
          </article>""" for _ in range(3))

    return head(
        "About Maple Dental Vancouver | Dr. Stephen Li, Kerrisdale Dentist",
        "Meet Dr. Stephen Li, DMD, AFAAID, FICOI, and the Maple Dental Vancouver team. Personal, coaching-style dental care in Kerrisdale, in English, French, Chinese and Arabic.",
        "/about/") + header("about") + page_hero(
        "About us", "Your dental coach",
        "We learn your goals, help you work toward them and support you through any setbacks along the way, because we like seeing our patients thrive.") + f"""

    <section class="section" aria-labelledby="approach-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Our approach")}
          <h2 id="approach-title">How we work with you</h2>
          <p>We see dental care as a partnership. Here is what that looks like in practice.</p>
        </div>
        <div class="cards cards--3" data-stagger>
{approach_html}
        </div>
      </div>
    </section>

    <section class="section section--cream" id="dr-li" aria-labelledby="drli-title">
      <div class="container split split--5-7">
        <div class="reveal">
          {dr_li_picture()}
        </div>
        <div class="reveal">
          {eyebrow("Meet your dentist")}
          <h2 id="drli-title">Dr. Stephen Li</h2>
          <p class="credentials-line">DMD, AFAAID, FICOI</p>
          <p>Dr. Li is the dentist you will see at every visit to Maple Dental Vancouver. He has a particular focus on implant dentistry, with more than 500 hours of continuing education dedicated to the field.</p>
          <ul class="check-list">
            <li>{icon("check")}<span><strong>AFAAID</strong>: Associate Fellow of the American Academy of Implant Dentistry</span></li>
            <li>{icon("check")}<span><strong>FICOI</strong>: Fellow of the International Congress of Oral Implantologists</span></li>
            <li>{icon("check")}<span>500+ hours of continuing education in implant dentistry</span></li>
          </ul>
          <p style="margin-top:20px">{ph("EDUCATION / BACKGROUND")}</p>
          <blockquote class="pull-quote">
            <p>&ldquo;We value individualized care, with my participation every step of the way. From your cleanings to your treatments, your wishes and concerns guide our approach.&rdquo;</p>
            <cite>Dr. Stephen Li</cite>
          </blockquote>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="team-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Our team")}
          <h2 id="team-title">The people you will meet</h2>
          <p>{ph("TEAM PHOTOS AND NAMES")}</p>
        </div>
        <div class="cards cards--3" data-stagger>
{team}
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="gallery-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("The clinic")}
          <h2 id="gallery-title">Inside Maple Dental</h2>
          <p>{ph("CLINIC PHOTO GALLERY")}</p>
        </div>
        <div class="gallery reveal">
          {ph_img("RECEPTION PHOTO")}
          {ph_img("TREATMENT ROOM PHOTO")}
          {ph_img("EQUIPMENT PHOTO")}
        </div>
      </div>
    </section>
""" + cta_band() + footer()


# ================================================================ SERVICES
def services():
    blocks = [
        ("single-tooth-implants", "Single-Tooth Implants",
         "A single implant replaces one missing tooth, root and all. A post is placed in the jawbone and topped with a crown made to match your surrounding teeth, without reshaping the healthy teeth on either side.",
         "Patients missing one tooth, whether from injury, decay or an old restoration that has failed."),
        ("multiple-implants", "Multiple Implants",
         "When several teeth are missing, implants can support individual crowns or a bridge. Each case is planned around your bite, bone and the natural teeth you still have.",
         "Patients missing two or more teeth in one or more areas of the mouth."),
        ("all-on-x", "All-on-X Full-Arch Treatment",
         "A full-arch implant solution that uses strategically placed dental implants to support a complete set of replacement teeth, offering stability, function and a natural-looking result.",
         "Patients missing most or all of the teeth in an arch, or whose remaining teeth cannot be saved."),
        ("implant-supported-dentures", "Implant-Supported Dentures",
         "A more secure alternative to traditional removable dentures. The denture attaches to implants, so it stays in place when you eat and speak.",
         "Denture wearers who want more stability, and patients considering dentures for the first time."),
    ]
    blocks_html = "\n".join(f"""        <article class="service-block" id="{a}" aria-labelledby="{a}-title">
          <div class="service-block__media reveal">{ph_img(f"{t.upper()} PHOTO OR ILLUSTRATION")}</div>
          <div class="reveal">
            {eyebrow(f"Service {i:02d}")}
            <h3 id="{a}-title" style="font-size:clamp(1.6rem,2.6vw,2.1rem)">{t}</h3>
            <p>{d}</p>
            <div class="who"><h4>Who it&rsquo;s for</h4><p>{w}</p></div>
            <a class="link-arrow" href="{BOOKING_URL}">Book a consult<span class="sr-only"> for {t}</span>{icon("arrow")}</a>
          </div>
        </article>""" for i, (a, t, d, w) in enumerate(blocks, 1))

    faqs = "\n".join(f"""          <div class="acc-item">
            <h3><button class="acc-trigger" type="button" aria-expanded="false" aria-controls="faq-{n}" id="faq-{n}-btn">
              <span>{ph(f"IMPLANT FAQ QUESTION {n}")}</span><span class="acc-icon">{icon("plus")}</span>
            </button></h3>
            <div class="acc-panel" id="faq-{n}" role="region" aria-labelledby="faq-{n}-btn">
              <div><div class="acc-panel__body"><p>{ph(f"ANSWER {n} FROM CLIENT")}</p></div></div>
            </div>
          </div>""" for n in range(1, 6))

    return head(
        "Dental Implants in Kerrisdale, Vancouver | Maple Dental Vancouver",
        "Single-tooth implants, multiple implants, All-on-X and implant-supported dentures with Dr. Stephen Li, AFAAID, FICOI, who has 500+ hours of implant education.",
        "/services/") + header("services") + page_hero(
        "Services", "Dental implant treatment",
        "From replacing a single missing tooth to restoring an entire arch, we plan each implant treatment around your oral health, your daily needs and how you want your smile to look.") + f"""

    <section class="section" aria-labelledby="cred-title">
      <div class="container cred-block">
        <div class="reveal">
          {eyebrow("Advanced implant education")}
          <p class="cred-big">500+</p>
          <h2 id="cred-title" style="font-size:clamp(1.4rem,2.2vw,1.75rem)">hours of continuing education dedicated to implant dentistry</h2>
          <p>Dr. Stephen Li&rsquo;s training in implant dentistry goes well beyond his general dental education.</p>
        </div>
        <div class="reveal">
          <div class="stack">
            <div class="card cred-card">
              <span class="icon-tile">{icon("award")}</span>
              <div><h3><abbr title="Associate Fellow of the American Academy of Implant Dentistry">AFAAID</abbr></h3><p>Associate Fellow of the American Academy of Implant Dentistry</p></div>
            </div>
            <div class="card cred-card">
              <span class="icon-tile">{icon("award")}</span>
              <div><h3><abbr title="Fellow of the International Congress of Oral Implantologists">FICOI</abbr></h3><p>Fellow of the International Congress of Oral Implantologists</p></div>
            </div>
          </div>
          <div class="cred-logos">
            <span class="cred-logos__label">Affiliations</span>
            <img src="/assets/img/icoi-logo.webp" width="626" height="184" alt="International Congress of Oral Implantologists (ICOI) logo" loading="lazy">
            {ph("AAID LOGO")}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--cream" aria-labelledby="treatments-title">
      <div class="container">
        <div class="section-head reveal">
          {eyebrow("Treatments")}
          <h2 id="treatments-title">Implant options we offer</h2>
        </div>
{blocks_html}
      </div>
    </section>

    <section class="section section--tight" aria-label="Additional services">
      <div class="container">
        <p class="ph-block reveal">[ADDITIONAL SERVICES: list any other services offered (e.g. general and preventive care) once confirmed by the clinic, or remove this block.]</p>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head section-head--center reveal">
          {eyebrow("FAQ")}
          <h2 id="faq-title">Implant questions, answered</h2>
          <p>{ph("IMPLANT FAQS FROM CLIENT")}</p>
        </div>
        <div class="accordion reveal">
{faqs}
        </div>
      </div>
    </section>
""" + cta_band() + footer()


# ================================================================ NEW PATIENTS
def new_patients():
    toc = [("first-visit", "Your first visit"), ("what-to-bring", "What to bring"),
           ("coverage", "Coverage and the CDCP"), ("cancellations", "Cancellation policy")]
    toc_html = "\n".join(f'              <li><a href="#{a}">{t}</a></li>' for a, t in toc)
    return head(
        "New Patients | Maple Dental Vancouver, Kerrisdale",
        "New to Maple Dental Vancouver? Learn what to expect at your first visit, what to bring, and how the Canadian Dental Care Plan (CDCP) works at our Kerrisdale clinic.",
        "/new-patients/") + header("new-patients") + page_hero(
        "New patients", "Welcome to Maple Dental",
        "Everything you need to know before your first appointment. If you have a question that is not answered here, call us and ask for Dr. Li.") + f"""

    <section class="section">
      <div class="container content-grid">
        <aside class="toc" aria-labelledby="toc-title">
          <h2 id="toc-title">On this page</h2>
          <ol>
{toc_html}
          </ol>
        </aside>
        <div>
          <section class="content-section reveal" id="first-visit" aria-labelledby="first-visit-title">
            <h2 id="first-visit-title"><span class="icon-tile">{icon("calendar")}</span>What to expect at your first visit</h2>
            <ol class="numbered">
              <li><div><strong>Book your appointment.</strong> Call {PHONE_DISPLAY}. If you call between 9am and 1pm, we can often see you the same day.</div></li>
              <li><div><strong>Talk to Dr. Li.</strong> A free phone consult lets you share your concerns before you come in.</div></li>
              <li><div><strong>Exam and personal plan.</strong> We get to know you, assess your oral health and agree on a plan together.</div></li>
              <li><div><strong>Treatment and follow-up.</strong> Dr. Li provides your care and remains your dentist for every future visit.</div></li>
            </ol>
            {ph_block("FIRST VISIT DETAILS FROM CLIENT: length of appointment, X-rays, forms to complete, arrival time")}
          </section>

          <section class="content-section reveal" id="what-to-bring" aria-labelledby="bring-title">
            <h2 id="bring-title"><span class="icon-tile">{icon("clipboard")}</span>What to bring</h2>
            {ph_block("WHAT TO BRING FROM CLIENT: e.g. photo ID, insurance or CDCP details, list of medications, previous dental records or X-rays")}
          </section>

          <section class="content-section reveal" id="coverage" aria-labelledby="np-coverage-title">
            <h2 id="np-coverage-title"><span class="icon-tile">{icon("shield")}</span>Coverage and the CDCP</h2>
            <p>Maple Dental Vancouver is a Canadian Dental Care Plan (CDCP) provider. If you are enrolled, let us know when you book. You can check eligibility and enrolment on <a href="{CDCP_URL}" target="_blank" rel="noopener">Canada.ca<span class="sr-only"> (opens in a new tab)</span></a>.</p>
            {ph_block("DIRECT BILLING / INSURANCE DETAILS")}
            {ph_block("PAYMENT OR FINANCING OPTIONS")}
          </section>

          <section class="content-section reveal" id="cancellations" aria-labelledby="cancel-title">
            <h2 id="cancel-title"><span class="icon-tile">{icon("clock")}</span>Cancellation policy</h2>
            {ph_block("CANCELLATION POLICY FROM CLIENT: notice required and any fees")}
          </section>
        </div>
      </div>
    </section>
""" + cta_band() + footer()


# ================================================================ CONTACT
def contact():
    def field(id_, label, type_="text", auto="", req=True, full=False, extra=""):
        r = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="hint">(optional)</span>'
        req_attr = " required" if req else ""
        err = f'<p class="error" id="{id_}-error" hidden>Please enter your {label.lower()}.</p>' if req else ""
        desc = f' aria-describedby="{id_}-error"' if req else ""
        return f"""              <div class="field{' field--full' if full else ''}">
                <label for="{id_}">{label}{r}</label>
                <input id="{id_}" name="{id_}" type="{type_}" autocomplete="{auto}"{req_attr}{desc}{extra}>
                {err}
              </div>"""

    return head(
        "Contact Maple Dental Vancouver | Kerrisdale Dentist, (604) 261-4607",
        "Contact Maple Dental Vancouver at 2025 W 42nd Ave, Unit 230, Vancouver. Call (604) 261-4607 or email welcome@mapledental.info. Open Tuesday to Friday, 9am to 5pm.",
        "/contact/") + header("contact") + page_hero(
        "Contact", "Get in touch",
        "Call us for the fastest response. For a same-day appointment, call between 9am and 1pm.") + f"""

    <section class="section">
      <div class="container contact-grid">
        <div class="reveal">
          <h2 style="font-size:1.75rem">Clinic details</h2>
          <div class="detail-list">
            <div class="detail">{icon("phone")}<div><h3>Phone</h3><p><a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></p></div></div>
            <div class="detail">{icon("mail")}<div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
            <div class="detail">{icon("pin")}<div><h3>Address</h3><address><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS_HTML}<span class="sr-only"> (opens Google Maps)</span></a></address></div></div>
            <div class="detail">{icon("clock")}<div><h3>Hours</h3>{hours_table()}</div></div>
            <div class="detail">{icon("globe")}<div><h3>Languages</h3><p>English, French, Chinese and Arabic</p></div></div>
          </div>
          {map_iframe()}
        </div>

        <div class="form-card reveal">
          <h2>Send us a message</h2>
          <p style="color:var(--muted)">We will reply by email or phone. Please do not include detailed medical information in this form.</p>
          <!-- [FORM ENDPOINT]: set FORM_ACTION in src/build.py -->
          <form action="{FORM_ACTION}" method="post" novalidate data-contact-form>
            <div class="form-grid">
{field("first-name", "First name", auto="given-name")}
{field("last-name", "Last name", auto="family-name")}
{field("email", "Email", "email", "email")}
{field("phone", "Phone", "tel", "tel", req=False)}
              <div class="field field--full">
                <label for="language">Preferred language</label>
                <select id="language" name="language" autocomplete="language">
                  <option>English</option>
                  <option>French</option>
                  <option>Chinese</option>
                  <option>Arabic</option>
                </select>
              </div>
              <div class="field field--full">
                <label for="message">Message <span class="req" aria-hidden="true">*</span></label>
                <textarea id="message" name="message" required aria-describedby="message-error"></textarea>
                <p class="error" id="message-error" hidden>Please enter a message.</p>
              </div>
              <div class="field field--full">
                <label class="consent" for="consent">
                  <input id="consent" name="consent" type="checkbox" required aria-describedby="consent-error">
                  <span>I agree that Maple Dental Vancouver may use the information I provide to respond to my enquiry, as described in the <a href="/privacy-policy/">Privacy Policy</a>.</span>
                </label>
                <p class="error" id="consent-error" hidden>Please confirm you agree before sending.</p>
              </div>
            </div>
            <p style="margin:20px 0 0;font-size:.875rem;color:var(--muted)"><span aria-hidden="true">*</span> Required field</p>
            <button class="btn btn--primary" type="submit" style="margin-top:16px">Send message{icon("arrow")}</button>
            <p class="form-status form-status--info" role="status" tabindex="-1" hidden></p>
          </form>
        </div>
      </div>
    </section>
""" + footer()


# ================================================================ PRIVACY
def privacy():
    return head(
        "Privacy Policy | Maple Dental Vancouver",
        "How Maple Dental Vancouver collects, uses and protects your personal information.",
        "/privacy-policy/") + header("") + page_hero(
        "Legal", "Privacy Policy", "How we collect, use and protect your personal information.") + f"""

    <section class="section">
      <div class="container" style="max-width:860px">
        {ph_block("PRIVACY POLICY FROM CLIENT: must reflect BC's Personal Information Protection Act (PIPA) and the clinic's actual practices, including the contact form, website analytics (if any) and the clinic's privacy officer contact details.")}
      </div>
    </section>
""" + footer()


# ================================================================ WRITE
PAGES = {
    "": home, "about": about, "services": services,
    "new-patients": new_patients, "contact": contact, "privacy-policy": privacy,
}

if __name__ == "__main__":
    for slug, fn in PAGES.items():
        out_dir = os.path.join(ROOT, slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", os.path.join(slug or ".", "index.html"))
