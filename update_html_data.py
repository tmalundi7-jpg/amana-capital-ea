import re
import docx

# 1. Parse Current Prices 17 July 2026.docx
cp_doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\Current Prices 17 July 2026.docx')
cp_tables = cp_doc.tables
cp_rows = []
for row in cp_tables[0].rows[1:]: # Skip header
    cells = [c.text.strip().replace('', '-') for c in row.cells]
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

cp_html = re.sub(r'End-of-Day, \w+ \d+[a-z]{2} [a-zA-Z]+ \d{4}', 'End-of-Day, Friday 17th July 2026', cp_html)
cp_html = re.sub(r'(?s)<tbody>.*?</tbody>', f'<tbody>\n{cp_tbody}            </tbody>', cp_html)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp_html)
    
print("Updated current-prices.html")

# 3. Snapshot Data (Hardcoded based on extraction)
dsei = "4,111.98"
tsi = "8,969.32"
turnover = "TZS 38.44 bn"
gainers_html = 'MUCOBA <span style="color:var(--gain)">+7.7%</span><br>DSE <span style="color:var(--gain)">+2.8%</span><br>TCCL <span style="color:var(--gain)">+2.4%</span>'
losers_html = 'TTP <span style="color:var(--loss)">-11.1%</span><br>DCB <span style="color:var(--loss)">-6.3%</span><br>MCB <span style="color:var(--loss)">-5.1%</span>'

# 4. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = re.sub(r'<div class="snapshot-value" id="home-dsei">.*?</div>', f'<div class="snapshot-value" id="home-dsei">{dsei}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-value" id="home-tsi">.*?</div>', f'<div class="snapshot-value" id="home-tsi">{tsi}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-value" id="home-turnover">.*?</div>', f'<div class="snapshot-value" id="home-turnover">{turnover}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-mover" id="home-gainers">.*?</div>', f'<div class="snapshot-mover" id="home-gainers">{gainers_html}</div>', idx_html)
idx_html = re.sub(r'<div class="snapshot-mover" id="home-losers">.*?</div>', f'<div class="snapshot-mover" id="home-losers">{losers_html}</div>', idx_html)

# Update Wrap content in index.html
wrap_date = "17 July 2026"
wrap_title = "Fourth CRDB Block Trade Seals Historic Handover as Foreign Selling Drops to a Year-Low"
wrap_teaser = "Friday's session at the Dar es Salaam Stock Exchange closed the week with the fourth enormous CRDB block trade of July — and the clearest signal yet that the largest ownership transfer in the exchange's history is complete. Another 13.2 million CRDB shares changed hands on the pre-arranged board, bringing the total for the month to over 116 million shares..."

idx_html = re.sub(r'<div class="wrap-date">.*?</div>', f'<div class="wrap-date">{wrap_date}</div>', idx_html)
idx_html = re.sub(r'<h3 class="wrap-title">.*?</h3>', f'<h3 class="wrap-title">{wrap_title}</h3>', idx_html)
idx_html = re.sub(r'<p class="wrap-teaser">.*?</p>', f'<p class="wrap-teaser">{wrap_teaser}</p>', idx_html)

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
                    <td><a href="#" class="btn-secondary" style="padding: 0.5rem 1rem;">Read</a> <a href="#" class="btn-secondary" style="padding: 0.5rem 1rem;">Download PDF</a></td>
                </tr>
'''

mi_html = mi_html.replace('<tbody>\n', f'<tbody>\n{new_archive_row}')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

print("Updated market-intelligence.html")
