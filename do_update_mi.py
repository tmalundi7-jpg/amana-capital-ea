import re

# 1. Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace dates
content = content.replace('17 September 2026', '18 September 2026')
content = content.replace('17 Sep 2026', '18 Sep 2026')
content = content.replace('17th September 2026', '18th September 2026')

# Replace snapshot figures
content = content.replace('4,632.03', '4,602.26') # DSEI
content = content.replace('10,220.27', '10,166.24') # TSI
content = content.replace('TZS 15.39 bn', 'TZS 4.30 bn') # Turnover

# Replace Gainers
content = re.sub(r'PAL, VODA, MCB, DCB, TCC', r'AFRIPRISE, VODA, KCB', content)
# Replace Losers
content = re.sub(r'TCCL, TOL, NMB, CRDB, AFRIPRISE, TPCC', r'PAL, DSE, CRDB, TOL, NMB', content)

# Update archive snippet for 18th
# The old one had "Banks Under Pressure as a Massive NMB Block..."
content = content.replace('Banks Under Pressure as a Massive NMB Block Trade Drives a 51% Turnover Surge', 'Turnover Cools but CRDB Absorbs a 380,000-Share Block Without Flinching')
content = content.replace('dse-wrap-2026-09-17', 'dse-wrap-2026-09-18')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated market-intelligence.html")

