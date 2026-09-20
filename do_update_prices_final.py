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

tbody_match = re.search(r'(<tbody>)(.*?)(</tbody>)', content, re.DOTALL)
pre_tbody = content[:tbody_match.start(2)]
tbody_content = tbody_match.group(2)
post_tbody = content[tbody_match.end(2):]

row_matches = list(re.finditer(r'(<tr.*?>)(.*?)(</tr>)', tbody_content, re.DOTALL))

new_tbody = ''
last_end = 0

for m in row_matches:
    new_tbody += tbody_content[last_end:m.start()]
    last_end = m.end()
    
    tr_open = m.group(1)
    tr_inner = m.group(2)
    tr_close = m.group(3)
    
    ticker_match = re.search(r'<td.*?>.*?([A-Z]{3,5})(?:<|&nbsp;|\s|$)', tr_inner, re.DOTALL)
    if not ticker_match:
        new_tbody += tr_open + tr_inner + tr_close
        continue
        
    ticker = ticker_match.group(1)
    
    if ticker in prices:
        tr_open = tr_open.replace('display: none;', '')
        
        data = prices[ticker]
        last_price = data[3]
        change_raw = data[4]
        volume = data[5]
        turnover = data[6]
        
        # Determine class based on raw text
        # If it has '+', positive
        # If it has a digit and NO '+', and it's not '0.0%', it must be negative.
        if '0.0%' in change_raw:
            c_class = 'change-neutral'
            change_val = '0.0%'
        elif '+' in change_raw:
            c_class = 'change-positive'
            change_val = change_raw # Keep the plus
        else:
            c_class = 'change-negative'
            # Force it to have &minus;
            # Extract just the number parts
            num = re.search(r'[\d\.]+', change_raw).group(0)
            change_val = f'&minus;{num}%'
        
        tds = list(re.finditer(r'(<td.*?>)(.*?)(</td>)', tr_inner, re.DOTALL))
        if len(tds) >= 7:
            td3_inner = tds[3].group(2)
            td4_inner = tds[4].group(2)
            td5_inner = tds[5].group(2)
            td6_inner = tds[6].group(2)
            
            # Replace Last Price
            new_td3_inner = re.sub(r'>[\d,]+<', f'>{last_price}<', td3_inner)
            if '>' not in new_td3_inner: new_td3_inner = last_price
            
            # Replace Change Class and Value
            td4_inner = re.sub(r'change-(positive|negative|neutral)', c_class, td4_inner)
            new_td4_inner = re.sub(r'>[^<]+<', f'>{change_val}<', td4_inner)
            if '>' not in new_td4_inner: new_td4_inner = change_val
            
            # Replace Volume
            new_td5_inner = re.sub(r'>[\d,]+<', f'>{volume}<', td5_inner)
            if '>' not in new_td5_inner: new_td5_inner = volume
            
            # Replace Turnover
            new_td6_inner = re.sub(r'(<span>)([\d,]+)(</span>)', fr'\g<1>{turnover}\g<3>', td6_inner)
            if '<span>' not in new_td6_inner:
                new_td6_inner = re.sub(r'>[\d,]+<', f'>{turnover}<', td6_inner)
                if '>' not in new_td6_inner: new_td6_inner = turnover
            
            new_tr_inner = ''
            t_last = 0
            for i, td_m in enumerate(tds):
                new_tr_inner += tr_inner[t_last:td_m.start()]
                if i == 3: new_tr_inner += td_m.group(1) + new_td3_inner + td_m.group(3)
                elif i == 4: new_tr_inner += td_m.group(1) + new_td4_inner + td_m.group(3)
                elif i == 5: new_tr_inner += td_m.group(1) + new_td5_inner + td_m.group(3)
                elif i == 6: new_tr_inner += td_m.group(1) + new_td6_inner + td_m.group(3)
                else: new_tr_inner += td_m.group(0)
                t_last = td_m.end()
            new_tr_inner += tr_inner[t_last:]
            tr_inner = new_tr_inner
            
    else:
        if 'display: none' not in tr_open:
            if 'style="' in tr_open: tr_open = tr_open.replace('style="', 'style="display: none; ')
            else: tr_open = tr_open.replace('<tr', '<tr style="display: none;"')
                
    new_tbody += tr_open + tr_inner + tr_close

new_tbody += tbody_content[last_end:]
new_content = pre_tbody + new_tbody + post_tbody

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated current-prices.html correctly")

