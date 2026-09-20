content = open('dse-wrap-2026-09-18.html', encoding='utf-8').read()
start = content.find('2. Top Movers')
end = content.find('3. In Focus')
print(content[start:end])
