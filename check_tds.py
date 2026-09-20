with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
tbody_match = re.search(r'(<tbody>)(.*?)(</tbody>)', content, re.DOTALL)
trs = list(re.finditer(r'<tr.*?</tr>', tbody_match.group(2), re.DOTALL))
print("First row tds:")
tds = list(re.finditer(r'<td.*?>.*?</td>', trs[0].group(0), re.DOTALL))
for i, td in enumerate(tds):
    print(f"[{i}]: {td.group(0).strip()}")
