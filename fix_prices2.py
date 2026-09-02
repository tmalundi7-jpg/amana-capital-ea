import docx
import re
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# 1. Parse Current Prices DOCX
doc = docx.Document('C:\\Users\\tmalu\\Documents\\Current Prices 02 September 2026.docx')
table_data = []
for i, row in enumerate(doc.tables[0].rows):
    if i == 0: continue # header
    cells = [c.text.replace('\n', ' ').strip() for c in row.cells]
    ticker, company, sector, price, change, vol, turnover = cells
    
    # Replace en-dash with minus
    change = change.replace('\u2013', '-')
    
    table_data.append((ticker, company, sector, price, change, vol, turnover))

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 3. Rebuild the table
tbody_start = c.find('<tbody>')
tbody_end = c.find('</tbody>')
if tbody_start != -1 and tbody_end != -1:
    tbody = '<tbody>\n'
    for t in table_data:
        ticker, company, sector, price, change, vol, turnover = t
        if '+' in change:
            chg_html = f'<td style="color: var(--gain); font-weight: 600;">{change}</td>'
        elif '-' in change:
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
print("Successfully fixed current-prices.html")
