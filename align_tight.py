import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace home-gainers
old_gainers = r'<div class="snapshot-mover" id="home-gainers".*?</div>'
new_gainers = """<div class="snapshot-mover" id="home-gainers" style="display: grid; grid-template-columns: auto auto; justify-content: start; row-gap: 0.15rem; column-gap: 0.75rem;">
  <span>NMG</span> <span style="color:var(--gain); text-align:right;">+5.8%</span>
  <span>NMB</span> <span style="color:var(--gain); text-align:right;">+4.9%</span>
  <span>VODA</span> <span style="color:var(--gain); text-align:right;">+1.9%</span>
</div>"""
html = re.sub(old_gainers, new_gainers, html, flags=re.DOTALL)

# Replace home-losers
old_losers = r'<div class="snapshot-mover" id="home-losers".*?</div>'
new_losers = """<div class="snapshot-mover" id="home-losers" style="display: grid; grid-template-columns: auto auto; justify-content: start; row-gap: 0.15rem; column-gap: 0.75rem;">
  <span>TOL</span> <span style="color:var(--loss); text-align:right;">-6.6%</span>
  <span>MBP</span> <span style="color:var(--loss); text-align:right;">-4.8%</span>
  <span>SWIS</span> <span style="color:var(--loss); text-align:right;">-1.6%</span>
</div>"""
html = re.sub(old_losers, new_losers, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_align_tight', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Aligned numbers perfectly. Cache bumped on {bumped} files.")
