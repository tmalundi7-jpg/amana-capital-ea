import re

with open('dse-wrap-2026-08-31.html', 'r', encoding='utf-8') as f:
    content = f.read()

m_excerpt = re.search(r'<p>(The Dar es Salaam Stock Exchange.*?)</p>', content)
excerpt = m_excerpt.group(1) if m_excerpt else 'The Dar es Salaam Stock Exchange delivered another session...'
excerpt = re.sub(r'<[^>]+>', '', excerpt).strip()
if len(excerpt) > 140:
    excerpt = excerpt[:140] + '...'

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

new_row = f'''<a class="archive-row" href="/dse-wrap-2026-08-31">
<div class="archive-date">31 Aug<br/>2026</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | Monday, 31 August 2026</div>
<div class="archive-content-excerpt">{excerpt}</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>'''

mi = re.sub(r'(<div class="archive-list">\s*)', r'\g<1>' + new_row + '\n', mi)
with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi)

print('Updated market-intelligence.html')
