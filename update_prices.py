import re
date_str = 'End-of-Day, Wednesday 16th September 2026'
block_trades_html = '''
    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">900,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">TBL</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">307,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">VODA</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">1,550,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">IEACLC-ETF</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">215,469 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
      </div>
'''
table_data = [
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
    ('VODA', 'Vodacom Tanzania', 'Commercial Services', '1,190', '+3.5%', '1,886,813', '2,259,310,470')
]
tbody_html = '<tbody>\n'
for t, c, s, p, ch, v, to in table_data:
    if '+' in ch:
        sty = 'color: var(--green); font-weight: 600;'
    elif '-' in ch:
        sty = 'color: var(--red); font-weight: 600;'
    else:
        sty = 'color: var(--mist); opacity: 0.7;'
    tbody_html += f'                              <tr>\n                                  <td><strong>{t}</strong></td>\n                                  <td>{c}</td>\n                                  <td style=\"color: #9A9490;\">{s}</td>\n                                  <td class=\"text-right\"><strong>{p}</strong></td>\n                                  <td class=\"text-right\" style=\"{sty}\">{ch}</td>\n                                  <td class=\"text-right\">{v}</td>\n                                  <td class=\"text-right\"><strong>{to}</strong></td>\n                              </tr>\n'
tbody_html += '                          </tbody>'
with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'<p style=\"color: var\(--gold\); font-size: 1\.1rem;\">.*?</p>', f'<p style=\"color: var(--gold); font-size: 1.1rem;\">{date_str}</p>', content)
content = re.sub(r'<div style=\"display: flex; gap: 1rem; flex-wrap: wrap;\">.*?</div>\s*</div>\s*</div>\s*<div style=\"overflow-x: auto', block_trades_html + '\n    </div>\n  </div>\n  <div style=\"overflow-x: auto', content, flags=re.DOTALL)
content = re.sub(r'<tbody>.*?</tbody>', tbody_html, content, flags=re.DOTALL)
new_no_trades = '<p style=\"margin-bottom: 0.75rem;\"><em>Change (%) calculated from opening to closing price. Counters with no trades (EABL, JHL, KA, NMG, SWALA, USL, YETU) are omitted.</em></p>'
content = re.sub(r'<p style=\"margin-bottom: 0\.75rem;\"><em>Change \(\%\) calculated from opening to closing price\. Counters with no trades.*?</em></p>', new_no_trades, content, flags=re.DOTALL)
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated current-prices.html')
