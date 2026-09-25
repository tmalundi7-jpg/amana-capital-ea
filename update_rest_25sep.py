import re

# 1. market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arch = f.read()

new_arc_row = """
<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">24 Sep 2026</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Thursday, 24th September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange had a quiet day on the surface. Equity turnover fell 34% to TZS 2.73 billion, dropping below TZS 3 billion for the first time in weeks. Yet both the DSEI and TSI closed at new post-split highs...</div></div>
<a href="/dse-wrap-2026-09-24" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>
"""
arch = arch.replace('<div id="archiveList" style="display: flex; flex-direction: column; gap: 1rem;">', '<div id="archiveList" style="display: flex; flex-direction: column; gap: 1rem;">\n' + new_arc_row.strip() + '\n')
arch = re.sub(r'script\.min\.js\?v=20260924a', 'script.min.js?v=20260925a', arch)
arch = re.sub(r'script\.js\?v=20260924a', 'script.js?v=20260925a', arch)

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arch)
print("Updated archive")

# 2. current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp = f.read()

cp = cp.replace('Thursday 24th September 2026', 'Friday 25th September 2026')
cp = re.sub(r'script\.min\.js\?v=20260924a', 'script.min.js?v=20260925a', cp)
cp = re.sub(r'script\.js\?v=20260924a', 'script.js?v=20260925a', cp)

# Update Pre-Arranged board block
pre_arr = """
<div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(11,29,58,0.1); padding-bottom: 0.5rem;">
<div style="font-weight: 700; color: var(--navy);">NMB</div>
<div style="font-weight: 600; color: var(--gold);">429,000 <span style="font-size: 0.75rem; color: rgba(11,29,58,0.6); font-weight: 500;">shares</span></div>
</div>
"""
cp = re.sub(r'<div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba\(11,29,58,0\.1\); padding-bottom: 0\.5rem;">.*?</div>\s*</div>', pre_arr.strip(), cp, flags=re.DOTALL)

# Update Table Rows
rows_data = [
    ("AFRIPRISE", "African Pride", "Commercial Services", "780", "+0.6%", "90,355", "70,636,660"),
    ("CRDB", "CRDB Bank", "Banks & Finance", "2,940", "+2.4%", "431,081", "1,266,096,490"),
    ("DCB", "Dar es Salaam Community Bank", "Banks & Finance", "420", "-4.5%", "106,635", "44,991,550"),
    ("DSE", "Dar es Salaam Stock Exchange", "Commercial Services", "6,200", "+0.5%", "1,259", "7,802,200"),
    ("KCB", "KCB Group (cross-listed)", "Banks & Finance", "2,200", "0.0%", "2,386", "5,238,990"),
    ("MBP", "Maendeleo Bank", "Banks & Finance", "2,150", "+2.9%", "5,467", "11,730,660"),
    ("MCB", "Mwanga Community Bank", "Banks & Finance", "375", "-1.3%", "59,796", "22,552,210"),
    ("MKCB", "Mkamba Commercial Bank", "Banks & Finance", "3,660", "+1.4%", "3,670", "13,427,400"),
    ("MUCOBA", "Mucoba Bank", "Banks & Finance", "450", "+11.1%", "356", "157,830"),
    ("NICO", "NICO Holdings", "Banks & Finance", "3,610", "-3.5%", "31,545", "113,918,460"),
    ("NMB", "NMB Bank", "Banks & Finance", "2,130", "0.0%", "859,775", "1,902,613,960"),
    ("PAL", "Pal Holdings", "Industrials", "305", "0.0%", "8,398", "2,554,175"),
    ("SWIS", "Swissport Tanzania", "Commercial Services", "2,560", "+1.2%", "5,836", "14,951,060"),
    ("TBL", "Tanzania Breweries", "Industrials", "9,800", "0.0%", "1,795", "17,586,000"),
    ("TCC", "Tanga Cement", "Industrials", "13,200", "+0.2%", "888", "11,777,310"),
    ("TCCL", "Tanzania Cigarette Company", "Industrials", "3,810", "-2.8%", "5,670", "21,566,240"),
    ("TOL", "TOL Gases", "Industrials", "1,810", "+1.1%", "2,764", "4,998,840"),
    ("TPCC", "Tanga Portland Cement", "Industrials", "5,700", "+1.8%", "1,253", "7,142,100"),
    ("TTP", "Tatepa Public Limited Company", "Commercial Services", "425", "0.0%", "125", "53,650"),
    ("VODA", "Vodacom Tanzania", "Commercial Services", "1,280", "-0.8%", "189,462", "241,987,740")
]

table_rows_html = ""
for rd in rows_data:
    color_style = ""
    if "+" in rd[4]:
        color_style = ' style="color: var(--green);"'
    elif "-" in rd[4]:
        color_style = ' style="color: var(--red);"'
        
    table_rows_html += f"""
<tr>
<td style="font-weight: 700; color: var(--navy);">{rd[0]}</td>
<td style="color: rgba(11,29,58,0.7);">{rd[1]}</td>
<td style="color: rgba(11,29,58,0.5); font-size: 0.8rem;">{rd[2]}</td>
<td style="font-weight: 600; text-align: right;">{rd[3]}</td>
<td{color_style} style="font-weight: 600; text-align: right;">{rd[4]}</td>
<td style="text-align: right; color: rgba(11,29,58,0.7);">{rd[5]}</td>
<td style="text-align: right; font-weight: 500; color: var(--navy);">{rd[6]}</td>
</tr>
"""

cp = re.sub(r'<tbody>.*?</tbody>', f'<tbody>\n{table_rows_html.strip()}\n</tbody>', cp, flags=re.DOTALL)
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp)
print("Updated current prices")

# 3. script.min.js
with open('script.min.js', 'r', encoding='utf-8') as f:
    js = f.read()
    
# Replace exact values in script.min.js
js = re.sub(r'{symbol:"AFRIPRISE",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"AFRIPRISE",marketCap:0.6,volume:90355,price:780}', js)
js = re.sub(r'{symbol:"CRDB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"CRDB",marketCap:2.4,volume:431081,price:2940}', js)
js = re.sub(r'{symbol:"DCB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"DCB",marketCap:-4.5,volume:106635,price:420}', js)
js = re.sub(r'{symbol:"DSE",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"DSE",marketCap:0.5,volume:1259,price:6200}', js)
js = re.sub(r'{symbol:"KCB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"KCB",marketCap:0.0,volume:2386,price:2200}', js)
js = re.sub(r'{symbol:"MBP",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"MBP",marketCap:2.9,volume:5467,price:2150}', js)
js = re.sub(r'{symbol:"MCB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"MCB",marketCap:-1.3,volume:59796,price:375}', js)
js = re.sub(r'{symbol:"MKCB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"MKCB",marketCap:1.4,volume:3670,price:3660}', js)
js = re.sub(r'{symbol:"MUCOBA",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"MUCOBA",marketCap:11.1,volume:356,price:450}', js)
js = re.sub(r'{symbol:"NICO",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"NICO",marketCap:-3.5,volume:31545,price:3610}', js)
js = re.sub(r'{symbol:"NMB",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"NMB",marketCap:0.0,volume:859775,price:2130}', js)
js = re.sub(r'{symbol:"PAL",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"PAL",marketCap:0.0,volume:8398,price:305}', js)
js = re.sub(r'{symbol:"SWIS",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"SWIS",marketCap:1.2,volume:5836,price:2560}', js)
js = re.sub(r'{symbol:"TBL",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TBL",marketCap:0.0,volume:1795,price:9800}', js)
js = re.sub(r'{symbol:"TCC",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TCC",marketCap:0.2,volume:888,price:13200}', js)
js = re.sub(r'{symbol:"TCCL",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TCCL",marketCap:-2.8,volume:5670,price:3810}', js)
js = re.sub(r'{symbol:"TOL",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TOL",marketCap:1.1,volume:2764,price:1810}', js)
js = re.sub(r'{symbol:"TPCC",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TPCC",marketCap:1.8,volume:1253,price:5700}', js)
js = re.sub(r'{symbol:"TTP",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"TTP",marketCap:0.0,volume:125,price:425}', js)
js = re.sub(r'{symbol:"VODA",marketCap:[\d\.-]+,volume:\d+,price:[\d\.-]+}', '{symbol:"VODA",marketCap:-0.8,volume:189462,price:1280}', js)

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(js)
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated scripts")
