
import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

prices_data = [
    ('AFRIPRISE', 'African Pride', 'Commercial Services', '600', '–0.8%', '394,056', '237,313,280'),
    ('CRDB', 'CRDB Bank', 'Banks &amp; Finance', '2,920', '–0.7%', '306,119', '892,753,770'),
    ('DCB', 'Dar es Salaam Community Bank', 'Banks &amp; Finance', '445', '+2.3%', '21,964', '9,810,095'),
    ('DSE', 'Dar es Salaam Stock Exchange', 'Commercial Services', '6,350', '–0.5%', '252', '1,601,950'),
    ('JATU', 'Jatu Plc', 'Commercial Services', '270', '0.0%', '4', '1,000'),
    ('KCB', 'KCB Group (cross-listed)', 'Banks &amp; Finance', '2,180', '–1.8%', '34,500', '75,146,680'),
    ('MBP', 'Maendeleo Bank', 'Banks &amp; Finance', '2,070', '–1.0%', '9,698', '20,033,400'),
    ('MCB', 'Mwanga Community Bank', 'Banks &amp; Finance', '395', '+2.6%', '29,526', '11,721,915'),
    ('MKCB', 'Mkamba Commercial Bank', 'Banks &amp; Finance', '3,650', '0.0%', '5,408', '19,736,680'),
    ('MUCOBA', 'Mucoba Bank', 'Banks &amp; Finance', '410', '–6.8%', '2,100', '862,600'),
    ('NICO', 'NICO Holdings', 'Banks &amp; Finance', '3,730', '–1.1%', '11,217', '41,861,050'),
    ('NMB', 'NMB Bank', 'Banks &amp; Finance', '2,150', '–1.4%', '1,560,725', '3,457,830,210'),
    ('PAL', 'Pal Holdings', 'Industrials', '315', '+3.3%', '1,975', '619,695'),
    ('SWIS', 'Swissport Tanzania', 'Commercial Services', '2,570', '–3.0%', '946', '2,438,240'),
    ('TBL', 'Tanzania Breweries', 'Industrials', '9,970', '0.0%', '307,875', '3,078,723,150'),
    ('TCC', 'Tanga Cement', 'Industrials', '13,450', '+0.7%', '982', '13,213,900'),
    ('TCCL', 'Tanzania Cigarette Company', 'Industrials', '3,700', '–5.1%', '7,619', '28,242,700'),
    ('TOL', 'TOL Gases', 'Industrials', '1,820', '–4.2%', '4,053', '7,353,420'),
    ('TPCC', 'Tanga Portland Cement', 'Industrials', '5,710', '–0.7%', '3,384', '19,337,860'),
    ('TTP', 'Tatepa Public Limited Company', 'Commercial Services', '420', '–2.3%', '310', '130,200'),
    ('VODA', 'Vodacom Tanzania', 'Commercial Services', '1,190', '+3.5%', '1,886,813', '2,259,310,470'),
]

block_trades = [
    ('NMB', '900,000'),
    ('TBL', '307,000'),
    ('VODA', '1,550,000'),
    ('IEACLC-ETF', '215,469'),
]

# 1. Update date
content = re.sub(
    r'(End-of-Day, )([^<]+)',
    r'\g<1>Wednesday, 16th September 2026',
    content
)

# 2. Update tbody rows
rows_html = ''
for ticker, company, sector, price, change, vol, turnover in prices_data:
    if '+' in change:
        change_class = ' change-positive'
    elif '–' in change:
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

# 3. Update block trades section
block_cards_html = ''
for ticker, shares in block_trades:
    block_cards_html += (
        f'      <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">\n'
        f'        <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">{ticker}</div>\n'
        f'        <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">{shares} <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>\n'
        f'      </div>\n'
    )

new_flex_block = (
    '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">\n'
    + block_cards_html +
    '    </div>'
)

# Let's do a substring replace
start_str = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
start_idx = content.find(start_str)
end_str = '<div class="table-responsive">'
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    # the end of the flex box is </div>\n  </div>\n  \n  <div class="table-responsive">
    # we want to replace from start_str up to right before `</div>\n  </div>\n  \n  <div class="table-responsive">`
    # Actually, we can find the `</div>\n  </div>\n  \n  ` part exactly.
    flex_end_idx = content.rfind('</div>\n  </div>', start_idx, end_idx)
    content = content[:start_idx] + new_flex_block + content[flex_end_idx:]
    
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('current-prices.html updated successfully with correct layout.')
