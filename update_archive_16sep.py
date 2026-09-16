
# Add 15 Sep 2026 wrap entry to market-intelligence-archive.html
# The previous wrap (15 Sep) needs to be at the top of the archive list

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if 15 Sep entry already exists
if 'dse-wrap-2026-09-15' in content:
    print('15 Sep entry already exists in archive - checking position...')
    idx = content.find('dse-wrap-2026-09-15')
    print('Found at:', idx)
    print('Context:', repr(content[idx-100:idx+300]))
else:
    print('15 Sep entry NOT in archive - will add it')
    # Find the first arc-row marker to insert before it
    marker = '<div class="arc-row">'
    idx = content.find(marker)
    if idx >= 0:
        new_entry = (
            '<div class="arc-row">\n'
            '<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">15 Sep 2026</div>\n'
            '<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Tuesday, 15th September 2026</div>'
            '<div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">Foreign Buyers Return as VODA Supply Evaporates. The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Tuesday. Equity turnover surged 166.5% to TZS 16.86 billion as foreign buyers returned in force...</div></div>\n'
            '<a href="/dse-wrap-2026-09-15" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>\n'
            '</div>\n'
        )
        content = content[:idx] + new_entry + content[idx:]
        print('Inserted 15 Sep entry at position:', idx)
        with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('market-intelligence-archive.html saved.')
    else:
        print('ERROR: arc-row marker not found!')
        # Show structure to diagnose
        print(content[2000:2600])
