import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace space-between with flex-start and a small gap for gainers
old_gainers_regex = r'<div class="snapshot-mover" id="home-gainers".*?</div>\s*</div>'
new_gainers = """<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.15rem; width:100%;">
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
  </div>
  </div>"""

html = re.sub(old_gainers_regex, new_gainers, html, flags=re.DOTALL)

# Same for losers
old_losers_regex = r'<div class="snapshot-mover" id="home-losers".*?</div>\s*</div>'
new_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.15rem; width:100%;">
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
      <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
  </div>
  </div>"""

html = re.sub(old_losers_regex, new_losers, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Also fix market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

mi_gainers_regex = r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->'
mi_new_gainers = """<!-- GAINERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
      </div>
      <!-- GAINERS_END -->"""
mi_html = re.sub(mi_gainers_regex, mi_new_gainers, mi_html, flags=re.DOTALL)

mi_losers_regex = r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->'
mi_new_losers = """<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
        <div style="display:flex; justify-content:flex-start; gap: 0.5rem; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
      </div>
      <!-- LOSERS_END -->"""
mi_html = re.sub(mi_losers_regex, mi_new_losers, mi_html, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

# Bump cache on all HTML files
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_nospace', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Fixed spacing. Cache bumped on {bumped} files.")
