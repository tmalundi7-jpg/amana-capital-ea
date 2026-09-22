import re

data_map = {
    'AFRIPRISE': {'price': '740', 'change': '0.0%', 'vol': '113,786', 'turnover': '84,326,730', 'class': 'change-neutral'},
    'CRDB': {'price': '2,810', 'change': '0.0%', 'vol': '668,525', 'turnover': '1,877,118,960', 'class': 'change-neutral'},
    'DCB': {'price': '445', 'change': '0.0%', 'vol': '18,793', 'turnover': '8,329,210', 'class': 'change-neutral'},
    'DSE': {'price': '6,070', 'change': '&minus;2.7%', 'vol': '1,456', 'turnover': '8,897,140', 'class': 'change-negative'},
    'JHL': {'price': '8,700', 'change': '+0.6%', 'vol': '60,097', 'turnover': '522,843,900', 'class': 'change-positive'},
    'KCB': {'price': '2,190', 'change': '0.0%', 'vol': '1,827,795', 'turnover': '3,840,902,520', 'class': 'change-neutral'},
    'MBP': {'price': '2,080', 'change': '+1.0%', 'vol': '8,561', 'turnover': '17,778,650', 'class': 'change-positive'},
    'MCB': {'price': '375', 'change': '&minus;3.8%', 'vol': '137,000', 'turnover': '51,252,585', 'class': 'change-negative'},
    'MKCB': {'price': '3,660', 'change': '+1.7%', 'vol': '1,746', 'turnover': '6,384,930', 'class': 'change-positive'},
    'MUCOBA': {'price': '415', 'change': '+2.5%', 'vol': '2,506', 'turnover': '1,048,090', 'class': 'change-positive'},
    'NICO': {'price': '3,700', 'change': '+0.8%', 'vol': '9,579', 'turnover': '35,426,960', 'class': 'change-positive'},
    'NMB': {'price': '2,130', 'change': '+2.9%', 'vol': '843,542', 'turnover': '1,772,719,520', 'class': 'change-positive'},
    'PAL': {'price': '310', 'change': '+3.3%', 'vol': '20,690', 'turnover': '6,378,230', 'class': 'change-positive'},
    'SWIS': {'price': '2,600', 'change': '&minus;1.5%', 'vol': '5,240', 'turnover': '13,644,090', 'class': 'change-negative'},
    'TBL': {'price': '9,880', 'change': '&minus;0.7%', 'vol': '3,361', 'turnover': '33,200,680', 'class': 'change-negative'},
    'TCC': {'price': '13,400', 'change': '0.0%', 'vol': '2,499', 'turnover': '33,482,930', 'class': 'change-neutral'},
    'TCCL': {'price': '3,910', 'change': '+0.3%', 'vol': '410,838', 'turnover': '1,482,394,130', 'class': 'change-positive'},
    'TOL': {'price': '1,770', 'change': '&minus;1.1%', 'vol': '505,307', 'turnover': '639,397,790', 'class': 'change-negative'},
    'TPCC': {'price': '5,700', 'change': '&minus;0.2%', 'vol': '7,007', 'turnover': '39,921,680', 'class': 'change-negative'},
    'TTP': {'price': '430', 'change': '+2.4%', 'vol': '339', 'turnover': '145,370', 'class': 'change-positive'},
    'VODA': {'price': '1,260', 'change': '+3.3%', 'vol': '1,066,989', 'turnover': '1,284,338,310', 'class': 'change-positive'}
}

with open('current-prices.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Check date
    if 'Friday 18th September 2026' in line:
        new_lines[-1] = line.replace('Friday 18th September 2026', 'Monday 21st September 2026')
    
    # Main board ticker
    match_main = re.search(r'<td>([A-Z]+)</td>', line)
    # Pre-arranged board ticker
    match_pre = re.search(r'<strong>([A-Z]+)</strong>', line)
    
    ticker = None
    if match_main:
        ticker = match_main.group(1)
    elif match_pre:
        ticker = match_pre.group(1)
        
    if ticker and ticker in data_map:
        # We found the ticker row.
        # Find the next 4 td with class="text-right"
        td_count = 0
        while td_count < 4:
            i += 1
            if i >= len(lines): break
            next_line = lines[i]
            
            if '<td class="text-right' in next_line:
                td_count += 1
                if td_count == 1: # Price
                    next_line = re.sub(r'>([^<]+)</td>', f'>{data_map[ticker]["price"]}</td>', next_line)
                elif td_count == 2: # Change
                    next_line = re.sub(r'change-\w+', data_map[ticker]['class'], next_line)
                    next_line = re.sub(r'>([^<]+)</td>', f'>{data_map[ticker]["change"]}</td>', next_line)
                elif td_count == 3: # Vol
                    next_line = re.sub(r'>([^<]+)</td>', f'>{data_map[ticker]["vol"]}</td>', next_line)
                elif td_count == 4: # Turnover
                    next_line = re.sub(r'>([^<]+)</td>', f'>{data_map[ticker]["turnover"]}</td>', next_line)
                    
            new_lines.append(next_line)
            
    i += 1

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Updated via strict parsing!")
