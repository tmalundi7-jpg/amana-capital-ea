import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    prices = f.read()

prices = prices.replace('Friday 18th September 2026', 'Monday 21st September 2026')

table_data = {
    'AFRIPRISE': ['740', '0.0%', '113,786', '84,326,730'],
    'CRDB': ['2,810', '0.0%', '668,525', '1,877,118,960'],
    'DCB': ['445', '0.0%', '18,793', '8,329,210'],
    'DSE': ['6,070', '&minus;2.7%', '1,456', '8,897,140'],
    'JHL': ['8,700', '+0.6%', '60,097', '522,843,900'],
    'KCB': ['2,190', '0.0%', '1,827,795', '3,840,902,520'],
    'MBP': ['2,080', '+1.0%', '8,561', '17,778,650'],
    'MCB': ['375', '&minus;3.8%', '137,000', '51,252,585'],
    'MKCB': ['3,660', '+1.7%', '1,746', '6,384,930'],
    'MUCOBA': ['415', '+2.5%', '2,506', '1,048,090'],
    'NICO': ['3,700', '+0.8%', '9,579', '35,426,960'],
    'NMB': ['2,130', '+2.9%', '843,542', '1,772,719,520'],
    'PAL': ['310', '+3.3%', '20,690', '6,378,230'],
    'SWIS': ['2,600', '&minus;1.5%', '5,240', '13,644,090'],
    'TBL': ['9,880', '&minus;0.7%', '3,361', '33,200,680'],
    'TCC': ['13,400', '0.0%', '2,499', '33,482,930'],
    'TCCL': ['3,910', '+0.3%', '410,838', '1,482,394,130'],
    'TOL': ['1,770', '&minus;1.1%', '505,307', '639,397,790'],
    'TPCC': ['5,700', '&minus;0.2%', '7,007', '39,921,680'],
    'TTP': ['430', '+2.4%', '339', '145,370'],
    'VODA': ['1,260', '+3.3%', '1,066,989', '1,284,338,310'],
}

for ticker, (price, change, vol, turnover) in table_data.items():
    if '+' in change:
        cls = 'change-positive'
    elif '-' in change or '&minus;' in change:
        cls = 'change-negative'
    else:
        cls = 'change-neutral'
        
    # We want to replace the text inside the specific td elements.
    # The structure is:
    # <td>TICKER</td>
    # ...
    # <td class="text-right">PRICE</td>
    # <td class="text-right change-something" style="font-weight: 400;">CHANGE</td>
    # <td class="text-right">VOL</td>
    # <td class="text-right">TURNOVER</td>
    
    # 1. Price
    prices = re.sub(fr'(<td>{ticker}</td>\s*<td>.*?</td>\s*<td.*?>.*?</td>\s*<td class="text-right">)[\d,]+(</td>)', fr'\g<1>{price}\g<2>', prices, flags=re.DOTALL)
    # 2. Change (and class)
    prices = re.sub(fr'(<td>{ticker}</td>.*?<td class="text-right )change-[a-z]+(" style="font-weight: 400;">)[^<]+(</td>)', fr'\g<1>{cls}\g<2>{change}\g<3>', prices, flags=re.DOTALL)
    
    # 3. Vol and Turnover
    pattern = fr'(<td>{ticker}</td>\s*<td>.*?</td>\s*<td.*?>.*?</td>\s*<td class="text-right">[\d,]+</td>\s*<td class="text-right change-[a-z]+" style="font-weight: 400;">[^<]+</td>\s*<td class="text-right">)[\d,]+(</td>\s*<td class="text-right">)[\d,]+(</td>)'
    prices = re.sub(pattern, fr'\g<1>{vol}\g<2>{turnover}\g<3>', prices, flags=re.DOTALL)

blocks_html = """  <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">IEACLC-ETF</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">1,915,953 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">KCB</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">1,800,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">VODA</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">1,000,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">TOL</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">500,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">TCCL</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">400,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">364,304 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
      </div>"""
prices = re.sub(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>', blocks_html + '\n  </div>', prices, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(prices)
