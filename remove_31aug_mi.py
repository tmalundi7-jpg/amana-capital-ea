import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

m31 = re.search(r'<a class="archive-row" href="/dse-wrap-2026-08-31">.*?</a>\n?', mi, flags=re.DOTALL)
if m31:
    mi = mi.replace(m31.group(0), '')
    with open('market-intelligence.html', 'w', encoding='utf-8') as f:
        f.write(mi)
    print('Removed 31 Aug from market-intelligence.html')
else:
    print('Could not find 31 Aug in market-intelligence.html')
