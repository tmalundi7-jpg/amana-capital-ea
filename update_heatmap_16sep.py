
# Update script.min.js heatmap with 16 Sep 2026 data
# Changes from wrap doc:
# VODA +3.5, PAL +3.3, MCB +2.6, DCB +2.3, TCC +0.7
# AFRIPRISE -0.8, CRDB -0.7, NMB -1.4, TOL -4.2, TCCL -5.1
# TPCC -0.7, TBL 0.0, KCB -1.8, MBP -1.0, NICO -1.1, SWIS -3.0
# MUCOBA -6.8, TTP -2.3, DSE -0.5, JATU 0.0

import re

with open('script.min.js', 'r', encoding='utf-8') as f:
    content = f.read()

# New changes map from source (all tickers from prices doc)
new_changes = {
    'AFRIPRISE': -0.8,
    'CRDB': -0.7,
    'DCB': 2.3,
    'DSE': -0.5,
    'JATU': 0.0,
    'KCB': -1.8,
    'MBP': -1.0,
    'MCB': 2.6,
    'MKCB': 0.0,
    'MUCOBA': -6.8,
    'NICO': -1.1,
    'NMB': -1.4,
    'PAL': 3.3,
    'SWIS': -3.0,
    'TBL': 0.0,
    'TCC': 0.7,
    'TCCL': -5.1,
    'TOL': -4.2,
    'TPCC': -0.7,
    'TTP': -2.3,
    'VODA': 3.5,
}

# Find the heatmap data array in script.min.js
# Pattern: { symbol: 'XXX', marketCap: NNN, change: N.N }
def replace_change(m):
    symbol = m.group(1)
    market_cap = m.group(2)
    old_change = m.group(3)
    
    if symbol in new_changes:
        new_change = new_changes[symbol]
        # Format: if integer, show as integer; otherwise show decimal
        if new_change == int(new_change):
            new_change_str = str(int(new_change))
        else:
            new_change_str = str(new_change)
        return f"{{ symbol: '{symbol}', marketCap: {market_cap}, change: {new_change_str} }}"
    else:
        return m.group(0)  # unchanged

pattern = r"\{\s*symbol:\s*'([A-Z]+)',\s*marketCap:\s*([\d.]+),\s*change:\s*([-\d.]+)\s*\}"
new_content = re.sub(pattern, replace_change, content)

# Count replacements
old_matches = re.findall(pattern, content)
print(f'Found {len(old_matches)} heatmap entries')
print('Symbols found:', [m[0] for m in old_matches])

# Verify specific tickers
for ticker, expected in [('VODA', 3.5), ('TCCL', -5.1), ('TOL', -4.2), ('CRDB', -0.7), ('NMB', -1.4)]:
    pattern_check = f"symbol: '{ticker}', marketCap: [\\d.]+, change: ([\\-\\d.]+)"
    m = re.search(pattern_check, new_content)
    if m:
        found = float(m.group(1))
        status = 'OK' if found == expected else f'FAIL (expected {expected})'
        print(f'  {ticker}: {found} [{status}]')
    else:
        print(f'  {ticker}: NOT FOUND')

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('script.min.js saved.')
