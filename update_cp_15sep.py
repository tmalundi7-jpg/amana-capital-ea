import os
import re
import json

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

with open('15_sep_prices.txt', 'r', encoding='utf-16', errors='ignore') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

start_idx = -1
for i, l in enumerate(lines):
    if 'Sector' in l and i+3 < len(lines) and 'Volume' in lines[i+3]:
        start_idx = i + 5
        break

rows = []
if start_idx != -1:
    i = start_idx
    while i < len(lines):
        if lines[i].startswith('Block trades') or lines[i].startswith('Change (%)'):
            break
        if i + 6 < len(lines):
            ticker = lines[i].strip().replace('\ufffd', '')
            company = lines[i+1].strip()
            sector = lines[i+2].strip()
            price = lines[i+3].strip()
            change = lines[i+4].strip()
            vol = lines[i+5].strip()
            turnover = lines[i+6].strip()
            
            rows.append({
                'ticker': ticker,
                'company': company,
                'sector': sector,
                'price': price,
                'change': change,
                'vol': vol,
                'turnover': turnover
            })
            i += 7
        else:
            break

with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp_html = f.read()

cp_html = cp_html.replace('End-of-Day, Monday 14th September 2026', 'End-of-Day, Tuesday 15th September 2026')
cp_html = cp_html.replace('End-of-Day, Monday, 14th September 2026', 'End-of-Day, Tuesday, 15th September 2026')

html_rows = []
for r in rows:
    change_class = ""
    c_val = r['change'].replace('%', '').replace('+', '').replace('\ufffd', '-').replace('?"', '-').replace('\u2013', '-').replace('\u2014', '-')
    
    try:
        cf = float(c_val)
        if cf > 0:
            change_class = " change-positive"
        elif cf < 0:
            change_class = " change-negative"
    except:
        pass

    change_text = r['change'].replace('\ufffd', '-').replace('?"', '-').replace('\u2013', '-').replace('\u2014', '-')
    
    row_html = f'''                            <tr>
                                <td><strong>{r['ticker']}</strong></td>
                                <td>{r['company']}</td>
                                <td style="color: var(--mist);">{r['sector']}</td>
                                <td class="text-right"><strong>{r['price']}</strong></td>
                                <td class="text-right{change_class}"><strong>{change_text}</strong></td>
                                <td class="text-right">{r['vol']}</td>
                                <td class="text-right">{r['turnover']}</td>
                            </tr>'''
    html_rows.append(row_html)

new_tbody = '<tbody>\n' + '\n'.join(html_rows) + '\n                        </tbody>'
cp_html = re.sub(r'<tbody>.*?</tbody>', new_tbody, cp_html, flags=re.DOTALL)

bt_lines = []
bt_start = False
for l in lines:
    if l.startswith('Block trades'):
        bt_start = True
        continue
    if bt_start:
        if l.startswith('Change (%)'):
            break
        if l:
            bt_lines.append(l)

new_bt_inner = ''
if bt_lines:
    for l in bt_lines:
        if ':' in l:
            ticker, shares = l.split(':', 1)
            ticker = ticker.replace('\ufffd', '').strip()
            shares = shares.replace('shares', '').replace('\ufffd', '').strip()
            
            new_bt_inner += f'''\n    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">{ticker}</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">{shares} <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>'''
new_bt_inner += '\n  '

start_bt = cp_html.find('<div style="display: flex; gap: 1rem; flex-wrap: wrap;">')
if start_bt != -1:
    end_bt = cp_html.find('</div>\n</div>\n\n<div class="table-responsive">', start_bt)
    if end_bt != -1:
        end_inner = cp_html.rfind('</div>', start_bt, end_bt)
        cp_html = cp_html[:start_bt + len('<div style="display: flex; gap: 1rem; flex-wrap: wrap;">')] + new_bt_inner + cp_html[end_inner:]

disclaimer_start = cp_html.find('Counters with no trades (')
if disclaimer_start != -1:
    disclaimer_end = cp_html.find(')', disclaimer_start)
    for l in lines:
        if l.startswith('Change (%)'):
            m = re.search(r'Counters with no trades \((.*?)\)', l)
            if m:
                omitted = m.group(1)
                cp_html = cp_html[:disclaimer_start] + f'Counters with no trades ({omitted}' + cp_html[disclaimer_end:]

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp_html)
print("Updated current-prices.html")
