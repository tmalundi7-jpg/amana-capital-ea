import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'End-of-Day, 1 September 2026', r'End-of-Day, 2 September 2026', c)
c = re.sub(r'End-of-Day, 31 August 2026', r'End-of-Day, 2 September 2026', c)
c = re.sub(r'End-of-Day, 28 August 2026', r'End-of-Day, 2 September 2026', c)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated current-prices.html subtitle.")
