import re

files = [
    ('31 Aug 2026', 'dse-wrap-2026-08-31.html'),
    ('28 Aug 2026', 'dse-wrap-2026-08-28.html'),
    ('27 Aug 2026', 'dse-wrap-2026-08-27.html')
]

out = []
for date_str, filename in files:
    try:
        content = open(filename, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f'Error reading {filename}')
        continue
        
    m_title = re.search(r'<p style="font-size: 1.1rem; color: var\(--mist\); margin-bottom: 0; font-weight: 600;">(.*?)</p>', content)
    
    title = m_title.group(1) if m_title else 'Daily Wrap'
    title = re.sub(r'<[^>]+>', '', title).strip()
    
    m_excerpt = re.search(r'<p>(The Dar es Salaam Stock Exchange.*?)</p>', content)
    excerpt = m_excerpt.group(1) if m_excerpt else 'The Dar es Salaam Stock Exchange delivered another session...'
    excerpt = re.sub(r'<[^>]+>', '', excerpt).strip()
    if len(excerpt) > 140:
        excerpt = excerpt[:140] + '...'
        
    out.append(f'''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">{date_str}</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">{title}</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">{excerpt}</div></div>
<a href="/{filename.replace('.html', '')}" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>''')

# Now insert it into market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    archive = f.read()

# find where to insert
insert_marker = '<div class="arc-row">'
parts = archive.split(insert_marker, 1)

new_archive = parts[0] + '\n'.join(out) + '\n' + insert_marker + parts[1]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(new_archive)

print("Inserted into archive!")
