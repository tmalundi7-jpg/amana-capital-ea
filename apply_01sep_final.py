import json
import re
import os

with open('extracted_01sep.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']['tables'][0][1:]
# Fix minus signs properly
for p in prices:
    p[4] = p[4].replace('\ufffd', '-').replace('?"', '-').replace("^'", "-")

gainers = sorted([p for p in prices if '+' in p[4] and p[4] != '+0.0%'], key=lambda x: float(x[4].replace('+','').replace('%','')), reverse=True)
losers = sorted([p for p in prices if '-' in p[4] and p[4] != '-0.0%'], key=lambda x: float(x[4].replace('-','').replace('%','')), reverse=True)

dsei = "4,395.95"
tsi = "9,758.17" 
turnover = "TZS 16.39 bn"

vol_sum = sum([int(row[5].replace(',', '')) for row in prices if row[5] != '-'])
volume = f"{vol_sum:,}"

date_str = "1 September 2026"
short_date = "2026-09-01"
cache_bust = "20260901_1sep_update"

wrap_title = "Daily DSE Wrap | 1 September 2026"
for i, p in enumerate(data['wrap']['paragraphs']):
    if "Daily DSE Wrap" in p:
        wrap_title = p
        break

intro_p = ""
for i, p in enumerate(data['wrap']['paragraphs']):
    if "The Dar es Salaam Stock Exchange" in p:
        intro_p = p
        break

def replace_in_file(filepath, pattern, replacement):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    c = re.sub(pattern, replacement, c, flags=re.DOTALL)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

# --- 1. Index.html ---
replace_in_file('index.html', r'id="home-dsei">.*?</div>', f'id="home-dsei">{dsei}</div>')
replace_in_file('index.html', r'id="home-tsi">.*?</div>', f'id="home-tsi">{tsi}</div>')
replace_in_file('index.html', r'id="home-turnover">.*?</div>', f'id="home-turnover">{turnover}</div>')
replace_in_file('index.html', r'id="home-snapshot-date">.*?</div>', f'id="home-snapshot-date">Terminal Feed | End-of-day, {date_str}</div>')

gainers_html = ""
for i in range(min(3, len(gainers))):
    gainers_html += f'<span>{gainers[i][0]} <span style="color:var(--gain)">{gainers[i][4]}</span></span>\n            '
replace_in_file('index.html', r'id="home-gainers".*?>.*?</div>', f'id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">\n            {gainers_html.strip()}\n          </div>')

losers_html = ""
for i in range(min(3, len(losers))):
    losers_html += f'<span>{losers[i][0]} <span style="color:var(--loss)">{losers[i][4]}</span></span>\n            '
if not losers_html:
    losers_html = '<span>None <span style="color:var(--loss)">0.0%</span></span>'
replace_in_file('index.html', r'id="home-losers".*?>.*?</div>', f'id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">\n            {losers_html.strip()}\n          </div>')

replace_in_file('index.html', r'<div class="teaser-prem-date">.*?</div>', f'<div class="teaser-prem-date">Tuesday, 1st September 2026</div>')
replace_in_file('index.html', r'<h3 class="teaser-prem-title">.*?</h3>', f'<h3 class="teaser-prem-title">{wrap_title}</h3>')
replace_in_file('index.html', r'<p class="teaser-prem-body">.*?</p>', f'<p class="teaser-prem-body">{intro_p}</p>')
replace_in_file('index.html', r'<div class="teaser-prem-stat-label">DSEI</div>.*?<div class="teaser-prem-stat-value">.*?</div>', f'<div class="teaser-prem-stat-label">DSEI</div>\n                <div class="teaser-prem-stat-value">{dsei}</div>')
replace_in_file('index.html', r'<div class="teaser-prem-stat-label">Turnover</div>.*?<div class="teaser-prem-stat-value">.*?</div>', f'<div class="teaser-prem-stat-label">Turnover</div>\n                <div class="teaser-prem-stat-value">{turnover}</div>')

if gainers:
    g_str = f'<span>{gainers[0][0]}</span> <span style="color: #22c55e;">{gainers[0][4]}</span>'
    replace_in_file('index.html', r'<div class="teaser-prem-stat-value gain".*?>.*?</div>', f'<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: \'Plus Jakarta Sans\', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">\n                  {g_str}\n                </div>')
replace_in_file('index.html', r'href="/dse-wrap-[0-9\-]+"', f'href="/dse-wrap-{short_date}"')

print("Updated index.html")

# --- 2. Market Intelligence ---
replace_in_file('market-intelligence.html', r'<span style="font-size:0.78rem;color:rgba\(251,247,240,0.7\);font-weight:600;">.*?</span>', f'<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">{date_str}</span>')
replace_in_file('market-intelligence.html', r'id="mi-dsei">.*?</div>', f'id="mi-dsei">{dsei}</div>')
replace_in_file('market-intelligence.html', r'id="mi-tsi">.*?</div>', f'id="mi-tsi">{tsi}</div>')
replace_in_file('market-intelligence.html', r'id="mi-turnover">.*?</div>', f'id="mi-turnover">{turnover}</div>')

mi_gainers_html = ""
for i in range(min(3, len(gainers))):
    mi_gainers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{gainers[i][0]}</span> <span style="color:var(--gain)">{gainers[i][4]}</span></div>\n        '
replace_in_file('market-intelligence.html', r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', f'<!-- GAINERS_START -->\n      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n        {mi_gainers_html.strip()}\n      </div>\n      <!-- GAINERS_END -->')

mi_losers_html = ""
for i in range(min(3, len(losers))):
    mi_losers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{losers[i][0]}</span> <span style="color:var(--loss)">{losers[i][4]}</span></div>\n        '
if not mi_losers_html:
    mi_losers_html = '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>None</span> <span style="color:var(--loss)">0.0%</span></div>\n        '
replace_in_file('market-intelligence.html', r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', f'<!-- LOSERS_START -->\n      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n        {mi_losers_html.strip()}\n      </div>\n      <!-- LOSERS_END -->')

replace_in_file('market-intelligence.html', r'<div class="archive-date">.*?</div>', f'<div class="archive-date">01 Sep<br/>2026</div>')
replace_in_file('market-intelligence.html', r'<div class="archive-content-title">.*?</div>', f'<div class="archive-content-title">{wrap_title}</div>')
replace_in_file('market-intelligence.html', r'<div class="archive-content-excerpt">.*?</div>', f'<div class="archive-content-excerpt">{intro_p[:130]}...</div>')
replace_in_file('market-intelligence.html', r'<a class="archive-row" href="/dse-wrap-[0-9\-]+">', f'<a class="archive-row" href="/dse-wrap-{short_date}">')

print("Updated market-intelligence.html")

# --- 3. Current Prices ---
prices_table_rows = ""
for row in prices:
    cls = ""
    if "+" in row[4]: cls = "gain"
    if "-" in row[4] and row[4] != "-0.0%": cls = "loss"
    
    # Check if empty string or '-'
    for j in range(len(row)):
        if row[j] == '-': row[j] = '-'
        
    prices_table_rows += f"<tr>\n  <td>{row[0]}</td>\n  <td>{row[1]}</td>\n  <td>{row[2]}</td>\n  <td>{row[3]}</td>\n  <td class=\"{cls}\">{row[4]}</td>\n  <td>{row[5]}</td>\n  <td>{row[6]}</td>\n</tr>\n"

replace_in_file('current-prices.html', r'<tbody>.*?</tbody>', f'<tbody>\n{prices_table_rows}</tbody>')
replace_in_file('current-prices.html', r'<span class="snapshot-value">DSEI:.*?</span>', f'<span class="snapshot-value">DSEI: {dsei}</span>')
replace_in_file('current-prices.html', r'<span class="snapshot-value">TSI:.*?</span>', f'<span class="snapshot-value">TSI: {tsi}</span>')
replace_in_file('current-prices.html', r'<span class="snapshot-value">Turnover:.*?</span>', f'<span class="snapshot-value">Turnover: {turnover}</span>')
replace_in_file('current-prices.html', r'<span class="snapshot-value">Volume:.*?</span>', f'<span class="snapshot-value">Volume: {volume}</span>')
replace_in_file('current-prices.html', r'<div class="snapshot-date">.*?</div>', f'<div class="snapshot-date">Prices as of {date_str}</div>')

print("Updated current-prices.html")

# --- 4. Market Intelligence Archive ---
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    archive_html = f.read()

new_arc_row = f"""
        <div class="arc-row">
            <div class="arc-date">01 Sep<br/>2026</div>
            <div class="arc-title">{wrap_title}</div>
            <div class="arc-excerpt">{intro_p[:150]}...</div>
            <div class="arc-link"><a href="/dse-wrap-{short_date}" class="gold-link">Read Full Report &rarr;</a></div>
        </div>
"""
# Insert before the first arc-row
archive_html = re.sub(r'(<div class="archive-list">.*?)(<div class="arc-row">)', rf'\1{new_arc_row}\2', archive_html, count=1, flags=re.DOTALL)

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(archive_html)

print("Updated market-intelligence-archive.html")

# --- 5. Cache busting ---
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', f'style.css?v={cache_bust}', c)
    if new_c != c:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_c)

print(f"Busted CSS cache with v={cache_bust}")
