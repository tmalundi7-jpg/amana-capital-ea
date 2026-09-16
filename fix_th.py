with open('current-prices.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<th class="th-right">Last Price (TZS)</th>', '<th scope="col" class="th-right">Last Price (TZS)</th>')
html = html.replace('<th class="th-right">Change (%)</th>', '<th scope="col" class="th-right">Change (%)</th>')
html = html.replace('<th class="th-right">Volume</th>', '<th scope="col" class="th-right">Volume</th>')
html = html.replace('<th class="th-right">Turnover (TZS)</th>', '<th scope="col" class="th-right">Turnover (TZS)</th>')
html = html.replace('<th>Company</th>', '<th scope="col">Company</th>')

# Also fix the literal \n before caption
html = html.replace('\\n<caption', '\n<caption')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(html)
