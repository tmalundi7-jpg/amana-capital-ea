import bs4
import re

# 1. Parse current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

prices = {}
table = soup.find('table', class_='data-table')
if table:
    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 5:
            sym = tds[0].get_text(strip=True)
            chg_str = tds[4].get_text(strip=True).replace('\u2212', '-')
            if chg_str == '0.0%':
                chg = 0.0
            else:
                chg = float(chg_str.replace('%', '').replace('+', ''))
            prices[sym] = chg

# 2. Identify Top Gainers and Top Losers
gainers = {k: v for k, v in prices.items() if v > 0}
losers = {k: v for k, v in prices.items() if v < 0}

top_gainers = sorted(gainers.items(), key=lambda x: x[1], reverse=True)[:5]
top_losers = sorted(losers.items(), key=lambda x: x[1])[:5]

# Function to build snapshot HTML
def build_snapshot_html(items, is_gain):
    html = ''
    color_var = '--gain' if is_gain else '--loss'
    for sym, val in items:
        sign = '+' if val > 0 else ''
        html += f'              <span>{sym} <span style="color:var({color_var})">{sign}{val:.1f}%</span></span>\n'
    return html.rstrip()

gainers_html = build_snapshot_html(top_gainers, True)
losers_html = build_snapshot_html(top_losers, False)

# 3. Update index.html and market-intelligence.html
def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Replace gainers
    gainer_pattern = r'(id="home-gainers".*?>\s*)(.*?)(?=\s*</div>)'
    text = re.sub(gainer_pattern, r'\g<1>' + gainers_html.replace('\\', '\\\\'), text, flags=re.DOTALL)
    
    # Replace losers
    loser_pattern = r'(id="home-losers".*?>\s*)(.*?)(?=\s*</div>)'
    text = re.sub(loser_pattern, r'\g<1>' + losers_html.replace('\\', '\\\\'), text, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

update_html_file('index.html')
update_html_file('market-intelligence.html')

# 4. Update script.js and script.min.js heatmap array
def update_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find the data array block
    # It looks like: const data = [ ... ];
    # Let's replace each change value for the symbols in the heatmap
    def replacer(match):
        sym = match.group(1)
        # If symbol in prices, use it, else 0.0
        val = prices.get(sym, 0.0)
        return f"symbol: '{sym}', marketCap: {match.group(2)}, change: {val:.1f}"
        
    text = re.sub(r"symbol:\s*'([A-Z]+)',\s*marketCap:\s*([0-9]+),\s*change:\s*[-0-9.]+", replacer, text)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

update_script('script.js')
update_script('script.min.js')

print("Update complete")
for sym, val in top_gainers:
    print(f"Gainer: {sym} +{val}%")
for sym, val in top_losers:
    print(f"Loser: {sym} {val}%")
