import re
import docx
import sys

# 1. Parse Current Prices 17 July 2026.docx
try:
    cp_doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\Current Prices 17 July 2026.docx')
except Exception as e:
    print(f"Error reading docx: {e}")
    sys.exit(1)

cp_tables = cp_doc.tables
cp_rows = []
for row in cp_tables[0].rows[1:]: # Skip header
    cells = [c.text.strip() for c in row.cells]
    cp_rows.append(cells)

# Generate HTML for the current-prices table rows
cp_tbody = ""
for row in cp_rows:
    if not row or not row[0]: continue
    cp_tbody += f"                <tr>\n"
    cp_tbody += f"                    <td><strong>{row[0]}</strong></td>\n"
    cp_tbody += f"                    <td>{row[1]}</td>\n"
    cp_tbody += f"                    <td>{row[2]}</td>\n"
    cp_tbody += f"                    <td>{row[3]}</td>\n"
    
    # Handling color for change
    change = row[4]
    
    # Fix weird character in change if any (e.g. 6.3% -> -6.3%)
    # Replace anything that isn't a digit, period, plus, or percent sign with a hyphen
    # If the string contains a minus-like character, it will be caught here.
    if change != "0.0%":
        change_cleaned = re.sub(r'[^0-9\.%\+]', '-', change)
    else:
        change_cleaned = change
        
    color_class = ""
    if '+' in change_cleaned:
        color_class = ' style="color:var(--gain)"'
    elif '-' in change_cleaned:
        color_class = ' style="color:var(--loss)"'
    
    cp_tbody += f"                    <td{color_class}>{change_cleaned}</td>\n"
    
    # Fix weird character in Volume if any (e.g. 13,660,491 -> 13,660,491)
    vol = re.sub(r'[^0-9,]', '', row[5])
    
    cp_tbody += f"                    <td>{vol}</td>\n"
    cp_tbody += f"                    <td>{row[6]}</td>\n"
    cp_tbody += f"                </tr>\n"

# 2. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp_html = f.read()

cp_html = re.sub(r'End-of-Day, \w+ \d+[a-z]{2} [a-zA-Z]+ \d{4}', 'End-of-Day, Friday 17th July 2026', cp_html)
cp_html = re.sub(r'(?s)<tbody>.*?</tbody>', f'<tbody>\n{cp_tbody}            </tbody>', cp_html)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(cp_html)
    
print("Updated current-prices.html successfully with safe unicode stripping.")
