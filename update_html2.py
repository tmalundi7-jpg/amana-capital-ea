import re

with open("current-prices.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace CSS variables with hex
html = html.replace("var(--navy)", "#0B1D3A")
html = html.replace("var(--cream)", "#FBF7F0")
html = html.replace("var(--mist)", "#9A9490")
html = html.replace("var(--gold)", "#C8962E")

# Add body inline style
html = html.replace('<body>', '<body style="background-color: #FBF7F0; color: #0B1D3A;">')

# Fix main swup class
html = html.replace('<main id="swup">', '<main id="swup" class="transition-fade">')

# Update date
html = re.sub(r'End-of-Day,.*2026', 'End-of-Day, Friday, 11th September 2026', html)

# Fix script tags
old_scripts = '<script defer="" src="script.min.js-v=20260830_final_polish_27"></script>'
new_scripts = """    <script src="https://unpkg.com/swup@4"></script>
    <script src="https://unpkg.com/@swup/progress-plugin@3"></script>
    <script src="https://unpkg.com/@swup/preload-plugin@3"></script>
    <script src="https://unpkg.com/@swup/scripts-plugin@2"></script>
    <script defer="" src="script.min.js?v=20260907_heatmap_fix"></script>"""
html = html.replace(old_scripts, new_scripts)

# Update pre-arranged board
board_html = """
  <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">4,904,282 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">TCC</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">114,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">VODA</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">600,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
  </div>"""

html = re.sub(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>', board_html + '\n</div>', html, flags=re.DOTALL)

data = [
    ("AFRIPRISE", "African Pride", "Commercial Services", "605", "-0.8%", "224,732", "135,896,150"),
    ("CRDB", "CRDB Bank", "Banks & Finance", "2,900", "+2.1%", "626,636", "1,820,183,120"),
    ("DCB", "Dar es Salaam Community Bank", "Banks & Finance", "445", "0.0%", "21,411", "9,483,390"),
    ("DSE", "Dar es Salaam Stock Exchange", "Commercial Services", "6,390", "+0.2%", "594", "3,793,720"),
    ("JATU", "Jatu Plc", "Commercial Services", "270", "0.0%", "2", "540"),
    ("KCB", "KCB Group (cross-listed)", "Banks & Finance", "2,120", "+1.0%", "33,413", "70,863,690"),
    ("MBP", "Maendeleo Bank", "Banks & Finance", "2,030", "-1.9%", "4,884", "9,938,080"),
    ("MCB", "Mwanga Community Bank", "Banks & Finance", "390", "-1.3%", "82,879", "32,417,250"),
    ("MKCB", "Mkamba Commercial Bank", "Banks & Finance", "3,730", "-0.5%", "3,978", "14,833,550"),
    ("MUCOBA", "Mucoba Bank", "Banks & Finance", "460", "0.0%", "40", "18,200"),
    ("NICO", "NICO Holdings", "Banks & Finance", "3,870", "+1.0%", "17,197", "66,635,210"),
    ("NMB", "NMB Bank", "Banks & Finance", "2,190", "0.0%", "5,726,307", "12,113,609,260"),
    ("PAL", "Pal Holdings", "Industrials", "305", "-1.6%", "6,642", "2,021,020"),
    ("SWIS", "Swissport Tanzania", "Commercial Services", "2,720", "-2.5%", "601", "1,612,050"),
    ("TBL", "Tanzania Breweries", "Industrials", "10,000", "+0.2%", "5,278", "52,754,650"),
    ("TCC", "Tanga Cement", "Industrials", "13,440", "+1.4%", "115,430", "1,529,710,000"),
    ("TCCL", "Tanzania Cigarette Company", "Industrials", "3,970", "+0.8%", "1,255", "4,987,600"),
    ("TOL", "TOL Gases", "Industrials", "1,760", "-3.8%", "18,907", "33,332,480"),
    ("TPCC", "Tanga Portland Cement", "Industrials", "5,770", "-0.3%", "6,259", "36,097,410"),
    ("TTP", "Tatepa Public Limited Company", "Commercial Services", "450", "0.0%", "1,046", "470,700"),
    ("VODA", "Vodacom Tanzania", "Commercial Services", "1,110", "0.0%", "631,323", "700,889,850")
]

tbody = []
for row in data:
    ticker, company, sector, price, change, volume, turnover = row
    change_class = ""
    if change.startswith("-"):
        change_class = " change-negative"
    elif change.startswith("+"):
        change_class = " change-positive"
    
    tbody.append(f'''                            <tr>
                                <td><strong>{ticker}</strong></td>
                                <td>{company}</td>
                                <td style="color: #9A9490;">{sector}</td>
                                <td class="text-right"><strong>{price}</strong></td>
                                <td class="text-right{change_class}"><strong>{change}</strong></td>
                                <td class="text-right">{volume}</td>
                                <td class="text-right">{turnover}</td>
                            </tr>''')

tbody_html = "\\n".join(tbody)
html = re.sub(r'<tbody>.*?</tbody>', '<tbody>\\n' + tbody_html + '\\n</tbody>', html, flags=re.DOTALL)

# Update omitted text
html = re.sub(r'Counters with no trades.*?omitted\.', 'Counters with no trades (EABL, JHL, KA, NMG, SWALA, USL, YETU) are omitted.', html)

with open("current-prices.html", "w", encoding="utf-8") as f:
    f.write(html)
