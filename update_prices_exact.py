import re
import json

data_map = {
    'AFRIPRISE': {'price': '740', 'change': '0.0%', 'vol': '113,786', 'turnover': '84,326,730'},
    'CRDB': {'price': '2,810', 'change': '0.0%', 'vol': '668,525', 'turnover': '1,877,118,960'},
    'DCB': {'price': '445', 'change': '0.0%', 'vol': '18,793', 'turnover': '8,329,210'},
    'DSE': {'price': '6,070', 'change': '-2.7%', 'vol': '1,456', 'turnover': '8,897,140'},
    'JHL': {'price': '8,700', 'change': '+0.6%', 'vol': '60,097', 'turnover': '522,843,900'},
    'KCB': {'price': '2,190', 'change': '0.0%', 'vol': '1,827,795', 'turnover': '3,840,902,520'},
    'MBP': {'price': '2,080', 'change': '+1.0%', 'vol': '8,561', 'turnover': '17,778,650'},
    'MCB': {'price': '375', 'change': '-3.8%', 'vol': '137,000', 'turnover': '51,252,585'},
    'MKCB': {'price': '3,660', 'change': '+1.7%', 'vol': '1,746', 'turnover': '6,384,930'},
    'MUCOBA': {'price': '415', 'change': '+2.5%', 'vol': '2,506', 'turnover': '1,048,090'},
    'NICO': {'price': '3,700', 'change': '+0.8%', 'vol': '9,579', 'turnover': '35,426,960'},
    'NMB': {'price': '2,130', 'change': '+2.9%', 'vol': '843,542', 'turnover': '1,772,719,520'},
    'PAL': {'price': '310', 'change': '+3.3%', 'vol': '20,690', 'turnover': '6,378,230'},
    'SWIS': {'price': '2,600', 'change': '-1.5%', 'vol': '5,240', 'turnover': '13,644,090'},
    'TBL': {'price': '9,880', 'change': '-0.7%', 'vol': '3,361', 'turnover': '33,200,680'},
    'TCC': {'price': '13,400', 'change': '0.0%', 'vol': '2,499', 'turnover': '33,482,930'},
    'TCCL': {'price': '3,910', 'change': '+0.3%', 'vol': '410,838', 'turnover': '1,482,394,130'},
    'TOL': {'price': '1,770', 'change': '-1.1%', 'vol': '505,307', 'turnover': '639,397,790'},
    'TPCC': {'price': '5,700', 'change': '-0.2%', 'vol': '7,007', 'turnover': '39,921,680'},
    'TTP': {'price': '430', 'change': '+2.4%', 'vol': '339', 'turnover': '145,370'},
    'VODA': {'price': '1,260', 'change': '+3.3%', 'vol': '1,066,989', 'turnover': '1,284,338,310'}
}

with open('current-prices.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update date
html = re.sub(r'Friday 18th September 2026', 'Monday 21st September 2026', html)

# Update the table rows
# A row looks roughly like:
# <tr>
#   <td><div class="company-name-cell"><strong>AFRIPRISE</strong>...</div></td>
#   <td class="text-right">740</td>
#   <td class="text-right change-neutral" style="font-weight: 400;">0.0%</td>
#   <td class="text-right">100</td>
#   <td class="text-right">74,000</td>
# </tr>

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# Update KCB, NMB, TCCL, TOL, VODA in the pre-arranged board? KCB, VODA, TOL, TCCL, NMB were block trades. 
# Wait, I shouldn't add to pre-arranged unless told, but the subagent updated them. The prompt says: "update the current prices with details from Current Prices 21 September 2026.docx keep the same format and do not add or change anything else". The table in docx doesn't mention "Pre-arranged board" so maybe I just update the main table.

tbody = soup.find('tbody')
if tbody:
    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 5:
            strong = tds[0].find('strong')
            if strong:
                ticker = strong.text.strip()
                if ticker in data_map:
                    # Update Price
                    tds[1].string = data_map[ticker]['price']
                    
                    # Update Change
                    change_val = data_map[ticker]['change']
                    tds[2].string = change_val.replace('-', '&minus;')
                    
                    # Update classes for change
                    if '-' in change_val:
                        tds[2]['class'] = ['text-right', 'change-negative']
                    elif '+' in change_val:
                        tds[2]['class'] = ['text-right', 'change-positive']
                    else:
                        tds[2]['class'] = ['text-right', 'change-neutral']
                        
                    # Update Volume
                    tds[3].string = data_map[ticker]['vol']
                    
                    # Update Turnover
                    tds[4].string = data_map[ticker]['turnover']

# Save
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(str(soup).replace('&amp;minus;', '&minus;'))

print("Updated current-prices.html")
