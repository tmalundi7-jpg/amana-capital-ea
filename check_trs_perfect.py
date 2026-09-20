content = open('dse-wrap-2026-09-18.html', encoding='utf-8').read()
start = content.find('2. Top Movers')
end = content.find('3. In Focus')
table_html = content[start:end]
print("TRs in Top Movers:", table_html.count('<tr>') + table_html.count('<tr style='))
