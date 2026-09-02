import re
c = open('current-prices.html', 'r', encoding='utf-8').read()
matches = re.findall(r'<div class="[^"]*value[^"]*">(.*?)</div>', c)
print(matches)
