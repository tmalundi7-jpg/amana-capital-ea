
import re

with open('script.min.js', 'r', encoding='utf-8') as f:
    content = f.read()

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

def replace_change(m):
    symbol = m.group(1)
    market_cap = m.group(2)
    old_change = m.group(3)
    
    if symbol in new_changes:
        new_change = new_changes[symbol]
        # Always output exactly 1 decimal place like in the source if possible, or just str()
        # Original script had e.g. 0.0, -1.1. We should format exactly to match JSON standard.
        new_change_str = str(new_change)
        return f"{{ symbol: '{symbol}', marketCap: {market_cap}, change: {new_change_str} }}"
    else:
        return m.group(0)

pattern = r"\{\s*symbol:\s*'([A-Z]+)',\s*marketCap:\s*([\d.]+),\s*change:\s*([-\d.]+)\s*\}"
new_content = re.sub(pattern, replace_change, content)

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('script.min.js updated successfully.')
