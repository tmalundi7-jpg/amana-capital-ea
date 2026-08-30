import re
import glob

# 1. Update Footer everywhere
html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace the footer text inline styling
    old_footer = r'<div style="color: var\(--gold\); font-weight: 800; letter-spacing: 0.1em; font-size: 0.85rem; margin-bottom: 0.3rem;">AMANA CAPITAL EAST AFRICA</div>'
    new_footer = r'<div style="font-family: \'Cormorant Garamond\', serif; color: var(--gold); font-weight: 600; letter-spacing: 3px; font-size: 1.6rem; margin-bottom: 0.3rem;">AMANA CAPITAL EAST AFRICA</div>'
    content = re.sub(old_footer, new_footer, content)

    # 2. Update Market Intelligence Newsletter
    if fname == 'market-intelligence.html':
        old_h2 = r'<h2>Never Miss a<br/><em>Market Signal</em></h2>'
        new_h2 = r'<h2 style="font-family: \'Cormorant Garamond\', serif; font-size: 3.5rem; font-weight: 400; color: var(--navy); line-height: 1.1; margin-bottom: 1.5rem;">Never Miss a<br/><em>Market Signal</em></h2>'
        content = re.sub(old_h2, new_h2, content)
        
        old_p = r'<p>Daily DSE wraps and macroeconomic briefings delivered to your inbox every trading day\. Institutional quality\. Completely free\.</p>'
        new_p = r'<p style="font-family: \'Inter\', sans-serif; font-size: 1.15rem; line-height: 1.6; color: rgba(11,29,58,0.85);">Daily DSE wraps and macroeconomic briefings delivered to your inbox every trading day. Institutional quality. Completely free.</p>'
        content = re.sub(old_p, new_p, content)

    # Bump cache buster
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_7', content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Update style.css for Daily Wrap (Cream and Gold) and tabular numbers
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will append the ultimate fix to style.css to override everything for .teaser-prem-left
css_fix = """
/* FINAL ULTIMATE DAILY WRAP REVERT (CREAM AND GOLD) */
.home-teaser {
    background-color: var(--cream) !important;
}
.home-teaser .teaser-premium {
    background-color: var(--cream) !important;
    border: 1px solid var(--gold) !important;
    box-shadow: 0 10px 40px rgba(200, 150, 46, 0.15) !important;
}
.home-teaser .teaser-prem-left {
    background-color: var(--cream) !important;
    border-right: 1px solid rgba(200, 150, 46, 0.3) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-eyebrow .teaser-prem-label,
.home-teaser .teaser-prem-left .teaser-prem-date {
    color: rgba(11, 29, 58, 0.7) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-title {
    color: var(--navy) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-body {
    color: rgba(11, 29, 58, 0.8) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-stats {
    border-top: 1px solid rgba(200, 150, 46, 0.2) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-stat-label {
    color: rgba(11, 29, 58, 0.6) !important;
}
.home-teaser .teaser-prem-left .teaser-prem-stat-value {
    color: var(--navy) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-variant-numeric: tabular-nums !important;
}
.home-teaser .teaser-prem-left .teaser-prem-stat-value.gain {
    color: #16a34a !important; /* Readable green on cream */
}
.home-teaser .teaser-prem-left .teaser-prem-stat-value.loss {
    color: #dc2626 !important; /* Readable red on cream */
}

/* Global Tabular Nums */
#amortization-schedule td,
.snapshot-val,
.snapshot-row,
.bc-result-val,
.numerical,
.number-cell {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-variant-numeric: tabular-nums !important;
}
"""
css += css_fix

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied final design fixes!")
