
# Update current-prices.html for 16 Sep 2026
# Source data from 16_sep_prices.txt

import re

prices_data = [
    ('AFRIPRISE', 'African Pride', 'Commercial Services', '600', '-0.8%', '394,056', '237,313,280'),
    ('CRDB', 'CRDB Bank', 'Banks & Finance', '2,920', '-0.7%', '306,119', '892,753,770'),
    ('DCB', 'Dar es Salaam Community Bank', 'Banks & Finance', '445', '+2.3%', '21,964', '9,810,095'),
    ('DSE', 'Dar es Salaam Stock Exchange', 'Commercial Services', '6,350', '-0.5%', '252', '1,601,950'),
    ('JATU', 'Jatu Plc', 'Commercial Services', '270', '0.0%', '4', '1,000'),
    ('KCB', 'KCB Group (cross-listed)', 'Banks & Finance', '2,180', '-1.8%', '34,500', '75,146,680'),
    ('MBP', 'Maendeleo Bank', 'Banks & Finance', '2,070', '-1.0%', '9,698', '20,033,400'),
    ('MCB', 'Mwanga Community Bank', 'Banks & Finance', '395', '+2.6%', '29,526', '11,721,915'),
    ('MKCB', 'Mkamba Commercial Bank', 'Banks & Finance', '3,650', '0.0%', '5,408', '19,736,680'),
    ('MUCOBA', 'Mucoba Bank', 'Banks & Finance', '410', '-6.8%', '2,100', '862,600'),
    ('NICO', 'NICO Holdings', 'Banks & Finance', '3,730', '-1.1%', '11,217', '41,861,050'),
    ('NMB', 'NMB Bank', 'Banks & Finance', '2,150', '-1.4%', '1,560,725', '3,457,830,210'),
    ('PAL', 'Pal Holdings', 'Industrials', '315', '+3.3%', '1,975', '619,695'),
    ('SWIS', 'Swissport Tanzania', 'Commercial Services', '2,570', '-3.0%', '946', '2,438,240'),
    ('TBL', 'Tanzania Breweries', 'Industrials', '9,970', '0.0%', '307,875', '3,078,723,150'),
    ('TCC', 'Tanga Cement', 'Industrials', '13,450', '+0.7%', '982', '13,213,900'),
    ('TCCL', 'Tanzania Cigarette Company', 'Industrials', '3,700', '-5.1%', '7,619', '28,242,700'),
    ('TOL', 'TOL Gases', 'Industrials', '1,820', '-4.2%', '4,053', '7,353,420'),
    ('TPCC', 'Tanga Portland Cement', 'Industrials', '5,710', '-0.7%', '3,384', '19,337,860'),
    ('TTP', 'Tatepa Public Limited Company', 'Commercial Services', '420', '-2.3%', '310', '130,200'),
    ('VODA', 'Vodacom Tanzania', 'Commercial Services', '1,190', '+3.5%', '1,886,813', '2,259,310,470'),
]

block_trades = [
    ('NMB', '900,000'),
    ('TBL', '307,000'),
    ('VODA', '1,550,000'),
    ('IEACLC-ETF', '215,469'),
]

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update date in subtitle
content = re.sub(
    r'End-of-Day,.*?</p>',
    'End-of-Day, Wednesday, 16th September 2026</p>',
    content
)
print('Date updated')

# 2. Update tbody rows
rows_html = ''
for ticker, company, sector, price, change, vol, turnover in prices_data:
    if change.startswith('+'):
        change_class = ' change-positive'
    elif change.startswith('-'):
        change_class = ' change-negative'
    else:
        change_class = ''
    rows_html += (
        f'                            <tr>\n'
        f'                                <td><strong>{ticker}</strong></td>\n'
        f'                                <td>{company}</td>\n'
        f'                                <td style="color: #9A9490;">{sector}</td>\n'
        f'                                <td class="text-right"><strong>{price}</strong></td>\n'
        f'                                <td class="text-right{change_class}"><strong>{change}</strong></td>\n'
        f'                                <td class="text-right">{vol}</td>\n'
        f'                                <td class="text-right">{turnover}</td>\n'
        f'                            </tr>\n'
    )

content = re.sub(
    r'<tbody>.*?</tbody>',
    f'<tbody>\n{rows_html}                        </tbody>',
    content,
    flags=re.DOTALL
)
print('Table rows updated')

# 3. Update block trades section
# Build new block trades HTML in same card style as existing
block_cards = ''
for ticker, shares in block_trades:
    block_cards += (
        f'    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">\n'
        f'      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">{ticker}</div>\n'
        f'      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">{shares} <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>\n'
        f'    </div>\n'
    )

new_block_container = (
    '  <div class="block-trades-container" style="display: flex; gap: 1rem; flex-wrap: wrap;">\n'
    + block_cards +
    '  </div>'
)

# Replace the block-trades-container
content = re.sub(
    r'<div class="block-trades-container".*?</div>\s*</div>',
    new_block_container + '\n</div>',
    content,
    flags=re.DOTALL
)
print('Block trades updated')

# Final verification
checks = {
    'Date 16th Sep': '16th September 2026' in content,
    'NMB block trade 900,000': '900,000' in content,
    'VODA +3.5%': '+3.5%' in content,
    'TCCL -5.1%': '-5.1%' in content,
    'CRDB price 2,920': '2,920' in content,
    'NMB price 2,150': '2,150' in content,
}
print('\n=== current-prices.html VERIFICATION ===')
all_ok = True
for k, v in checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: all_ok = False
    print(f'  [{status}] {k}')

if all_ok:
    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('\ncurrent-prices.html SAVED.')
else:
    print('\nSome checks FAILED. File NOT saved.')
