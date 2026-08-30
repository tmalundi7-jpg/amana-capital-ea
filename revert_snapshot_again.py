import re
import glob

# 1. Restore the HTML for Top Gainers and Top Losers back to the raw spans
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

gainers_html = """<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>NMG <span style="color:var(--gain)">+5.8%</span></span><span>NMB <span style="color:var(--gain)">+4.9%</span></span><span>VODA <span style="color:var(--gain)">+1.9%</span></span></div>"""
html = re.sub(r'<div class="snapshot-mover" id="home-gainers".*?</div>', gainers_html, html, flags=re.DOTALL)

losers_html = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>TOL <span style="color:var(--loss)">-6.6%</span></span><span>MBP <span style="color:var(--loss)">-4.8%</span></span><span>SWIS <span style="color:var(--loss)">-1.6%</span></span></div>"""
html = re.sub(r'<div class="snapshot-mover" id="home-losers".*?</div>', losers_html, html, flags=re.DOTALL)

# Revert the section padding around the snapshot back to 5rem 0
html = html.replace('<section style="padding: 3rem 0 1rem 0; background: var(--cream);">', '<section style="padding: 5rem 0; background: var(--cream);">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Revert the snapshot-card padding reduction in style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the REDUCE SNAPSHOT SQUARE SIZE AND BOTTOM MARGIN block
css = re.sub(r'/\* ============================================================\n   REDUCE SNAPSHOT SQUARE SIZE AND BOTTOM MARGIN\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_revert_snapshot_again', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Reverted snapshot layout again. Cache bumped on {bumped} files.")
