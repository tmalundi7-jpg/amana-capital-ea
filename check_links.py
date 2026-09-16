import re
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()
links = re.findall(r'href="([^"]+)"', c)
for l in links:
    if 'current' in l:
        print(l)
