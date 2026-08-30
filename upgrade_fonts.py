import re
import glob

# 1. Update market-intelligence.html "Turnover (TZS)" -> "Turnover"
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

mi = mi.replace('<div class="snapshot-label" style="color:rgba(251,247,240,0.85);">Turnover (TZS)</div>', '<div class="snapshot-label" style="color:rgba(251,247,240,0.85);">Turnover</div>')
# If it was already stripped of inline styles:
mi = mi.replace('<div class="snapshot-label">Turnover (TZS)</div>', '<div class="snapshot-label">Turnover</div>')
mi = mi.replace('<div class="snapshot-value" id="mi-turnover">10.20 bn</div>', '<div class="snapshot-value" id="mi-turnover">TZS 10.20 bn</div>')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi)

# 2. Append CSS upgrades to style.css
css_updates = """
/* --- GLOBAL TYPOGRAPHY UNISON & UPGRADE --- */
body, p, a, li, input, button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
h1, h2, h3, h4, h5, h6, .brand-text, .section-title, .ab-title, .teaser-prem-title, .why-section-header .section-title {
    font-family: 'Cormorant Garamond', serif !important;
}

/* Ensure all primary financial snapshot numbers are strictly elegant serif */
.snapshot-value, .teaser-prem-stat-value {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 700 !important;
    font-variant-numeric: tabular-nums !important;
}

/* Fix Horizontal Alignment of the 5-Grid Snapshot */
.snapshot-label {
    min-height: 24px !important; /* Forces all labels to identical height, perfectly aligning the numbers below them */
    display: flex !important;
    align-items: flex-end !important;
}

/* --- DAILY DSE WRAP MINI-SNAPSHOT UPGRADE --- */
.teaser-prem-stats {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 1rem !important;
    border-top: none !important; /* Remove old border */
    padding-top: 1.5rem !important;
}
.teaser-prem-stat, .teaser-prem-stats > div {
    background-color: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(200,150,46,0.2) !important;
    border-top: 3px solid var(--gold) !important;
    padding: 1rem !important;
    border-radius: 4px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}
.teaser-prem-stat-label {
    color: var(--gold) !important;
    font-size: 0.65rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.teaser-prem-stat-value {
    font-size: 1.4rem !important;
    color: var(--cream) !important;
}
/* Ensure the +5.8% gain tag looks like the main grid */
.teaser-prem-stat-value.gain {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    color: #22c55e !important; /* Keeping the requested green */
    display: flex;
    align-items: center;
    height: 100%;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_updates)

# 3. Bump cache
html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_20', c2)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c2)

print('Upgraded typography and mini snapshot')
