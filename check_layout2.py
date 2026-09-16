
with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('Pre-Arranged Board')
print(content[idx-100:idx+800])
