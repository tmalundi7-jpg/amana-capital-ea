import re
import json

with open('extracted_prices.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

changes = {}
for row in d['tables'][0][1:]:
    ticker = row[0]
    change = row[4].replace('%', '').replace('+', '').replace('–', '-')
    try:
        changes[ticker] = float(change)
    except ValueError:
        changes[ticker] = 0.0

# Add NMG explicitly if missing (it's 0.0 usually)
if 'NMG' not in changes:
    changes['NMG'] = 0.0

def update_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find the data array in initDSEHeatmap
    # We will regex replace each line: { symbol: 'NMB', marketCap: 2675, change: 4.95 },
    
    def replacer(match):
        sym = match.group(1)
        if sym in changes:
            return f"symbol: '{sym}', marketCap: {match.group(2)}, change: {changes[sym]}"
        return match.group(0)

    c = re.sub(r"symbol:\s*'([^']+)',\s*marketCap:\s*([0-9.]+),\s*change:\s*[-0-9.]+", replacer, c)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(c)

update_script('script.js')
update_script('script.min.js')

print('Updated script.js and script.min.js Heatmap data.')
