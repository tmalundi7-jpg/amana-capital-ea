import re
import glob

# =========================================================
# 1. UPGRADE style.css
# =========================================================
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# --- A. Brighten nav brand (AMANA CAPITAL) and nav links ---
# Logo primary: was `color: var(--white)` at 85% opacity effectively
# Bump to pure bright white, add subtle gold glow on hover
css = css.replace(
    "color: var(--white);\n      line-height: 1;\n      white-space: nowrap;\n  }",
    "color: #FFFFFF;\n      line-height: 1;\n      white-space: nowrap;\n      text-shadow: 0 0 20px rgba(229,177,59,0.15);\n  }"
)

# Nav links: was rgba(251,247,240,0.85) - bump to full white
css = css.replace(
    "color: rgba(251, 247, 240, 0.85); /* Cream text */",
    "color: #FFFFFF; /* Bright white - improved visibility */"
)

# Also add a brightening override at the end of CSS for the logo-word-secondary subtitle
nav_brightness_override = """
/* ====== NAV BRIGHTNESS UPGRADE ====== */
.logo-word-primary {
    color: #FFFFFF !important;
    text-shadow: 0 0 20px rgba(229,177,59,0.12) !important;
}
.logo-word-secondary {
    color: var(--gold) !important;
    opacity: 1 !important;
}
.nav-links a {
    color: #FFFFFF !important;
}
.nav-links a:hover,
.nav-links a.active {
    color: #FFFFFF !important;
    text-shadow: 0 0 12px rgba(229,177,59,0.5) !important;
}
/* ===================================== */
"""
css += nav_brightness_override

# --- B. Upgrade teaser-prem-left (article) and teaser-prem-right (CTA) visual design ---
teaser_upgrade = """
/* ====== DAILY DSE WRAP TEASER UPGRADE ====== */

/* Outer card: tighter gold border, stronger shadow */
.teaser-premium {
    border: 2px solid var(--gold) !important;
    box-shadow: 0 16px 60px rgba(0,0,0,0.35), 0 0 0 1px rgba(200,150,46,0.1) !important;
    border-radius: 6px !important;
}

/* Left panel: article body */
.teaser-prem-eyebrow {
    margin-bottom: 1.5rem !important;
}
.teaser-prem-label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    color: var(--gold) !important;
}
.teaser-prem-date {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: rgba(251,247,240,0.5) !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    margin-bottom: 1rem !important;
}
.teaser-prem-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: var(--cream) !important;
    line-height: 1.2 !important;
    margin-bottom: 1.5rem !important;
    letter-spacing: -0.5px !important;
}
.teaser-prem-body {
    font-size: 0.92rem !important;
    color: rgba(251,247,240,0.72) !important;
    line-height: 1.75 !important;
    margin-bottom: 2rem !important;
    border-left: 3px solid var(--gold) !important;
    padding-left: 1.25rem !important;
}

/* Right panel: "Institutional Analysis" CTA */
.teaser-prem-right {
    background: rgba(200,150,46,0.07) !important;
    border-left: 1px solid rgba(200,150,46,0.35) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    gap: 1.5rem !important;
    padding: 4rem 3rem !important;
}
.teaser-right-label {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--gold) !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 0 !important;
}
.teaser-right-divider {
    width: 50px !important;
    height: 2px !important;
    background: var(--gold) !important;
    opacity: 0.6 !important;
}
.teaser-right-cta-text {
    font-size: 0.95rem !important;
    color: rgba(251,247,240,0.75) !important;
    line-height: 1.7 !important;
    font-style: italic !important;
}
/* ============================================= */
"""
css += teaser_upgrade

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("style.css updated")

# =========================================================
# 2. UPGRADE about.html — Our Core Purpose hero
# =========================================================
with open('about.html', 'r', encoding='utf-8') as f:
    about = f.read()

# Replace the hero section with an elevated version
old_hero = re.search(r'<section class="ab-hero">.*?</section>', about, re.DOTALL)
if old_hero:
    new_hero = '''<section class="ab-hero">
    <div class="container">
        <div class="ab-hero-inner">
            <!-- Left: Massive Navy Plaque -->
            <div style="background-color: var(--navy); border: 2px solid var(--gold); padding: 5rem 4rem; border-radius: 6px; box-shadow: 0 16px 60px rgba(11,29,58,0.25), 0 0 0 1px rgba(200,150,46,0.08); display: flex; flex-direction: column; justify-content: center;">
                <div style="color: var(--gold); font-size: 0.75rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 2rem; display: flex; align-items: center; gap: 0.75rem;">
                    <span style="display: inline-block; width: 6px; height: 6px; background: var(--gold); border-radius: 50%;"></span>
                    Our Core Purpose
                </div>
                <h1 style="font-family: 'Cormorant Garamond', serif; font-size: 5.5rem; font-weight: 400; color: var(--cream); line-height: 0.95; margin: 0; letter-spacing: -2px;">
                    About<br>Amana<br>Capital<span style="color: var(--gold);">.</span>
                </h1>
                <div style="width: 60px; height: 2px; background: var(--gold); margin-top: 2.5rem; opacity: 0.6;"></div>
            </div>

            <!-- Right: Mission Statement -->
            <div style="padding: 1rem 0 1rem 3.5rem; display: flex; flex-direction: column; justify-content: center; gap: 2rem;">
                <p style="font-family: 'Cormorant Garamond', serif; font-size: 2.1rem; color: var(--navy); line-height: 1.4; margin: 0;">
                    Amana Capital East Africa Limited exists to deliver institutional-grade investment research, advisory, and fund management services rooted in the Dar es Salaam Stock Exchange and East African capital markets.
                </p>

                <div style="width: 70px; height: 3px; background: linear-gradient(90deg, var(--gold), rgba(200,150,46,0.3));"></div>

                <p style="font-size: 1.1rem; color: rgba(11,29,58,0.78); line-height: 1.85; margin: 0; border-left: 3px solid var(--gold); padding-left: 1.25rem;">
                    Our core purpose is to equip Tanzanian investors &mdash; both at home and across the global diaspora &mdash; with the clarity, discipline, and long-horizon perspective needed to build lasting wealth in the region&#x27;s frontier markets.
                </p>
            </div>
        </div>
    </div>
</section>'''
    about = about.replace(old_hero.group(0), new_hero)
    print("about.html hero upgraded")

# bump cache
about = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_25', about)
with open('about.html', 'w', encoding='utf-8') as f:
    f.write(about)

# =========================================================
# 3. BUMP CACHE on all HTML files
# =========================================================
html_files = glob.glob('*.html')
for fname in html_files:
    if fname == 'about.html' or 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_25', c)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c)

print("All HTML cache bumped to v25")
print("Done.")
