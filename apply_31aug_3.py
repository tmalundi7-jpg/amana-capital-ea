import json
import re
import os

with open('extracted_31aug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']['tables'][0][1:]
# Fix minus signs properly
for p in prices:
    p[4] = p[4].replace('\ufffd', '-').replace('–', '-').replace('−', '-')

dsei = "4,440.47"
tsi = "9,897.20"
turnover = "TZS 14.89 bn"

date_str = "31 August 2026"
short_date = "2026-08-31"
volume = "7,061,300" # from the wrap table

def replace_in_file(filepath, pattern, replacement):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    c = re.sub(pattern, replacement, c, flags=re.DOTALL)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

# --- 4. Current Prices ---
replace_in_file('current-prices.html', r'<div class="cp-stat-value" id="cp-dsei">.*?</div>', f'<div class="cp-stat-value" id="cp-dsei">{dsei}</div>')
replace_in_file('current-prices.html', r'<div class="cp-stat-value" id="cp-tsi">.*?</div>', f'<div class="cp-stat-value" id="cp-tsi">{tsi}</div>')
replace_in_file('current-prices.html', r'<div class="cp-stat-value" id="cp-turnover">.*?</div>', f'<div class="cp-stat-value" id="cp-turnover">{turnover}</div>')
replace_in_file('current-prices.html', r'<div class="cp-stat-value" id="cp-volume">.*?</div>', f'<div class="cp-stat-value" id="cp-volume">{volume}</div>')
replace_in_file('current-prices.html', r'<div class="cp-stat-value" style="color:var\(--gold\);">.*?</div>', f'<div class="cp-stat-value" style="color:var(--gold);">{date_str}</div>')

# Rebuild table
table_html = ""
for p in prices:
    cls = ""
    if "+" in p[4]: cls = 'class="gain"'
    elif "-" in p[4] and p[4] != "-0.0%": cls = 'class="loss"'
    
    table_html += f"<tr>\n"
    table_html += f"  <td><strong>{p[0]}</strong></td>\n"
    table_html += f"  <td>{p[1]}</td>\n"
    table_html += f"  <td><span class=\"sector-badge\">{p[2]}</span></td>\n"
    table_html += f"  <td>{p[3]}</td>\n"
    table_html += f"  <td {cls}>{p[4]}</td>\n"
    table_html += f"  <td>{p[5]}</td>\n"
    table_html += f"  <td>{p[6]}</td>\n"
    table_html += f"</tr>\n"

replace_in_file('current-prices.html', r'<!-- PRICES_TABLE_START -->.*?<!-- PRICES_TABLE_END -->', f'<!-- PRICES_TABLE_START -->\n{table_html}<!-- PRICES_TABLE_END -->')
print("Updated current-prices.html")

# --- 5. Market Intelligence Archive ---
wrap_title = data['wrap']['paragraphs'][1]
intro_p = ""
for i, p in enumerate(data['wrap']['paragraphs']):
    if "The era of 15% risk-free yields is ending" in p or "The Dar es Salaam Stock Exchange" in p or "A session that began with" in p or "Monday's session" in p:
        intro_p = p
        break

new_archive_entry = f"""
        <div class="arc-row">
            <div class="arc-date">31 Aug<br>2026</div>
            <div class="arc-content">
                <span class="arc-badge">Equities</span>
                <a href="/dse-wrap-{short_date}" class="arc-title">{wrap_title}</a>
                <p class="arc-excerpt">{intro_p[:150]}...</p>
            </div>
            <a href="/dse-wrap-{short_date}" class="arc-read">Read Report &rarr;</a>
        </div>
"""

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc_html = f.read()

# Check if already added
if short_date not in arc_html:
    arc_html = re.sub(r'(<div class="arc-list">)', f'\\1\n{new_archive_entry}', arc_html)
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(arc_html)
    print("Updated market-intelligence-archive.html")
else:
    print("Archive already updated")

