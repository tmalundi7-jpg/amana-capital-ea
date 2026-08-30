import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Strip out the previous mobile block I added
match = re.search(r'/\* ============================================================\n   MOBILE RESPONSIVENESS LOCK — v20260830.*', css, re.DOTALL)
if match:
    css = css[:match.start()]
    print('Removed old mobile lock block.')
else:
    print('Could not find mobile lock block.')

# Let's write the updated mobile CSS lock
mobile_css_v3 = """
/* ============================================================
   MOBILE RESPONSIVENESS LOCK — v3 (Compact & Grid-based)
   ============================================================ */

/* --- BASE MOBILE (max 768px) --- */
@media (max-width: 768px) {
    /* Keep padding tight */
    .container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Hero: Slightly smaller fonts, but keep horizontal stats structure */
    .home-hero { padding: 3rem 0 2rem !important; }
    .home-hero h1 { font-size: 2.2rem !important; line-height: 1.1 !important; }
    .home-hero-stats { 
        display: grid !important; 
        grid-template-columns: repeat(3, 1fr) !important; 
        gap: 0.5rem !important;
        padding-top: 1.5rem !important; 
        border-left: none !important; 
        border-top: 1px solid rgba(255,255,255,0.08) !important; 
        padding-left: 0 !important; 
    }

    /* DSE Snapshot: Keep horizontal scroll or wrap into 2 columns max */
    .snapshot-card { padding: 1.25rem !important; }
    .snapshot-grid { 
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important; 
        gap: 0.5rem !important; 
    }
    /* Let the Top Gainers / Losers span 2 columns so they aren't squished */
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 2 !important;
    }
    
    .snapshot-value { font-size: 1.15rem !important; }
    .snapshot-label { font-size: 0.65rem !important; margin-bottom: 0.25rem !important; }

    /* Core Services & Why Amana: 2 columns is better than 1 if cards are compact */
    .why-section, .services-section { padding: 2.5rem 0 !important; }
    .why-grid { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1rem !important; }
    .services-grid { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1rem !important; }
    .section-title { font-size: 1.6rem !important; margin-bottom: 0 !important; }
    .why-section-header, .services-section-header { margin-bottom: 1.5rem !important; }

    /* Daily DSE Wrap teaser card */
    .teaser-premium { grid-template-columns: 1fr !important; }
    .teaser-prem-left, .teaser-prem-right { padding: 1.5rem !important; }
    .teaser-prem-right { border-left: none !important; border-top: 1px solid rgba(200,150,46,0.3) !important; }
    .teaser-prem-title { font-size: 1.6rem !important; }
    .teaser-prem-body { font-size: 0.9rem !important; margin-bottom: 1rem !important; }
    
    /* Keep the teaser stats HORIZONTAL in 3 columns */
    .teaser-prem-stats { 
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important; 
        gap: 0.5rem !important; 
    }
    .teaser-prem-stat, .teaser-prem-stats > div {
        padding: 0.75rem !important;
    }
    .teaser-prem-stat-label { font-size: 0.6rem !important; }
    .teaser-prem-stat-value { font-size: 1.15rem !important; }

    /* Newsletter section */
    .newsletter-premium { padding: 2.5rem 0 !important; }
    .newsletter-inner { grid-template-columns: 1fr !important; gap: 1.5rem !important; }
    .newsletter-left h2 { font-size: 1.6rem !important; }

    /* About page */
    .ab-hero { padding: 2.5rem 0 !important; }
    .ab-hero-inner { grid-template-columns: 1fr !important; gap: 1.5rem !important; }
    .ab-hero h1 { font-size: 3rem !important; }
    .ab-pillars { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1rem !important; }

    /* Market Intelligence */
    .mi-hero { padding: 2.5rem 0 !important; }
    .mi-grid { display: grid !important; grid-template-columns: 1fr !important; }

    /* Footer */
    .footer-inner { flex-direction: column !important; gap: 1.5rem !important; }
    .footer-nav { flex-wrap: wrap !important; gap: 1rem !important; justify-content: space-between !important; }
}

/* --- SMALL MOBILE (max 480px) --- */
@media (max-width: 480px) {
    /* Even on tiny screens, try to keep stats horizontal by using smaller text and padding */
    .home-hero-stats { gap: 0.25rem !important; }
    .home-hero-stats h4 { font-size: 1rem !important; }
    .snapshot-card { padding: 1rem !important; }
    .snapshot-grid { grid-template-columns: repeat(2, 1fr) !important; }
    
    /* On tiny screens, why grid and services grid can go to 1 column, but with tight gaps */
    .why-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }
    .services-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }
    
    /* Keep teaser stats 3 columns but super compact */
    .teaser-prem-stats { gap: 0.25rem !important; }
    .teaser-prem-stat, .teaser-prem-stats > div { padding: 0.5rem !important; }
    .teaser-prem-stat-value { font-size: 1rem !important; }
    .teaser-prem-stat-label { font-size: 0.55rem !important; min-height: 18px !important; }
}

/* ============================================================ */
/* ====== NAV BRIGHTNESS LOCK v3 (FINAL) ====== */
.logo-word-primary {
    color: #FFFFFF !important;
    text-shadow: 0 0 20px rgba(229,177,59,0.12) !important;
}
.logo-word-secondary {
    color: #e5b13b !important;
    opacity: 1 !important;
}
.nav-links a {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
.nav-links a:hover,
.nav-links a.active {
    color: #FFFFFF !important;
    text-shadow: 0 0 12px rgba(229,177,59,0.5) !important;
}
/* ============================================= */
"""

css += mobile_css_v3

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v4', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Done. Cache bumped on {bumped} files.")
