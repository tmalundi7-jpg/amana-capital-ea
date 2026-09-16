import re
with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()
print(re.findall(r'change-negative\">(.*?)</td>', text))
