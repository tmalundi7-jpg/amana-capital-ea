import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'End-of-day.*?1 September 2026', r'End-of-day &middot; 2 September 2026', c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
    
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()
    
c = re.sub(r'End-of-day.*?1 September 2026', r'End-of-day &middot; 2 September 2026', c)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed terminal dates!")
