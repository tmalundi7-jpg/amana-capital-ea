import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_grid = """<!-- SNAPSHOT_CARD_START -->
  <div class="snapshot-grid">
  <div class="snapshot-item">
  <div class="snapshot-label">DSEI</div>
  <div class="snapshot-value" id="home-dsei" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.4rem; font-weight: 700; color: var(--navy);">4,444.48</div>
  </div>
  <div class="snapshot-item">
  <div class="snapshot-label">TSI</div>
  <div class="snapshot-value" id="home-tsi" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.4rem; font-weight: 700; color: var(--navy);">4,484.05</div>
  </div>
  <div class="snapshot-item">
  <div class="snapshot-label">Turnover</div>
  <div class="snapshot-value" id="home-turnover" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.4rem; font-weight: 700; color: var(--navy);">TZS 10.20 bn</div>
  </div>
  <div class="snapshot-item">
  <div class="snapshot-label">Top Gainers</div>
  <div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.15rem; width:100%; font-family: 'Plus Jakarta Sans', sans-serif; font-size:0.75rem; font-weight:700; color:var(--navy);">
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
  </div>
  </div>
  <div class="snapshot-item">
  <div class="snapshot-label">Top Losers</div>
  <div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.15rem; width:100%; font-family: 'Plus Jakarta Sans', sans-serif; font-size:0.75rem; font-weight:700; color:var(--navy);">
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
      <div style="display:flex; justify-content:start; gap:0.5rem;"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
  </div>
  </div>
  </div>"""

html = re.sub(r'<!-- SNAPSHOT_CARD_START -->.*?</div>\s*<div class="snapshot-note"', new_grid + '\n  <div class="snapshot-note"', html, flags=re.DOTALL)

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_match_text_style', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Matched text style on Homepage. Cache bumped on {bumped} files.")
