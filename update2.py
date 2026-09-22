import re

# 2. Update market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc = f.read()

# We need to add 18 Sep 2026 into the archive.
# Wait, the current archive has 17 Sep as the top row. Let's insert 18 Sep above it.
new_row = """<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">18 Sep 2026</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Friday, 18th September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange closed the week with a session of quiet resilience. Equity turnover fell 72% to TZS 4.30 billion from Thursday's block-heavy TZS 15.39 billion, and the All-Share In...</div></div>
<a href="/dse-wrap-2026-09-18" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>
"""

# Find the insertion point (before 17 Sep)
arc = arc.replace('<div class="arc-row">\n<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">17 Sep 2026</div>', 
                  new_row + '<div class="arc-row">\n<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">17 Sep 2026</div>')

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arc)

print("market-intelligence-archive.html updated")


# 3. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    prices = f.read()

prices = prices.replace('Friday 18th September 2026', 'Monday 21st September 2026')
# For block trades, daily wrap says:
# "KCB (1,800,000 shares), VODA (1,000,000 shares), TOL (500,000 shares), TCCL (400,000 shares), and NMB (364,304 shares)" and IEACLC-ETF 1,915,953
# Wait, the block trades currently in current-prices.html:
# NMB: 5,451,880 -> 364,304
# TBL: 307,000 -> 0 (hidden)
# VODA: 1,550,000 -> 1,000,000
# IEACLC-ETF: 215,469 -> 1,915,953
# Let's just do a regex replace or manual string replacement for the block trades.
# Actually, the user says "update the current prices using Current Prices 21 September 2026.docx".
# Current Prices docx block trades: "Block trades on the pre-arranged board today: KCB:  1,800,000 shares NMB:  364,304 shares TCCL:  400,000 shares TOL:  500,000 shares VODA:  1,000,000 shares IEACLC-ETF:  1,915,953 shares (ETF)"
# In the HTML, there are 4 blocks shown. I'll just change the values and names for 4 of them. Or maybe add more. 
# But "Do not add any new section, row, label, card, table, text, note, ticker, disclaimer, or value that does not appear in the source DOCX files... Do not delete or rename anything unless it is explicitly part of the update. ... Keep the existing website format exactly the same."
# Let's replace the first 4 blocks with the top 4 by volume (KCB, IEACLC-ETF, VODA, TOL), and leave the rest or make them visible.
# Currently they have visibility:hidden except NMB. 
# Let's just update the table rows.

# Current Prices docx table data:
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
import re

for ticker, (price, change, vol, turnover) in table_data.items():
    # Find the row for this ticker. 
    # Example: <td>NMB</td>\n <td>NMB Bank</td>\n <td style="color: #9A9490;">Banks & Finance</td>\n <td class="text-right">2,070</td>
    # The change column has a class like change-negative, change-positive, change-neutral.
    
    if '+' in change:
        cls = 'change-positive'
    elif '-' in change or '&minus;' in change:
        cls = 'change-negative'
    else:
        cls = 'change-neutral'
        
    # Replace price
    prices = re.sub(fr'(<td>{ticker}</td>.*?<td class="text-right">)[\d,]+(</td>)', fr'\g<1>{price}\g<2>', prices, flags=re.DOTALL)
    # Replace change
    prices = re.sub(fr'(<td>{ticker}</td>.*?<td class="text-right change-)[^"]+(" style="font-weight: 400;">)[^<]+(</td>)', fr'\g<1>{cls}\g<2>{change}\g<3>', prices, flags=re.DOTALL)
    # Replace vol and turnover - careful, they are the next two text-right tds
    # We can do it by finding the whole block
    pattern = fr'(<td>{ticker}</td>\s*<td>.*?</td>\s*<td.*?>.*?</td>\s*<td class="text-right">)[\d,]+(</td>\s*<td class="text-right change-[^"]+" style="font-weight: 400;">[^<]+</td>\s*<td class="text-right">)[\d,]+(</td>\s*<td class="text-right">)[\d,]+(</td>)'
    
    match = re.search(pattern, prices, re.DOTALL)
    if match:
        prices = prices[:match.start(3)] + vol + match.group(3) + turnover + match.group(4) + prices[match.end(4):]

# Update block trades (NMB, KCB, VODA, IEACLC-ETF)
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
      </div>"""
prices = re.sub(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>', blocks_html + '\n  </div>', prices, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(prices)
print("current-prices.html updated")


# 4. Update script.js & script.min.js for heatmap
heatmap_changes = {
    'NMB': 2.9,
    'TBL': -0.7,
    'CRDB': 0.0,
    'VODA': 3.3,
    'TPCC': -0.2,
    'NICO': 0.8,
    'KCB': 0.0,
    'TCCL': 0.3,
    'TOL': -1.1,
    'SWIS': -1.5,
    'DCB': 0.0,
    'MBP': 1.0,
    'MCB': -3.8,
    'NMG': 0.0
}

for js_file in ['script.js', 'script.min.js']:
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    for symbol, change in heatmap_changes.items():
        # find { symbol: 'NMB', marketCap: 2675, change: 4.95 }
        js_content = re.sub(fr"(symbol:\s*'{symbol}',\s*marketCap:\s*[\d\.]+,\s*change:\s*)[-\d\.]+", fr"\g<1>{change}", js_content)
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
print("script.js updated")
