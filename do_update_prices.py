import re
from docx import Document
from bs4 import BeautifulSoup

# 1. Read the DOCX
doc = Document(r'C:\Users\tmalu\Documents\Current Prices 18 September 2026.docx')

prices = {}
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows[1:]):
        cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        ticker = cells[0]
        # cells: Ticker, Company, Sector, Last Price, Change, Volume, Turnover
        prices[ticker] = cells

# 2. Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update date
content = content.replace('Thursday 17th September 2026', 'Friday 18th September 2026')
# Update block trades
content = content.replace('NMB: 5,450,000 shares', 'CRDB: 380,000 shares')

# Now process the table using BeautifulSoup to preserve EVERYTHING except text contents and specific classes
soup = BeautifulSoup(content, 'html.parser')

tbody = soup.find('tbody')
trs = tbody.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    if not tds:
        continue
        
    # The first td has a span with the ticker name, but wait, the first td contains <div>... <span>TICKER</span>
    ticker_span = tds[0].find('span', style=re.compile(r'color: var\(--navy\); font-weight: 600;'))
    if not ticker_span:
        ticker = tds[0].get_text(strip=True).split('\n')[0].strip()
    else:
        ticker = ticker_span.get_text(strip=True)

    # Some might just have raw text or inside a div.
    # Let's extract the ticker more reliably:
    # It's usually the text before any <br> or inside a specific span.
    # Actually, in current-prices.html, the first TD has <div ...><span style="...">TICKER</span><span ...>Name</span></div>
    if ticker_span:
        ticker = ticker_span.get_text(strip=True)
        
    if ticker in prices:
        # Show row
        if 'display: none' in tr.get('style', ''):
            style = tr.get('style')
            tr['style'] = style.replace('display: none;', '').strip()
            
        data = prices[ticker]
        last_price = data[3]
        change = data[4].replace('-', '&minus;').replace('−', '&minus;').replace('', '&minus;')
        volume = data[5]
        turnover = data[6]
        
        # update last price
        # It's the 3rd TD (index 2)
        tds[2].string = last_price
        
        # update change
        # It's the 4th TD (index 3). It contains a span.
        change_span = tds[3].find('span')
        if change_span:
            change_span.clear()
            # We need to insert HTML for &minus;, so we can just set it and let soup handle it, but soup escapes.
            # We will use BeautifulSoup parsing for the text.
            from bs4 import NavigableString
            
            # update class
            if '+' in change:
                change_span['class'] = ['change-positive']
            elif '&minus;' in change:
                change_span['class'] = ['change-negative']
            else:
                change_span['class'] = ['change-neutral']
                
            # If it's 0.0%, no minus or plus.
            if change == '0.0%':
                change_str = '0.0%'
            else:
                # keep raw string, we'll replace the &amp;minus; later in raw HTML
                change_str = change.replace('&minus;', 'MINUS_SIGN')
                
            change_span.string = change_str
            
        # update volume
        tds[4].string = volume
        
        # update turnover
        # Wait, turnover TD has a span and a div
        # <td ...><div ...><span>2,380,191,230</span><span class="invisible-spacer">...</span></div></td>
        val_span = tds[5].find('span', class_=False)
        if val_span:
            val_span.string = turnover
            
    else:
        # Hide row
        style = tr.get('style', '')
        if 'display: none' not in style:
            tr['style'] = style + '; display: none;' if style else 'display: none;'

# Convert back to string
new_content = str(soup)
new_content = new_content.replace('MINUS_SIGN', '&minus;')

# Also fix the block trade styling if it got messed up (NMB to CRDB).
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated current-prices.html")
