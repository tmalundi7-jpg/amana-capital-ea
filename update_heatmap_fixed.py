import re

with open('output_prices.txt', 'r', encoding='utf-8') as f:
    txt = f.read()

txt_lines = [l for l in txt.split('\n') if ' | ' in l]

changes = {}
for line in txt_lines:
    parts = line.split(' | ')
    if len(parts) >= 7 and parts[0] != 'Ticker':
        ticker = parts[0]
        change_str = parts[4].replace('%', '').replace('+', '').replace('?"', '-').replace('–', '-')
        try:
            changes[ticker] = float(change_str)
        except ValueError:
            changes[ticker] = 0.0

if 'NMG' not in changes:
    changes['NMG'] = 0.0

def update_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

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
print("Heatmap updated correctly from output_prices.txt")
