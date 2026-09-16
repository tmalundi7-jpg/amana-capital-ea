with open('current-prices.html', 'rb') as f:
    text = f.read().decode('utf-8')
import re
match = re.search(r'change-negative\">(.*?)</td>', text)
if match:
    print(match.group(1).encode('utf-8'))
