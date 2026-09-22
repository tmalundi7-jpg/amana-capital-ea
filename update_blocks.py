import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the pre-arranged board
# Current pre-arranged board is:
# <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
#           <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
#             ...
#         </div>

# We will replace everything inside the <div style="display: flex; gap: 1rem; flex-wrap: wrap;"> up to the closing </div></div> before the <div class="table-responsive">

# Let's find it.
pre_board_start = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
pre_board_idx = content.find(pre_board_start)
end_pre_board_idx = content.find('<div class="table-responsive">', pre_board_idx)

# Find the closing tag for the flex div. The flex div closes just before the table-responsive div.
pre_board_block = content[pre_board_idx:end_pre_board_idx]

# Let's generate the new pre-arranged board
block_trades = [
    ('KCB', '1,800,000'),
    ('NMB', '364,304'),
    ('TCCL', '400,000'),
    ('TOL', '500,000'),
    ('VODA', '1,000,000'),
    ('IEACLC-ETF', '1,915,953')
]

new_pre_board = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">\n'
for ticker, shares in block_trades:
    new_pre_board += f'''          <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
            <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.25rem;">{ticker}</div>
            <div style="font-size: 1.6rem; color: #0A1628; font-weight: 400;">{shares} <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
          </div>\n'''
new_pre_board += '        </div>\n    </div>\n    \n    '

content = content[:pre_board_idx] + new_pre_board + content[end_pre_board_idx:]

# 2. Insert JHL into the table. It goes between DSE and JATU.
jhl_html = '''                                <tr>
                                    <td>JHL</td>
                                    <td>Jubilee Holdings</td>
                                    <td style="color: #9A9490;">Banks & Finance</td>
                                    <td class="text-right">8,700</td>
                                    <td class="text-right change-positive" style="font-weight: 400;">+0.6%</td>
                                    <td class="text-right">60,097</td>
                                    <td class="text-right">522,843,900</td>
                                </tr>
'''
# Find DSE row closing
dse_row_end = content.find('8,897,140</td>\n                                </tr>')
dse_row_end += len('8,897,140</td>\n                                </tr>\n')
content = content[:dse_row_end] + jhl_html + content[dse_row_end:]

# 3. Update the omission note
old_note = 'Counters with no trades (EABL, JATU, JHL, KA, NMG, SWALA, USL, YETU) are omitted.'
new_note = 'Counters with no trades (EABL, JATU, KA, NMG, SWALA, USL, YETU) are omitted.'
content = content.replace(old_note, new_note)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated current-prices.html successfully")
