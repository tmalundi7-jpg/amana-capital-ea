import re
from docx import Document

doc = Document(r'C:\Users\tmalu\Documents\Current Prices 18 September 2026.docx')
prices = {}
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows[1:]):
        cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        prices[cells[0]] = cells

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Thursday 17th September 2026', 'Friday 18th September 2026')
content = content.replace('NMB: 5,450,000 shares', 'CRDB: 380,000 shares')

# Split content by <tbody>...</tbody> to isolate the table
tbody_match = re.search(r'(<tbody>)(.*?)(</tbody>)', content, re.DOTALL)
if not tbody_match:
    print("Could not find tbody")
    exit(1)

pre_tbody = content[:tbody_match.start(2)]
tbody_content = tbody_match.group(2)
post_tbody = content[tbody_match.end(2):]

# Split tbody into rows
row_matches = list(re.finditer(r'(<tr.*?>)(.*?)(</tr>)', tbody_content, re.DOTALL))

new_tbody = ''
last_end = 0

for m in row_matches:
    new_tbody += tbody_content[last_end:m.start()]
    last_end = m.end()
    
    tr_open = m.group(1)
    tr_inner = m.group(2)
    tr_close = m.group(3)
    
    # Find ticker
    ticker_match = re.search(r'<td.*?>.*?([A-Z]{3,5})(?:<|&nbsp;|\s|$)', tr_inner, re.DOTALL)
    if not ticker_match:
        new_tbody += tr_open + tr_inner + tr_close
        continue
        
    ticker = ticker_match.group(1)
    
    if ticker in prices:
        # Show row
        tr_open = tr_open.replace('display: none;', '')
        
        data = prices[ticker]
        last_price = data[3]
        change = data[4].replace('-', '&minus;').replace('−', '&minus;')
        volume = data[5]
        turnover = data[6]
        
        # Parse tds
        tds = list(re.finditer(r'(<td.*?>)(.*?)(</td>)', tr_inner, re.DOTALL))
        if len(tds) >= 7:
            # 3 = Last Price
            td3_inner = tds[3].group(2)
            # 4 = Change
            td4_inner = tds[4].group(2)
            # 5 = Volume
            td5_inner = tds[5].group(2)
            # 6 = Turnover
            td6_inner = tds[6].group(2)
            
            # Replace Last Price (just numbers)
            new_td3_inner = re.sub(r'>[\d,]+<', f'>{last_price}<', td3_inner)
            if '>' not in new_td3_inner:
                new_td3_inner = last_price
            
            # Replace Change
            # Update class first
            if '+' in change:
                td4_inner = re.sub(r'change-[a-z]+', 'change-positive', td4_inner)
            elif '&minus;' in change:
                td4_inner = re.sub(r'change-[a-z]+', 'change-negative', td4_inner)
            else:
                td4_inner = re.sub(r'change-[a-z]+', 'change-neutral', td4_inner)
                
            # Replace value
            change_val = change if change != '0.0%' else '0.0%'
            new_td4_inner = re.sub(r'>[^<]+<', f'>{change_val}<', td4_inner)
            if '>' not in new_td4_inner:
                new_td4_inner = change_val
            
            # Replace Volume
            new_td5_inner = re.sub(r'>[\d,]+<', f'>{volume}<', td5_inner)
            if '>' not in new_td5_inner:
                new_td5_inner = volume
            
            # Replace Turnover
            new_td6_inner = re.sub(r'(<span>)([\d,]+)(</span>)', fr'\g<1>{turnover}\g<3>', td6_inner)
            if '<span>' not in new_td6_inner:
                new_td6_inner = re.sub(r'>[\d,]+<', f'>{turnover}<', td6_inner)
                if '>' not in new_td6_inner:
                    new_td6_inner = turnover
            
            # Reconstruct tr_inner
            new_tr_inner = ''
            t_last = 0
            for i, td_m in enumerate(tds):
                new_tr_inner += tr_inner[t_last:td_m.start()]
                if i == 3:
                    new_tr_inner += td_m.group(1) + new_td3_inner + td_m.group(3)
                elif i == 4:
                    new_tr_inner += td_m.group(1) + new_td4_inner + td_m.group(3)
                elif i == 5:
                    new_tr_inner += td_m.group(1) + new_td5_inner + td_m.group(3)
                elif i == 6:
                    new_tr_inner += td_m.group(1) + new_td6_inner + td_m.group(3)
                else:
                    new_tr_inner += td_m.group(0)
                t_last = td_m.end()
            new_tr_inner += tr_inner[t_last:]
            tr_inner = new_tr_inner
            
    else:
        # Hide row
        if 'display: none' not in tr_open:
            if 'style="' in tr_open:
                tr_open = tr_open.replace('style="', 'style="display: none; ')
            else:
                tr_open = tr_open.replace('<tr', '<tr style="display: none;"')
                
    new_tbody += tr_open + tr_inner + tr_close

new_tbody += tbody_content[last_end:]
new_content = pre_tbody + new_tbody + post_tbody

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated current-prices.html flawlessly")

