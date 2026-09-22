import re

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Dar es Salaam A Tanzania A Registration', 'Dar es Salaam &middot; Tanzania &middot; Registration')
content = content.replace('Ac 2026', '&copy; 2026')

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(content)
