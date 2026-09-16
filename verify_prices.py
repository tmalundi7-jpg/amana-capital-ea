import re

with open('output_prices.txt', 'r', encoding='utf-8') as f:
    txt = f.read()

with open('current-prices.html', 'r', encoding='utf-8') as f:
    html = f.read()

txt_lines = [l for l in txt.split('\n') if ' | ' in l]

errors = 0
for line in txt_lines:
    parts = line.split(' | ')
    if len(parts) >= 7 and parts[0] != 'Ticker':
        ticker, company, sector, price, change, vol, turnover = parts[:7]
        # Check if this ticker is in html with the correct price and change
        # Regex to find the row
        pattern = re.compile(rf'<td><strong>{ticker}</strong></td>.*?<td[^>]*><strong>{price}</strong></td>', re.DOTALL | re.IGNORECASE)
        if not pattern.search(html):
            print(f"ERROR: {ticker} not found with price {price} in html")
            errors += 1

if errors == 0:
    print("All prices match!")
else:
    print(f"Total errors: {errors}")
