import re
import os

repo_dir = r"C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main"
index_path = os.path.join(repo_dir, "index.html")
mi_path = os.path.join(repo_dir, "market-intelligence.html")

# Read index.html
with open(index_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Update index.html
idx = re.sub(r'(<div class="snapshot-value" id="home-dsei">).*?(</div>)', r'\g<1>4,102.83\g<2>', idx)
idx = re.sub(r'(<div class="snapshot-value" id="home-tsi">).*?(</div>)', r'\g<1>8,952.33\g<2>', idx)
idx = re.sub(r'(<div class="snapshot-value" id="home-turnover">).*?(</div>)', r'\g<1>TZS 1.72 bn\g<2>', idx)

gainers_html = 'PAL <span style="color:var(--gain)">+9.2%</span><br>MBP <span style="color:var(--gain)">+6.3%</span><br>SWIS <span style="color:var(--gain)">+5.6%</span>'
idx = re.sub(r'(<div class="snapshot-mover" id="home-gainers">).*?(</div>)', r'\1' + gainers_html + r'\2', idx, flags=re.DOTALL)

losers_html = 'NMG <span style="color:var(--loss)">-3.8%</span><br>DSE <span style="color:var(--loss)">-2.0%</span><br>MKCB <span style="color:var(--loss)">-1.4%</span>'
idx = re.sub(r'(<div class="snapshot-mover" id="home-losers">).*?(</div>)', r'\1' + losers_html + r'\2', idx, flags=re.DOTALL)

idx = re.sub(r'(<div class="snapshot-note" id="home-snapshot-date">)End‑of‑day,.*?( For educational purposes only\.</div>)', r'\g<1>End‑of‑day, 21st July 2026.\g<2>', idx)

# Write index.html
with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx)

# Read market-intelligence.html
with open(mi_path, "r", encoding="utf-8") as f:
    mi = f.read()

# The user thinks mi-dsei, mi-tsi, mi-turnover exist. If they don't, we add them to the div.
mi = re.sub(r'(<div class="snapshot-label">DSEI</div>\s*<div class="snapshot-value")[^>]*>.*?(</div>)', r'\1 id="mi-dsei">4,102.83\2', mi)
mi = re.sub(r'(<div class="snapshot-label">TSI</div>\s*<div class="snapshot-value")[^>]*>.*?(</div>)', r'\1 id="mi-tsi">8,952.33\2', mi)
mi = re.sub(r'(<div class="snapshot-label">Turnover \(TZS\)</div>\s*<div class="snapshot-value")[^>]*>.*?(</div>)', r'\1 id="mi-turnover">TZS 1.72 bn\2', mi)

mi_gainers = '''<!-- GAINERS_START -->
<div class="snapshot-mover" id="mi-gainer">PAL <span style="color:#16A34A">+9.2%</span></div>
<div class="snapshot-mover" id="mi-gainer">MBP <span style="color:#16A34A">+6.3%</span></div>
<div class="snapshot-mover" id="mi-gainer">SWIS <span style="color:#16A34A">+5.6%</span></div>
<!-- GAINERS_END -->'''

mi_losers = '''<!-- LOSERS_START -->
<div class="snapshot-mover" id="mi-loser">NMG <span style="color:#DC2626">-3.8%</span></div>
<div class="snapshot-mover" id="mi-loser">DSE <span style="color:#DC2626">-2.0%</span></div>
<div class="snapshot-mover" id="mi-loser">MKCB <span style="color:#DC2626">-1.4%</span></div>
<!-- LOSERS_END -->'''

# Replace top gainers
mi = re.sub(r'(<div class="snapshot-label">Top Gainers</div>\s*)<div class="snapshot-mover">.*?</div>', r'\1' + mi_gainers, mi, flags=re.DOTALL)
# If <!-- GAINERS_START --> already existed, the above might not match if it was modified, so let's check
if '<!-- GAINERS_START -->' in mi:
    mi = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', mi_gainers, mi, flags=re.DOTALL)

# Replace top losers
mi = re.sub(r'(<div class="snapshot-label">Top Losers</div>\s*)<div class="snapshot-mover">.*?</div>', r'\1' + mi_losers, mi, flags=re.DOTALL)
if '<!-- LOSERS_START -->' in mi:
    mi = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', mi_losers, mi, flags=re.DOTALL)

# Replace timestamp
# The user wants <div class="snapshot-timestamp">, currently it's a span with a style. Let's make it a div with class snapshot-timestamp
mi = re.sub(r'<span style="font-size: 0\.8rem; color: var\(--mist\); font-weight: 600; text-transform: uppercase;">.*?</span>', r'<div class="snapshot-timestamp" style="font-size: 0.8rem; color: var(--mist); font-weight: 600; text-transform: uppercase;">21st July 2026</div>', mi)

if '<div class="snapshot-timestamp">' in mi:
    mi = re.sub(r'(<div class="snapshot-timestamp"[^>]*>).*?(</div>)', r'\g<1>21st July 2026\g<2>', mi)

with open(mi_path, "w", encoding="utf-8") as f:
    f.write(mi)

print("Updates applied successfully.")
