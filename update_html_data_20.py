import re
import docx

# 1. Parse Current Prices 20 July 2026.docx
cp_doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\Current Prices 20 July 2026.docx')
cp_tables = cp_doc.tables
cp_rows = []
for row in cp_tables[0].rows[1:]: # Skip header
    cells = [c.text.strip().replace('\ufffd', '-').replace('—', '-') for c in row.cells]
    cp_rows.append(cells)

# Generate HTML for the current-prices table rows
cp_tbody = ""
for row in cp_rows:
    cp_tbody += f"                <tr>\n"
    cp_tbody += f"                    <td><strong>{row[0]}</strong></td>\n"
    cp_tbody += f"                    <td>{row[1]}</td>\n"
    cp_tbody += f"                    <td>{row[2]}</td>\n"
    cp_tbody += f"                    <td>{row[3]}</td>\n"
    
    # Handling color for change
    change = row[4]
    color_class = ""
    if '+' in change:
        color_class = ' style="color:var(--gain)"'
    elif '-' in change:
        color_class = ' style="color:var(--loss)"'
    
    cp_tbody += f"                    <td{color_class}>{change}</td>\n"
    cp_tbody += f"                    <td>{row[5]}</td>\n"
    cp_tbody += f"                    <td>{row[6]}</td>\n"
    cp_tbody += f"                </tr>\n"

# 2. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp_html = f.read()

cp_html = re.sub(r'End-of-Day, \w+ \d+[a-z]{2} [a-zA-Z]+ \d{4}', 'End-of-Day, Monday 20th July 2026', cp_html)
cp_html = re.sub(r'(?s)<tbody>.*?</tbody>', f'<tbody>\n{cp_tbody}            </tbody>', cp_html)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp_html)
    
print("Updated current-prices.html")

# 3. Snapshot Data (Hardcoded based on extraction)
dsei = "4,102.83"
tsi = "8,952.33"
turnover = "TZS 4.61 bn"
gainers_html = 'DSE <span style="color:var(--gain)">+2.4%</span><br>TCCL <span style="color:var(--gain)">+0.9%</span><br>PAL <span style="color:var(--gain)">+5.4%</span>'
losers_html = 'TTP <span style="color:var(--loss)">-2.2%</span><br>DCB <span style="color:var(--loss)">-5.0%</span><br>MCB <span style="color:var(--loss)">-3.5%</span><br>MBP <span style="color:var(--loss)">-9.8%</span>'

# 4. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = re.sub(r'<div class="snapshot-value" id="home-dsei">.*?</div>', f'<div class="snapshot-value" id="home-dsei">{dsei}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-value" id="home-tsi">.*?</div>', f'<div class="snapshot-value" id="home-tsi">{tsi}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-value" id="home-turnover">.*?</div>', f'<div class="snapshot-value" id="home-turnover">{turnover}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-mover" id="home-gainers">.*?</div>', f'<div class="snapshot-mover" id="home-gainers">{gainers_html}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-mover" id="home-losers">.*?</div>', f'<div class="snapshot-mover" id="home-losers">{losers_html}</div>', idx_html)

# Update Wrap content in index.html
wrap_date = "20 July 2026"
wrap_title = "CRDB Block Wave Subsides as VODA Block Surprises and NMB Hits a New Peak"
wrap_teaser = "The Dar es Salaam Stock Exchange opened the new week with a change of pace. After two weeks dominated by massive CRDB block trades, Monday delivered a more varied session. A large 600,000-share VODA block took centre stage, while CRDB's block activity shrank dramatically to just 200,000 shares — the smallest in July. The number of individual deals jumped to 3,701, the highest in over a week, showing that everyday investors and local institutions are increasingly driving the market. Meanwhile, NMB briefly surged to a new high of 17,050 before settling back."

idx_html = re.sub(r'<div class="wrap-date">.*?</div>', f'<div class="wrap-date">{wrap_date}</div>', idx_html)
idx_html = re.sub(r'<h3 class="wrap-title">.*?</h3>', f'<h3 class="wrap-title">{wrap_title}</h3>', idx_html)
idx_html = re.sub(r'<p class="wrap-teaser">.*?</p>', f'<p class="wrap-teaser">{wrap_teaser}</p>', idx_html)
# Update the link inside the button (it should point to dse-wrap-2026-07-20.html)
idx_html = re.sub(r'href="dse-wrap-2026-07-17.html"', 'href="dse-wrap-2026-07-20.html"', idx_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)

print("Updated index.html")

# 5. Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

mi_html = re.sub(r'<div class="snapshot-value" id="mi-dsei">.*?</div>', f'<div class="snapshot-value" id="mi-dsei">{dsei}</div>', mi_html)
mi_html = re.sub(r'<div class="snapshot-value" id="mi-tsi">.*?</div>', f'<div class="snapshot-value" id="mi-tsi">{tsi}</div>', mi_html)
mi_html = re.sub(r'<div class="snapshot-value" id="mi-turnover">.*?</div>', f'<div class="snapshot-value" id="mi-turnover">{turnover}</div>', mi_html)
mi_html = re.sub(r'<div class="snapshot-mover" id="mi-gainers">.*?</div>', f'<div class="snapshot-mover" id="mi-gainers">{gainers_html}</div>', mi_html)
mi_html = re.sub(r'<div class="snapshot-mover" id="mi-losers">.*?</div>', f'<div class="snapshot-mover" id="mi-losers">{losers_html}</div>', mi_html)

# Add new archive entry in market-intelligence.html
new_archive_row = f'''                <tr>
                    <td>{wrap_date}</td>
                    <td>{wrap_title}</td>
                    <td><a href="dse-wrap-2026-07-20.html" class="btn-secondary" style="padding: 0.5rem 1rem;">Read</a> <a href="#" class="btn-secondary" style="padding: 0.5rem 1rem;">Download PDF</a></td>
                </tr>
'''

mi_html = mi_html.replace('<tbody>\n', f'<tbody>\n{new_archive_row}')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

print("Updated market-intelligence.html")
