import json
import re

prices = {}
with open('15_sep_prices.txt', 'r', encoding='utf-16', errors='ignore') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

start_idx = -1
for i, l in enumerate(lines):
    if 'Sector' in l and i+3 < len(lines) and 'Volume' in lines[i+3]:
        start_idx = i + 5
        break

if start_idx != -1:
    i = start_idx
    while i < len(lines):
        if lines[i].startswith('Block trades') or lines[i].startswith('Change (%)'):
            break
        if i + 6 < len(lines):
            ticker = lines[i].strip().replace('\ufffd', '')
            change = lines[i+4].strip().replace('%', '').replace('+', '').replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
            
            try:
                cf = float(change)
                prices[ticker] = cf
            except:
                prices[ticker] = 0.0
            
            i += 7
        else:
            break

with open('prices_15sept.json', 'w') as f:
    json.dump(prices, f, indent=2)

print("Generated prices_15sept.json")
