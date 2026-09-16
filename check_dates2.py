import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

for m in re.finditer(r'.{0,20}(?:august|aug|july|jul|september|sep) 2026.{0,20}', c, re.IGNORECASE):
    print("Match:", repr(m.group(0)))
