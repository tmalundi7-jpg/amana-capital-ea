import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

m31 = re.search(r'<a class="archive-row" href="/dse-wrap-2026-08-31">.*?</a>', mi, flags=re.DOTALL)
m01 = re.search(r'<a class="archive-row" href="/dse-wrap-2026-09-01">.*?</a>', mi, flags=re.DOTALL)

if m31 and m01:
    s31 = m31.group(0)
    s01 = m01.group(0)
    
    # Simple replacement: Just extract the archive list content and put them in order
    archive_content = s01 + '\n' + s31
    
    # Remove old from mi
    mi = mi.replace(s31, '')
    mi = mi.replace(s01, '')
    
    # insert at archive-list
    mi = mi.replace('<div class="archive-list">', '<div class="archive-list">\n' + archive_content)
    
    with open('market-intelligence.html', 'w', encoding='utf-8') as f:
        f.write(mi)
    print('Swapped!')
else:
    print('Failed to find one of the rows')
