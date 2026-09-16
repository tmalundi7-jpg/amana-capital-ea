import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'<a[^>]+href="([^"]*curren[^"]*)"', c)
print(matches)
