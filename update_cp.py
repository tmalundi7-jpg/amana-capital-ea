import re

def update_cp():
    with open('current-prices.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Date
    html = html.replace('End-of-Day, Monday, 7th September 2026', 'End-of-Day, Monday, 14th September 2026')

    # Data to replace
    # Format: Ticker: (Price, Change, Vol, Turnover)
    new_data = {
        'AFRIPRISE': ('605', '0.0%', '130,817', '78,927,740'),
        'CRDB': ('2,980', '+2.8%', '760,252', '2,265,085,000'),
        'DCB': ('450', '+1.1%', '146,603', '66,045,800'),
        'DSE': ('6,390', '0.0%', '2,930', '18,707,160'),
        'JATU': ('270', '0.0%', '100', '27,000'),
        'KCB': ('2,200', '+3.8%', '10,565', '23,241,480'),
        'MBP': ('2,100', '+3.4%', '6,454', '13,565,910'),
        'MCB': ('395', '+1.3%', '27,593', '10,845,330'),
        'MKCB': ('3,680', '-1.3%', '10,276', '37,844,980'),
        'MUCOBA': ('440', '-4.3%', '240', '105,775'),
        'NICO': ('3,790', '-2.1%', '26,479', '100,482,560'),
        'NMB': ('2,180', '-0.5%', '1,536,134', '3,364,604,200'),
        'PAL': ('305', '0.0%', '44,095', '13,524,805'),
        'SWIS': ('2,680', '-1.5%', '6,289', '16,852,660'),
        'TBL': ('9,990', '-0.1%', '4,665', '46,599,320'),
        'TCC': ('13,500', '+0.4%', '2,177', '29,358,660'),
        'TCCL': ('3,800', '-4.3%', '16,336', '62,046,950'),
        'TOL': ('1,860', '+5.7%', '5,346', '9,931,820'),
        'TPCC': ('5,750', '-0.3%', '13,220', '76,015,500'),
        'TTP': ('425', '-5.6%', '2,522', '1,078,775'),
        'VODA': ('1,110', '0.0%', '81,530', '90,661,330')
    }

    # Iterate through HTML and replace the table row for each ticker
    for ticker, (price, change, vol, turn) in new_data.items():
        # Match the row:
        # <td><strong>TICKER</strong></td> ...
        # <td class="text-right"><strong>PRICE</strong></td>
        # <td class="text-right change-positive"><strong>CHANGE</strong></td>
        # <td class="text-right">VOL</td>
        
        # We need a robust regex to replace the values in the row for 	icker
        # Using a pattern that captures the structure and replaces the contents of the last 4 <td>s
        
        pattern = r'(<td><strong>' + ticker + r'</strong></td>\s*<td>.*?</td>\s*<td.*?>.*?</td>\s*)<td class="text-right"><strong>.*?</strong></td>\s*(<td class="text-right[^>]*>)<strong>.*?</strong></td>\s*<td class="text-right">.*?</td>'
        
        def replacer(match):
            prefix = match.group(1)
            td_change_class = match.group(2) # original class
            
            # Determine new class based on change
            new_td_change_class = '<td class="text-right ">'
            if '+' in change:
                new_td_change_class = '<td class="text-right change-positive">'
            elif '-' in change:
                new_td_change_class = '<td class="text-right change-negative">'
                
            return f'{prefix}<td class="text-right"><strong>{price}</strong></td>\n                                  {new_td_change_class}<strong>{change}</strong></td>\n                                  <td class="text-right">{vol}</td>'

        new_html = re.sub(pattern, replacer, html, count=1, flags=re.DOTALL)
        if new_html == html:
            print(f"FAIL: Ticker {ticker} not replaced properly")
        html = new_html

    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("current-prices.html updated.")

update_cp()
