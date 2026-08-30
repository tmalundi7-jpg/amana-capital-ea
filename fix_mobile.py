import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# ============================================================
# COMPREHENSIVE MOBILE RESPONSIVENESS OVERRIDE
# Appended at the very end of style.css to override everything
# ============================================================
mobile_css = """

/* ============================================================
   MOBILE RESPONSIVENESS LOCK — v20260830
   Covers: Homepage, Market Intelligence, About, Contact,
           Education, Bond Calculator, DSE Wrap pages, Footer
   ============================================================ */

/* --- BASE MOBILE (max 768px) --- */
@media (max-width: 768px) {

    /* Container */
    .container {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    /* ---- HOMEPAGE ---- */

    /* Hero */
    .home-hero { padding: 3rem 0 2rem !important; }
    .home-hero h1 { font-size: 2.4rem !important; line-height: 1.1 !important; }
    .home-hero-sub { font-size: 0.95rem !important; }
    .home-hero-grid { grid-template-columns: 1fr !important; gap: 2rem !important; }
    .home-hero-stats { grid-template-columns: 1fr !important; gap: 1rem !important; padding-top: 1.5rem !important; border-left: none !important; border-top: 1px solid rgba(255,255,255,0.08) !important; padding-left: 0 !important; }

    /* DSE Snapshot card */
    .snapshot-card { padding: 1.5rem !important; }
    .snapshot-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 0.75rem !important; }
    .snapshot-value { font-size: 1.1rem !important; }
    .home-snapshot-header { flex-direction: column !important; align-items: flex-start !important; gap: 0.75rem !important; }

    /* Why Amana / Governing Principles */
    .why-section { padding: 3rem 0 !important; }
    .why-section-header { flex-direction: column !important; align-items: flex-start !important; gap: 0.75rem !important; margin-bottom: 2rem !important; }
    .why-grid { grid-template-columns: 1fr !important; gap: 1.5rem !important; }
    .section-title { font-size: 1.85rem !important; }

    /* Core Services */
    .services-section { padding: 3rem 0 !important; }
    .services-section-header { flex-direction: column !important; align-items: flex-start !important; gap: 0.75rem !important; margin-bottom: 2rem !important; }
    .services-grid { grid-template-columns: 1fr !important; gap: 1.5rem !important; }

    /* Daily DSE Wrap teaser card */
    .teaser-premium { grid-template-columns: 1fr !important; }
    .teaser-prem-left { padding: 2rem !important; }
    .teaser-prem-right { padding: 2rem !important; border-left: none !important; border-top: 1px solid rgba(200,150,46,0.3) !important; }
    .teaser-prem-title { font-size: 1.6rem !important; }
    .teaser-prem-body { font-size: 0.88rem !important; }
    .teaser-prem-stats { grid-template-columns: 1fr !important; gap: 0.75rem !important; }

    /* Newsletter section */
    .newsletter-premium { padding: 3rem 0 !important; }
    .newsletter-inner { grid-template-columns: 1fr !important; gap: 2rem !important; }
    .newsletter-left h2 { font-size: 1.75rem !important; }

    /* ---- ABOUT PAGE ---- */
    .ab-hero { padding: 3rem 0 !important; }
    .ab-hero-inner { grid-template-columns: 1fr !important; gap: 2rem !important; }
    .ab-hero h1 { font-size: 3.5rem !important; }
    .ab-team-grid { grid-template-columns: 1fr !important; }
    .ab-pillars { grid-template-columns: repeat(2, 1fr) !important; }
    .ab-info-grid { grid-template-columns: 1fr !important; }
    .ab-reg-card { grid-template-columns: 1fr !important; }

    /* ---- MARKET INTELLIGENCE ---- */
    .mi-hero { padding: 3rem 0 2rem !important; }
    .mi-grid, .mi-content-grid { grid-template-columns: 1fr !important; }
    .mi-subscribe-inner { flex-direction: column !important; gap: 1.5rem !important; max-width: 100% !important; }

    /* ---- DSE WRAP ARTICLE PAGES ---- */
    .dse-article-card { padding: 1.5rem !important; }
    .dse-article-card h1 { font-size: 2rem !important; }
    .dse-article-card h2 { font-size: 1.4rem !important; }
    .dse-header-box { padding: 2rem !important; }

    /* ---- BOND CALCULATOR ---- */
    .bc-grid, .bond-grid { grid-template-columns: 1fr !important; }
    .bc-card { padding: 1.5rem !important; }

    /* ---- FOOTER ---- */
    .site-footer .footer-inner,
    .footer-inner { flex-direction: column !important; gap: 2rem !important; text-align: center !important; }
    .footer-brand { align-items: center !important; }
    .footer-nav { flex-wrap: wrap !important; justify-content: center !important; }
    .footer-bottom { flex-direction: column !important; gap: 0.5rem !important; text-align: center !important; }
}

/* --- SMALL MOBILE (max 480px) --- */
@media (max-width: 480px) {

    .container { padding-left: 1rem !important; padding-right: 1rem !important; }

    /* Navbar */
    .logo-word-primary { font-size: 1.1rem !important; }

    /* Homepage hero */
    .home-hero h1 { font-size: 2rem !important; }
    .home-hero-cta { flex-direction: column !important; gap: 0.75rem !important; width: 100% !important; }
    .home-hero-cta .btn { width: 100% !important; text-align: center !important; justify-content: center !important; }

    /* DSE Snapshot */
    .snapshot-grid { grid-template-columns: 1fr !important; }
    .snapshot-value { font-size: 1.2rem !important; }

    /* Teaser stats */
    .teaser-prem-stats { grid-template-columns: 1fr !important; }
    .teaser-prem-title { font-size: 1.4rem !important; }

    /* About hero */
    .ab-hero h1 { font-size: 2.8rem !important; letter-spacing: -1px !important; }
    .ab-pillars { grid-template-columns: 1fr !important; }

    /* DSE wrap article */
    .dse-article-card h1 { font-size: 1.6rem !important; }

    /* Buttons */
    .btn { padding: 0.75rem 1.25rem !important; font-size: 0.88rem !important; }
}

/* --- TABLET (max 1024px) --- */
@media (max-width: 1024px) {
    .why-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .services-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .home-hero-grid { grid-template-columns: 1fr !important; gap: 2.5rem !important; }
    .snapshot-grid { grid-template-columns: repeat(3, 1fr) !important; }
    .teaser-premium { grid-template-columns: 1.2fr 1fr !important; }
    .ab-hero-inner { grid-template-columns: 1fr !important; gap: 2rem !important; }
}

/* ============================================================ */
"""

css += mobile_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bump cache on all HTML files
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v1', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Mobile CSS appended. Cache bumped on {bumped} files.")
