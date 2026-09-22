import re

# From docx Top Movers:
heatmap_data = [
    "{ symbol: 'NMB', marketCap: 2675, change: 2.9 },",
    "{ symbol: 'TBL', marketCap: 3200, change: -0.7 },",
    "{ symbol: 'CRDB', marketCap: 1515, change: 0.0 },",
    "{ symbol: 'VODA', marketCap: 1200, change: 3.3 },",
    "{ symbol: 'TPCC', marketCap: 900, change: -0.2 },",
    "{ symbol: 'NICO', marketCap: 700, change: 0.8 },",
    "{ symbol: 'KCB', marketCap: 380, change: 0.0 },",
    "{ symbol: 'JHL', marketCap: 320, change: 0.6 },",
    "{ symbol: 'TCCL', marketCap: 300, change: 0.3 },",
    "{ symbol: 'DCB', marketCap: 180, change: 0.0 },",
    "{ symbol: 'TICL', marketCap: 150, change: 0.0 },",
    "{ symbol: 'TOL', marketCap: 120, change: -1.1 },",
    "{ symbol: 'SWIS', marketCap: 100, change: -1.5 },",
    "{ symbol: 'AFRIPRISE', marketCap: 80, change: 0.0 },",
    "{ symbol: 'MCB', marketCap: 50, change: -3.8 },",
    "{ symbol: 'PAL', marketCap: 40, change: 3.3 },",
    "{ symbol: 'MUCOBA', marketCap: 20, change: 2.5 }",
]

with open('script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the data array inside initDSEHeatmap
new_js = re.sub(r'const data = \[.*?\];', 'const data = [\n        ' + '\n        '.join(heatmap_data) + '\n    ];', js_content, flags=re.DOTALL)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

# Also update script.min.js
with open('script.min.js', 'r', encoding='utf-8') as f:
    min_js_content = f.read()

new_min_js = re.sub(r'const [a-zA-Z0-9_]+=new Array\(\{symbol:"NMB".*?\}\];', 'const data=[' + ''.join(heatmap_data).replace(' ', '').replace(',\n', ',') + '];', min_js_content, flags=re.DOTALL)
# It might be simpler to just copy script.js to script.min.js if there's no actual minification, but let's just do a basic replace or see if it matches.
# Actually, the user says script.min.js needs updating. I will just replace the exact data string.
