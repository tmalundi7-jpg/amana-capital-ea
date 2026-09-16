with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r'\n<div class="brand-text vertical-logo">', '\n<div class="brand-text vertical-logo">')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)
