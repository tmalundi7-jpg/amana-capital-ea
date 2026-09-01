import json
import re

with open('extracted_01sep.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']['tables'][0][1:]

losers = []
for p in prices:
    val = p[4].replace('\ufffd', '-').replace('?"', '-').replace('–', '-')
    if '-' in val and val != '-0.0%':
        losers.append((p[0], val))

losers = sorted(losers, key=lambda x: float(x[1].replace('-','').replace('%','')), reverse=True)

# 1. Update index.html Top Losers
losers_html = ""
for i in range(min(3, len(losers))):
    losers_html += f'<span>{losers[i][0]} <span style="color:var(--loss)">{losers[i][1]}</span></span>\n            '

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'id="home-losers".*?>.*?</div>', f'id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">\n            {losers_html.strip()}\n          </div>', c, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

# 2. Update MI Top Losers
mi_losers_html = ""
for i in range(min(3, len(losers))):
    mi_losers_html += f'<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>{losers[i][0]}</span> <span style="color:var(--loss)">{losers[i][1]}</span></div>\n        '

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', f'<!-- LOSERS_START -->\n      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n        {mi_losers_html.strip()}\n      </div>\n      <!-- LOSERS_END -->', c, flags=re.DOTALL)
with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

# 3. Update Current Prices classes
with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace any td with en-dash to have class="loss"
c = re.sub(r'<td class="">(–[\d\.]+%)</td>', r'<td class="loss">\1</td>', c)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)
