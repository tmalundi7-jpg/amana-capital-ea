import re
from docx import Document

doc = Document(r'C:\Users\tmalu\Documents\Current Prices 18 September 2026.docx')
prices = {}
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows[1:]):
        cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        prices[cells[0]] = cells

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update date
content = content.replace('Thursday 17th September 2026', 'Friday 18th September 2026')
# Update block trades
content = content.replace('NMB: 5,450,000 shares', 'CRDB: 380,000 shares')

# Process rows by finding them with regex
# Row pattern: <tr> ... <span ...>TICKER</span> ... </tr> or just <tr>...<td>TICKER</td>...</tr>
# We'll split by <tr> and process each one.

parts = content.split('<tr>')
new_parts = [parts[0]]

for part in parts[1:]:
    # Find ticker
    match = re.search(r'<td[^>]*>(?:<div[^>]*>)?(?:<span[^>]*>)?([A-Z]{2,5})(?:</span>)?', part)
    if not match:
        new_parts.append(part)
        continue
    
    ticker = match.group(1)
    
    if ticker in prices:
        # Show row
        # Remove display: none; if exists. Wait, the style is on <tr>, which was split out.
        # But wait! '<tr>' was the split string! So if it had 'style="display: none;"', it would be '<tr style="display: none;">'.
        # Since I split by '<tr>', any row with attributes wasn't split!!
        pass
    new_parts.append(part)

