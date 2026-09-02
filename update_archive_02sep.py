import re

out = []
files = [
    ('02 Sep 2026', 'dse-wrap-2026-09-02.html', 'Daily DSE Wrap | Wednesday, 2nd September 2026', 'The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion...'),
    ('01 Sep 2026', 'dse-wrap-2026-09-01.html', 'Daily DSE Wrap | Tuesday, 1st September 2026', 'The Dar es Salaam Stock Exchange began September with a session that may prove to be the most significant of the quarter. Equity turnover...')
]

for date_str, filename, title, excerpt in files:
    out.append(f'''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">{date_str}</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">{title}</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">{excerpt}</div></div>
<a href="/{filename.replace('.html', '')}" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>''')

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    archive = f.read()

insert_marker = '<div class="arc-row">'
parts = archive.split(insert_marker, 1)

new_archive = parts[0] + '\n'.join(out) + '\n' + insert_marker + parts[1]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(new_archive)

print("Inserted 02 Sep and 01 Sep into archive!")
