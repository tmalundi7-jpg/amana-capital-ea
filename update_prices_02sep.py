import docx
import re
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# 1. Parse Current Prices DOCX
doc = docx.Document('C:\\Users\\tmalu\\Documents\\Current Prices 02 September 2026.docx')
table_data = []
total_vol = 0
for i, row in enumerate(doc.tables[0].rows):
    if i == 0: continue # header
    cells = [c.text.replace('\n', ' ').strip() for c in row.cells]
    ticker, company, sector, price, change, vol, turnover = cells
    vol_int = int(vol.replace(',', ''))
    total_vol += vol_int
    change = change.replace('', '-')
    table_data.append((ticker, company, sector, price, change, vol, turnover))

vol_str = f"{total_vol:,}"
turnover_str = "TZS 4.01 bn"
date_str = "02 Sep 2026"
subtitle_date = "2 September 2026"

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 2. Update the snapshot bar
c = re.sub(r'(<div class="snapshot-value">)4,395\.95(</div>)', r'\g<1>4,415.49\g<2>', c) # DSEI
c = re.sub(r'(<div class="snapshot-value">)9,758\.17(</div>)', r'\g<1>9,699.66\g<2>', c) # TSI
c = re.sub(r'(<div class="snapshot-value" data-format-type="bn" data-tzs-value="[0-9]+">)TZS [0-9.]+ bn(</div>)', r'<div class="snapshot-value" data-format-type="bn" data-tzs-value="4010000000">TZS 4.01 bn</div>', c) # Turnover
c = re.sub(r'(<div class="snapshot-value">)[0-9,]+(</div>)', r'\g<1>' + vol_str + r'\g<2>', c, count=1) # Volume - wait, count=1 might replace DSEI if the regex matches!
# Safer Volume replacement:
c = re.sub(r'(<div class="snapshot-label">Total Volume.*?<div class="snapshot-value">)[0-9,]+(</div>)', r'\g<1>' + vol_str + r'\g<2>', c, flags=re.DOTALL)
c = re.sub(r'(<div class="snapshot-label">Date.*?<div class="snapshot-value">).*?(</div>)', r'\g<1>' + date_str + r'\g<2>', c, flags=re.DOTALL)

# Update subtitle
c = re.sub(r'(<p style="text-align: center; color: rgba\(11,29,58,0\.6\); font-size: 0\.95rem; margin-top: -0\.5rem; margin-bottom: 2rem;">).*?(</p>)', r'\g<1>Closing prices for ' + subtitle_date + r'\g<2>', c)

# 3. Rebuild the table
tbody_start = c.find('<tbody>')
tbody_end = c.find('</tbody>')
if tbody_start != -1 and tbody_end != -1:
    tbody = '<tbody>\n'
    for t in table_data:
        ticker, company, sector, price, change, vol, turnover = t
        if change.startswith('+'):
            chg_html = f'<td style="color: var(--gain); font-weight: 600;">{change}</td>'
        elif change.startswith('-'):
            chg_html = f'<td style="color: var(--loss); font-weight: 600;">{change}</td>'
        else:
            chg_html = f'<td style="color: #666; font-weight: 600;">{change}</td>'
            
        tbody += f'''<tr>
<td><strong>{ticker}</strong></td>
<td>{company}</td>
<td>{sector}</td>
<td style="font-weight: 600;">{price}</td>
{chg_html}
<td>{vol}</td>
<td>{turnover}</td>
</tr>\n'''
    tbody += '</tbody>'
    c = c[:tbody_start] + tbody + c[tbody_end+8:]

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Successfully updated current-prices.html")
