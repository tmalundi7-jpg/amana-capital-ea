import re

def insert_jatu_and_update_footnote():
    with open('current-prices.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Insert JATU after DSE row
    dse_row_pattern = r'(<td><strong>DSE</strong></td>.*?<td class="text-right">.*?</td>\s*</tr>)'
    jatu_row = '''
                            <tr>
                                <td><strong>JATU</strong></td>
                                <td>Jatu Plc</td>
                                <td style="color: var(--mist);">Commercial Services</td>
                                <td class="text-right"><strong>270</strong></td>
                                <td class="text-right "><strong>0.0%</strong></td>
                                <td class="text-right">100</td>
                            </tr>'''
    
    html = re.sub(dse_row_pattern, r'\1' + jatu_row, html, count=1, flags=re.DOTALL)

    # Update footnote
    html = html.replace('(EABL, JATU, JHL, KA, NMG, SWALA, USL, YETU)', '(EABL, JHL, KA, NMG, SWALA, USL, YETU)')
    
    # Wait, the block trades in 14 Sep footnote:
    # 07 Sep had: NMB: 5.2 million shares, CRDB: 1.1 million shares, TPCC: 300,000 shares
    # 14 Sep has: NMB: 500,000 shares, IEACLC-ETF: 175,000 shares
    
    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("JATU and footnote updated.")

insert_jatu_and_update_footnote()
