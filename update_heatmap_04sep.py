import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# The changes from 4 September 2026
changes = {
    'CRDB': 1.9,
    'DCB': 2.1,
    'DSE': -1.4,
    'KCB': 3.7,
    'MBP': 1.5,
    'MCB': 2.6,
    'NICO': -1.2,
    'NMB': 3.6,
    'NMG': 0.0,
    'SWIS': -0.4,
    'TBL': 0.9,
    'TCCL': 0.8,
    'TOL': -0.5,
    'TPCC': -0.2,
    'VODA': -1.9
}

for js_file in ['script.js', 'script.min.js']:
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the data array
    # In minified, it might be `const data=[{symbol:"NMB",marketCap:2675,change:4.9},...];`
    match = re.search(r'const data\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not match:
        print(f"Failed to find data in {js_file}")
        continue
        
    data_str = match.group(1)
    
    # We will use regex to find each `{ symbol: 'NMB', marketCap: 2675, change: 4.9 }` and replace change
    
    def repl(m):
        sym = m.group(1)
        cap = m.group(2)
        old_change = m.group(3)
        if sym in changes:
            new_change = changes[sym]
            return f"{{ symbol: '{sym}', marketCap: {cap}, change: {new_change} }}"
        else:
            return m.group(0) # Keep original if not in changes
            
    # For script.js it looks like { symbol: 'NMB', marketCap: 2675, change: 4.9 }
    # For minified it looks like {symbol:"NMB",marketCap:2675,change:4.9}
    
    # We can match loosely:
    new_data_str = re.sub(r'\{\s*symbol:\s*[\'"]([A-Z]+)[\'"]\s*,\s*marketCap:\s*([\d.]+)\s*,\s*change:\s*([-\d.]+)\s*\}', repl, data_str)
    
    new_content = content[:match.start(1)] + new_data_str + content[match.end(1):]
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Updated {js_file}")
