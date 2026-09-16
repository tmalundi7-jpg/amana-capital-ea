import re
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()
match = re.search(r'<a[^>]+href="/current-prices"[^>]*>.*?</a>', c, flags=re.DOTALL)
if match:
    print(match.group(0))
