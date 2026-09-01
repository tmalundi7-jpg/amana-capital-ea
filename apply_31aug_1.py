import json
import re
import os

with open('extracted_31aug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']['tables'][0][1:]

# Fix minus signs properly
for p in prices:
    p[4] = p[4].replace('\ufffd', '-').replace('–', '-').replace('−', '-')

gainers = sorted([p for p in prices if '+' in p[4] and p[4] != '+0.0%'], key=lambda x: float(x[4].replace('+','').replace('%','')), reverse=True)
losers = sorted([p for p in prices if '-' in p[4] and p[4] != '-0.0%'], key=lambda x: float(x[4].replace('-','').replace('%','')), reverse=False) # Changed to False because larger negative number should be first (-6.0 is smaller than -1.0 so reverse=False puts -6.0 first)
# Wait, if I strip '-', then '6.0' vs '1.0'. I stripped '-', so x is positive float. reverse=True would make 6.0 first.
losers = sorted([p for p in prices if '-' in p[4] and p[4] != '-0.0%'], key=lambda x: float(x[4].replace('-','').replace('%','')), reverse=True)


dsei = "4,440.47"
tsi = "9,897.20"
turnover = "TZS 14.89 bn"

date_str = "31 August 2026"
short_date = "2026-08-31"

wrap_title = data['wrap']['paragraphs'][1]
intro_p = ""
for i, p in enumerate(data['wrap']['paragraphs']):
    if "The era of 15% risk-free yields is ending" in p or "The Dar es Salaam Stock Exchange" in p or "A session that began with" in p or "Monday's session" in p:
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
    gainers_html += f'<span>{gainers[i][0]} <span style="color:var(--gain)">{gainers[i][4]}</span></span>'
replace_in_file('index.html', r'id="home-gainers".*?>.*?</div>', f'id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">{gainers_html}</div>')

losers_html = ""
for i in range(min(3, len(losers))):
    losers_html += f'<span>{losers[i][0]} <span style="color:var(--loss)">{losers[i][4]}</span></span>'
if not losers_html:
    losers_html = '<span>None <span style="color:var(--loss)">0.0%</span></span>'
replace_in_file('index.html', r'id="home-losers".*?>.*?</div>', f'id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">{losers_html}</div>')

replace_in_file('index.html', r'<div class="teaser-prem-date">.*?</div>', f'<div class="teaser-prem-date">Monday, 31st August 2026</div>')
replace_in_file('index.html', r'<h3 class="teaser-prem-title">.*?</h3>', f'<h3 class="teaser-prem-title">{wrap_title}</h3>')
replace_in_file('index.html', r'<p class="teaser-prem-body">.*?</p>', f'<p class="teaser-prem-body">{intro_p}</p>')
replace_in_file('index.html', r'<div class="teaser-prem-stat-label">DSEI</div>.*?<div class="teaser-prem-stat-value">.*?</div>', f'<div class="teaser-prem-stat-label">DSEI</div>\n<div class="teaser-prem-stat-value">{dsei}</div>')
replace_in_file('index.html', r'<div class="teaser-prem-stat-label">Turnover</div>.*?<div class="teaser-prem-stat-value">.*?</div>', f'<div class="teaser-prem-stat-label">Turnover</div>\n<div class="teaser-prem-stat-value">{turnover}</div>')

if gainers:
    g_str = f'<span>{gainers[0][0]}</span> <span style="color: #22c55e;">{gainers[0][4]}</span>'
    replace_in_file('index.html', r'<div class="teaser-prem-stat-value gain".*?>.*?</div>', f'<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: \'Plus Jakarta Sans\', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">\n      {g_str}\n  </div>')
replace_in_file('index.html', r'href="/dse-wrap-[0-9\-]+"', f'href="/dse-wrap-2026-08-31"')

print("Updated index.html")

# --- 2. Market Intelligence ---
replace_in_file('market-intelligence.html', r'<span style="font-size:0.78rem;color:rgba\(251,247,240,0.7\);font-weight:600;">.*?</span>', f'<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">{date_str}</span>')
replace_in_file('market-intelligence.html', r'id="mi-dsei">.*?</div>', f'id="mi-dsei">{dsei}</div>')
replace_in_file('market-intelligence.html', r'id="mi-tsi">.*?</div>', f'id="mi-tsi">{tsi}</div>')
replace_in_file('market-intelligence.html', r'id="mi-turnover">.*?</div>', f'id="mi-turnover">{turnover}</div>')

mi_gainers_html = ""
for i in range(min(3, len(gainers))):
    mi_gainers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{gainers[i][0]}</span> <span style="color:var(--gain)">{gainers[i][4]}</span></div>\n          '
replace_in_file('market-intelligence.html', r'<!-- GAINERS_START -->.*?</div>', f'<!-- GAINERS_START -->\n        <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n          {mi_gainers_html.strip()}\n        </div>')

mi_losers_html = ""
for i in range(min(3, len(losers))):
    mi_losers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{losers[i][0]}</span> <span style="color:var(--loss)">{losers[i][4]}</span></div>\n          '
if not mi_losers_html:
    mi_losers_html = '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>None</span> <span style="color:var(--loss)">0.0%</span></div>'
replace_in_file('market-intelligence.html', r'<!-- LOSERS_START -->.*?</div>', f'<!-- LOSERS_START -->\n        <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n          {mi_losers_html.strip()}\n        </div>')

replace_in_file('market-intelligence.html', r'<div class="archive-date">.*?</div>', f'<div class="archive-date">31 Aug<br/>2026</div>')
replace_in_file('market-intelligence.html', r'<div class="archive-content-title">.*?</div>', f'<div class="archive-content-title">{wrap_title}</div>')
replace_in_file('market-intelligence.html', r'<div class="archive-content-excerpt">.*?</div>', f'<div class="archive-content-excerpt">{intro_p[:130]}...</div>')
replace_in_file('market-intelligence.html', r'<a class="archive-row" href="/dse-wrap-[0-9\-]+">', f'<a class="archive-row" href="/dse-wrap-2026-08-31">')

print("Updated market-intelligence.html")
