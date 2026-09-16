import re
with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()
match = re.search(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', c, flags=re.DOTALL)
if match:
    print(match.group(0))
