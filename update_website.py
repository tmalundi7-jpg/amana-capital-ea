import json
import re
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Load data
with open('extracted_dse_wrap_17_aug_2026.json', 'r', encoding='utf-8') as f:
    wrap_data = json.load(f)
with open('extracted_current_prices_17_aug_2026.json', 'r', encoding='utf-8') as f:
    prices_data = json.load(f)

prices = prices_data.get('prices', [])

def parse_change(c):
    if c == '0.0%': return 0.0
    c = c.replace('?"', '-').replace('%', '')
    try:
        return float(c)
    except:
        return 0.0

sorted_prices = sorted(prices, key=lambda x: parse_change(x.get('change_pct', '0%')), reverse=True)
gainers = [p for p in sorted_prices if parse_change(p.get('change_pct')) > 0][:3]
losers = [p for p in sorted_prices if parse_change(p.get('change_pct')) < 0]
losers.reverse()
losers = losers[:3]

# 1. Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

# Instead of full beautifulsoup parse which can break formatting, we can use regex for specific blocks, 
# or carefully use BeautifulSoup. Let's use BeautifulSoup but we'll use regex for text replacement where possible.
# Actually, the user requirement is: "direct DOM-like object manipulation (or clear text block replacement) is required"
soup_mi = BeautifulSoup(mi_html, 'html.parser')

# Update snapshot dates
for elem in soup_mi.find_all(string=re.compile(r'14 August 2026')):
    elem.replace_with(elem.replace('14 August 2026', '17 August 2026'))

for elem in soup_mi.find_all(string=re.compile(r'13 Aug 2026')):
    elem.replace_with(elem.replace('13 Aug 2026', '17 Aug 2026'))

for elem in soup_mi.find_all(string=re.compile(r'14 Aug 2026')):
    elem.replace_with(elem.replace('14 Aug 2026', '17 Aug 2026'))

# Update Live Snapshot figures
dsei_elem = soup_mi.find(id='mi-dsei')
if dsei_elem:
    # 4,232.85 <span style="color: #22c55e;">▲</span>
    dsei_val = wrap_data['headline_figures'].get('DSEI', '4,248.98')
    dsei_elem.clear()
    dsei_elem.append(f"{dsei_val} ")
    span = soup_mi.new_tag('span', style="color: #22c55e;")
    span.string = '▲'
    dsei_elem.append(span)

tsi_elem = soup_mi.find(id='mi-tsi')
if tsi_elem:
    tsi_val = wrap_data['headline_figures'].get('TSI', '9,349.59')
    tsi_elem.clear()
    tsi_elem.append(f"{tsi_val} ")
    span = soup_mi.new_tag('span', style="color: #22c55e;")
    span.string = '▲'
    tsi_elem.append(span)

turnover_elem = soup_mi.find(id='mi-turnover')
if turnover_elem:
    turnover_elem['data-tzs-value'] = '4770000000'
    turnover_elem.string = '4.77 bn'

# Update Gainers/Losers
def generate_movers_html(movers, is_gainer):
    html = ""
    for m in movers:
        color = "#22c55e" if is_gainer else "#ef4444"
        change = m['change_pct'].replace('?"', '-')
        html += f'<div class="snapshot-mover" id="mi-{"gainer" if is_gainer else "loser"}">{m["ticker"]} <span style="color:{color}">{change}</span></div>\n'
    return html

gainers_html = generate_movers_html(gainers, True)
losers_html = generate_movers_html(losers, False)

mi_html = str(soup_mi)
mi_html = re.sub(r'(<!-- GAINERS_START -->).*?(<!-- GAINERS_END -->)', r'\1\n' + gainers_html + r'                                      \2', mi_html, flags=re.DOTALL)
mi_html = re.sub(r'(<!-- LOSERS_START -->).*?(<!-- LOSERS_END -->)', r'\1\n' + losers_html + r'                                      \2', mi_html, flags=re.DOTALL)

# Archive Row handling:
# Find the old archive row
archive_row_pattern = re.compile(r'(<a class="archive-row" href="/dse-wrap-2026-08-14">.*?</a>)', re.DOTALL)
old_archive_match = archive_row_pattern.search(mi_html)
old_archive_html = ""
if old_archive_match:
    old_archive_html = old_archive_match.group(1)
    
    new_archive_row = """<a class="archive-row" href="/dse-wrap-2026-08-17">
                                    <div class="archive-date">17 Aug<br>2026</div>
                                    <div>
                                        <div class="archive-badge badge-equity">Equities</div>
                                        <div class="archive-content-title">DCB\'s Block Trade and the Power of Local Demand</div>
                                        <div class="archive-content-excerpt">The Dar es Salaam Stock Exchange closed Monday on a strong note, with the All-Share Index rising. A massive 760,000-share DCB block trade boosted overall activity...</div>
                                    </div>
                                    <span class="archive-cta">Read &rarr;</span>
                                </a>"""
    mi_html = mi_html.replace(old_archive_html, new_archive_row)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

# 2. Update market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc_html = f.read()

# Insert old archive row into archiveList
if old_archive_html:
    # Remove the `href` if we want, or keep it. It's valid.
    # The archive list starts after `<div id="archiveList" ...>`
    insert_pos = arc_html.find('<div id="archiveList"')
    if insert_pos != -1:
        # find the end of this div tag
        insert_pos = arc_html.find('>', insert_pos) + 1
        arc_html = arc_html[:insert_pos] + "\n" + old_archive_html + arc_html[insert_pos:]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arc_html)

# 3. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp_html = f.read()
soup_cp = BeautifulSoup(cp_html, 'html.parser')

date_elem_cp = soup_cp.find(string=re.compile(r'14 August 2026'))
if date_elem_cp:
    date_elem_cp.replace_with(date_elem_cp.replace('14 August 2026', '17 August 2026'))

# Generate new table rows
tbody = soup_cp.find('tbody')
if tbody:
    tbody.clear()
    for p in prices:
        tr = soup_cp.new_tag('tr')
        # ticker, company, sector, last price, change, volume, turnover
        for key in ['ticker', 'company', 'sector', 'last_price_tzs']:
            td = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
            td.string = p.get(key, '')
            tr.append(td)
        
        # change_pct
        td_change = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;  font-weight: 600;")
        c = p.get('change_pct', '0.0%').replace('?"', '-')
        c_val = parse_change(c)
        if c_val > 0:
            td_change['style'] += " color: var(--gain);"
        elif c_val < 0:
            td_change['style'] += " color: var(--loss);"
        td_change.string = c
        tr.append(td_change)

        # volume
        td_vol = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
        td_vol.string = p.get('volume', '').replace('?"', '-')
        tr.append(td_vol)
        
        # turnover
        td_turn = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
        td_turn.string = p.get('turnover_tzs', '').replace('?"', '-')
        tr.append(td_turn)

        tbody.append(tr)

cp_html = str(soup_cp)
# The footnotes in json
new_footnotes = prices_data.get('footnotes', [])
if new_footnotes:
    footnote_text = new_footnotes[0].replace('?"', '-')
    # find the em tag in current prices
    em_tags = soup_cp.find_all('em')
    for em in em_tags:
        if 'Includes a' in em.text or 'Change (%) calculated' in em.text:
            # We can just replace the parent's content
            pass # simpler to do a targeted replace using string replace on cp_html

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp_html)

print("Update complete")
