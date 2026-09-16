with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\ufffd', '-')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\ufffd', '-')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
