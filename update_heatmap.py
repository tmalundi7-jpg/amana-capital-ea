import json
import re

# Load prices
with open('extracted_current_prices_17_aug_2026.json', 'r', encoding='utf-8') as f:
    prices = {p['ticker']: p for p in json.load(f)['prices']}

for js_file in ['script.js', 'script.min.js']:
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the data array in initDSEHeatmap
    match = re.search(r'const data = \[(.*?)\];', content, re.DOTALL)
    if match:
        data_str = match.group(1)
        # Parse the JS objects roughly
        new_data_str = []
        for line in data_str.split('\n'):
            if '{' in line:
                sym_m = re.search(r"symbol:\s*'([^']+)'", line)
                if sym_m:
                    sym = sym_m.group(1)
                    if sym in prices:
                        c_str = prices[sym].get('change_pct', '0%').replace('?', '-').replace('', '-').replace('%', '')
                        try:
                            new_change = float(c_str)
                        except:
                            new_change = 0.0
                        line = re.sub(r'change:\s*[^}]+', f'change: {new_change} ', line)
            new_data_str.append(line)
        
        new_content = content[:match.start(1)] + '\n'.join(new_data_str) + content[match.end(1):]
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {js_file}')
