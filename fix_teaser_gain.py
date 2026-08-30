import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the Top Gainer HTML in the teaser to use spans for left/right alignment
old_gain = r'<div class="teaser-prem-stat-value gain">NMG \+5\.8%</div>'
new_gain = """<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">
    <span>NMG</span> <span style="color: #22c55e;">+5.8%</span>
</div>"""

html = re.sub(old_gain, new_gain, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make sure all teaser stat tiles align their values properly
css_override = """
/* ============================================================
   ALIGN TEASER STATS VALUES
   ============================================================ */
.teaser-prem-stats > div, .teaser-prem-stat {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
}

/* Ensure the label has a consistent height so the values line up */
.teaser-prem-stat-label {
    min-height: 24px !important;
    display: flex !important;
    align-items: flex-end !important;
    margin-bottom: 0.5rem !important;
    white-space: nowrap !important; /* Prevent 'Top Gainer' from wrapping and pushing the value down */
}

/* If the text is a gain label, make it sans-serif and slightly smaller so it fits */
.teaser-prem-stat-value.gain {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    margin-top: auto !important; /* Pushes the value up/down to align if needed, but flex-start is on parent */
}
/* ============================================================ */
"""

css += css_override

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_align', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Fixed teaser gain alignment. Cache bumped on {bumped} files.")
