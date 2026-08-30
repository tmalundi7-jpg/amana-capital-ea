import re
import glob

# 1. Fix market-intelligence.html HTML structure
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

# Make sure all children of .snapshot-grid have class="snapshot-item"
mi_html = re.sub(r'<div class="snapshot-grid">\s*<div>', '<div class="snapshot-grid">\n  <div class="snapshot-item">', mi_html)
mi_html = re.sub(r'</div>\s*<div>\s*<div class="snapshot-label"', '</div>\n  <div class="snapshot-item">\n  <div class="snapshot-label"', mi_html)
mi_html = re.sub(r'</div>\s*<div>\s*<div class="snapshot-label"', '</div>\n  <div class="snapshot-item">\n  <div class="snapshot-label"', mi_html)
mi_html = re.sub(r'</div>\s*<div>\s*<div class="snapshot-label"', '</div>\n  <div class="snapshot-item">\n  <div class="snapshot-label"', mi_html)
mi_html = re.sub(r'</div>\s*<div>\s*<div class="snapshot-label"', '</div>\n  <div class="snapshot-item">\n  <div class="snapshot-label"', mi_html)

# Remove the inline styles from mi_html that might conflict
mi_html = re.sub(r'\.snapshot-grid \{[^}]+\}', '', mi_html)
mi_html = re.sub(r'\.snapshot-label \{[^}]+\}', '', mi_html)
mi_html = re.sub(r'\.snapshot-value \{[^}]+\}', '', mi_html)
mi_html = re.sub(r'\.snapshot-mover \{[^}]+\}', '', mi_html)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

# 2. Add upgraded CSS to style.css
css_updates = """
/* --- SNAPSHOT GRID UPGRADE --- */
.snapshot-grid {
    display: grid !important;
    grid-template-columns: repeat(5, 1fr) !important;
    gap: 1rem !important;
    width: 100% !important;
}
.snapshot-item {
    background-color: var(--navy) !important;
    border: 1px solid rgba(200,150,46,0.3) !important;
    border-top: 3px solid var(--gold) !important;
    border-right: 1px solid rgba(200,150,46,0.3) !important; /* Override old inline right-borders */
    padding: 1.25rem !important;
    border-radius: 4px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    display: flex;
    flex-direction: column;
}
.snapshot-label {
    font-size: 0.65rem !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: 0.5rem !important;
    font-weight: 700 !important;
}
.snapshot-value {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--cream) !important;
    font-variant-numeric: tabular-nums !important;
    margin-bottom: 0.2rem !important;
}
/* For the Gainers/Losers lists inside the snapshot items */
.snapshot-item .snapshot-mover,
.snapshot-item div[style*="font-size:0.85rem;"] {
    font-size: 0.75rem !important;
    color: var(--cream) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    margin-bottom: 0.2rem !important;
}
/* Ensure the charts scale down */
.snapshot-item canvas {
    max-width: 100% !important;
    height: auto !important;
    margin-top: auto !important; /* Push to bottom */
}
.snapshot-bar-chart {
    margin-top: auto !important;
}

@media (max-width: 860px) {
    .snapshot-grid { grid-template-columns: repeat(3, 1fr) !important; }
}
@media (max-width: 540px) {
    .snapshot-grid { grid-template-columns: repeat(2, 1fr) !important; }
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
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_19', c2)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c2)

print('Upgraded Snapshot grids')
