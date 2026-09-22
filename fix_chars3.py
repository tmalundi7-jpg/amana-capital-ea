with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('A', '&middot;')
content = content.replace('Ac', '&copy;')

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(content)
