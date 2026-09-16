import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
links = re.findall(r'href="([^"]+)"', c)
for l in links:
    print(l)
