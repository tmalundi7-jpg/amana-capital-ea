import re
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()
print("market-intelligence.html links:")
links = set(re.findall(r'href="([^"]+)"', c))
for l in links:
    print(l)
