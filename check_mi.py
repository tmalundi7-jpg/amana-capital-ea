import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Dates:", re.findall(r'\d+ \w+ \d{4}', c))

with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp = f.read()

print("Current Prices dates:", re.findall(r'\d+ \w+ \d{4}', cp))

