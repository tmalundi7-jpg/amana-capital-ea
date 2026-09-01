import json
import re

with open('extracted_31aug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']['tables'][0][1:]
for p in prices:
    p[4] = p[4].replace('\ufffd', '-').replace('–', '-').replace('−', '-')

gainers = sorted([p for p in prices if '+' in p[4] and p[4] != '+0.0%'], key=lambda x: float(x[4].replace('+','').replace('%','')), reverse=True)
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

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update date
html = re.sub(r'<span style="font-size:0.78rem;color:rgba\(251,247,240,0.7\);font-weight:600;">.*?</span>', f'<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">{date_str}</span>', html)
# Update simple values
html = re.sub(r'id="mi-dsei">.*?</div>', f'id="mi-dsei">{dsei}</div>', html)
html = re.sub(r'id="mi-tsi">.*?</div>', f'id="mi-tsi">{tsi}</div>', html)
html = re.sub(r'id="mi-turnover">.*?</div>', f'id="mi-turnover">{turnover}</div>', html)

# Build Gainers
mi_gainers_html = ""
for i in range(min(3, len(gainers))):
    mi_gainers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{gainers[i][0]}</span> <span style="color:var(--gain)">{gainers[i][4]}</span></div>\n        '
gainers_full = f'<!-- GAINERS_START -->\n      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n        {mi_gainers_html.strip()}\n      </div>\n      <!-- GAINERS_END -->'

# Replace strictly between START and END comments
html = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', gainers_full, html, flags=re.DOTALL)

# Build Losers
mi_losers_html = ""
for i in range(min(3, len(losers))):
    mi_losers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{losers[i][0]}</span> <span style="color:var(--loss)">{losers[i][4]}</span></div>\n        '
if not mi_losers_html:
    mi_losers_html = '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>None</span> <span style="color:var(--loss)">0.0%</span></div>\n        '
losers_full = f'<!-- LOSERS_START -->\n      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n        {mi_losers_html.strip()}\n      </div>\n      <!-- LOSERS_END -->'

# Replace strictly between START and END comments
html = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', losers_full, html, flags=re.DOTALL)

# Archive Teaser
html = re.sub(r'<div class="archive-date">.*?</div>', f'<div class="archive-date">31 Aug<br/>2026</div>', html)
html = re.sub(r'<div class="archive-content-title">.*?</div>', f'<div class="archive-content-title">{wrap_title}</div>', html)
html = re.sub(r'<div class="archive-content-excerpt">.*?</div>', f'<div class="archive-content-excerpt">{intro_p[:130]}...</div>', html)
html = re.sub(r'<a class="archive-row" href="/dse-wrap-[0-9\-]+">', f'<a class="archive-row" href="/dse-wrap-2026-08-31">', html)

# Bump cache to trigger browser reload
html = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260901_31aug_mi_fix', html)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("market-intelligence.html fixed")
