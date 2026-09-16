with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('change-negative\\\">', 'change-negative\">')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(text)
