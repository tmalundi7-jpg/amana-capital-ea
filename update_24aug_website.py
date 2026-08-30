import json
import re
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# Load parsed data
with open('parsed_wrap_24aug.json', 'r', encoding='utf-8') as f:
    wrap_data = json.load(f)
with open('parsed_prices_24aug.json', 'r', encoding='utf-8') as f:
    prices = json.load(f)

# 1. Generate dse-wrap-2026-08-24.html
def generate_html(data, template_path, output_path):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    html_out = template.render(**data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f"Generated {output_path}")

generate_html(wrap_data, "wrap_template.html", "dse-wrap-2026-08-24.html")

# Calculate Gainers and Losers for Heatmap from Prices
def parse_change(c):
    if c == '0.0%': return 0.0
    c = c.replace('?', '-').replace('–', '-').replace('%', '').replace('+', '')
    try:
        return float(c)
    except:
        return 0.0

sorted_prices = sorted(prices, key=lambda x: parse_change(x.get('change_pct', '0%')), reverse=True)
gainers = [p for p in sorted_prices if parse_change(p.get('change_pct')) > 0][:3]
losers = [p for p in sorted_prices if parse_change(p.get('change_pct')) < 0]
losers.reverse()
losers = losers[:3]

# 2. Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

soup_mi = BeautifulSoup(mi_html, 'html.parser')

# Update Dates
for elem in soup_mi.find_all(string=re.compile(r'17 August 2026')):
    elem.replace_with(elem.replace('17 August 2026', '24 August 2026'))
for elem in soup_mi.find_all(string=re.compile(r'21 August 2026')):
    elem.replace_with(elem.replace('21 August 2026', '24 August 2026'))
for elem in soup_mi.find_all(string=re.compile(r'17 Aug 2026')):
    elem.replace_with(elem.replace('17 Aug 2026', '24 Aug 2026'))
for elem in soup_mi.find_all(string=re.compile(r'21 Aug 2026')):
    elem.replace_with(elem.replace('21 Aug 2026', '24 Aug 2026'))
for elem in soup_mi.find_all(string=re.compile(r'14 Aug 2026')):
    elem.replace_with(elem.replace('14 Aug 2026', '24 Aug 2026'))

# Update Live Snapshot figures
dsei_elem = soup_mi.find(id='mi-dsei')
if dsei_elem:
    dsei_val = wrap_data['snapshot'].get('dsei', '4,232.85')
    dsei_elem.clear()
    dsei_elem.append(f"{dsei_val} ")
    span = soup_mi.new_tag('span', style="color: #ef4444;") # Assuming down, will just set neutral or figure it out from previous value, but the script didn't specify. The word doc has a red arrow for DSEI.
    span.string = '▼'
    dsei_elem.append(span)

tsi_elem = soup_mi.find(id='mi-tsi')
if tsi_elem:
    tsi_val = wrap_data['snapshot'].get('tsi', '9,349.59')
    tsi_elem.clear()
    tsi_elem.append(f"{tsi_val} ")
    span = soup_mi.new_tag('span', style="color: #22c55e;")
    span.string = '▲'
    tsi_elem.append(span)

turnover_elem = soup_mi.find(id='mi-turnover')
if turnover_elem:
    turnover_elem.string = wrap_data['snapshot'].get('turnover', 'TZS 4.77bn').replace('TZS ', '').replace('m', ' m').replace('bn', ' bn')

# Update Gainers/Losers
def generate_movers_html(movers, is_gainer):
    html = ""
    for m in movers:
        color = "#22c55e" if is_gainer else "#ef4444"
        change = m['change_pct'].replace('?', '-').replace('–', '-')
        if is_gainer and not change.startswith('+'):
            change = "+" + change
        html += f'<div class="snapshot-mover" id="mi-{"gainer" if is_gainer else "loser"}">{m["ticker"]} <span style="color:{color}">{change}</span></div>\n'
    return html

gainers_html = generate_movers_html(gainers, True)
losers_html = generate_movers_html(losers, False)

mi_html = str(soup_mi)
mi_html = re.sub(r'(<!-- GAINERS_START -->).*?(<!-- GAINERS_END -->)', r'\1\n' + gainers_html + r'                                      \2', mi_html, flags=re.DOTALL)
mi_html = re.sub(r'(<!-- LOSERS_START -->).*?(<!-- LOSERS_END -->)', r'\1\n' + losers_html + r'                                      \2', mi_html, flags=re.DOTALL)

# Archive Row handling:
# Find the old archive row (from 21 Aug presumably)
archive_row_pattern = re.compile(r'(<a class="archive-row" href="/dse-wrap-2026-08-21.*?</a>)', re.DOTALL)
old_archive_match = archive_row_pattern.search(mi_html)
old_archive_html = ""
if old_archive_match:
    old_archive_html = old_archive_match.group(1)
    
new_archive_row = f"""<a class="archive-row" href="/dse-wrap-2026-08-24">
                                    <div class="archive-date">24 Aug<br>2026</div>
                                    <div>
                                        <div class="archive-badge badge-equity">Equities</div>
                                        <div class="archive-content-title">{wrap_data['headline']}</div>
                                        <div class="archive-content-excerpt">{wrap_data['introduction_paragraphs'][0][:150]}...</div>
                                    </div>
                                    <span class="archive-cta">Read &rarr;</span>
                                </a>"""
# Replace old with new in market-intelligence.html
if old_archive_html:
    mi_html = mi_html.replace(old_archive_html, new_archive_row)
else:
    # If 21st doesn't exist, we fallback to 17th or whichever was the latest
    fallback_pattern = re.compile(r'(<a class="archive-row" href="/dse-wrap-2026-08-17.*?</a>)', re.DOTALL)
    fallback_match = fallback_pattern.search(mi_html)
    if fallback_match:
        old_archive_html = fallback_match.group(1)
        mi_html = mi_html.replace(old_archive_html, new_archive_row)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)
print("Updated market-intelligence.html")

# 3. Update market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc_html = f.read()

if old_archive_html:
    insert_pos = arc_html.find('<div id="archiveList"')
    if insert_pos != -1:
        insert_pos = arc_html.find('>', insert_pos) + 1
        arc_html = arc_html[:insert_pos] + "\n" + old_archive_html + arc_html[insert_pos:]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arc_html)
print("Updated market-intelligence-archive.html")

# 4. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp_html = f.read()
soup_cp = BeautifulSoup(cp_html, 'html.parser')

date_elem_cp = soup_cp.find(string=re.compile(r'17 August 2026'))
if date_elem_cp:
    date_elem_cp.replace_with(date_elem_cp.replace('17 August 2026', '24 August 2026'))
for elem in soup_cp.find_all(string=re.compile(r'21 August 2026')):
    elem.replace_with(elem.replace('21 August 2026', '24 August 2026'))

tbody = soup_cp.find('tbody')
if tbody:
    tbody.clear()
    for p in prices:
        tr = soup_cp.new_tag('tr')
        for key in ['ticker', 'company', 'sector', 'last_price_tzs']:
            td = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
            td.string = str(p.get(key, ''))
            tr.append(td)
        
        td_change = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;  font-weight: 600;")
        c = p.get('change_pct', '0.0%').replace('?', '-').replace('–', '-')
        c_val = parse_change(c)
        if c_val > 0:
            td_change['style'] += " color: var(--gain);"
            if not c.startswith('+'):
                c = '+' + c
        elif c_val < 0:
            td_change['style'] += " color: var(--loss);"
        td_change.string = c
        tr.append(td_change)

        td_vol = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
        td_vol.string = str(p.get('volume', '')).replace('?', '-').replace('–', '-')
        tr.append(td_vol)
        
        td_turn = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
        td_turn.string = str(p.get('turnover_tzs', '')).replace('?', '-').replace('–', '-')
        tr.append(td_turn)

        tbody.append(tr)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(str(soup_cp))
print("Updated current-prices.html")
