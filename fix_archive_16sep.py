
# AGENT 3 - Fix archive row and finalize market-intelligence.html

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The file uses \n line endings (not \r\n) - fix archive row
archive_old = (
    '<a class="archive-row" href="/dse-wrap-2026-09-15">\n'
    '<div class="archive-date">15 Sep<br/>2026</div>\n'
    '<div>\n'
    '<div class="archive-badge badge-equity">Equities</div>\n'
    '<div class="archive-content-title">Daily DSE Wrap | Tuesday, 15th September 2026</div>\n'
    '<div class="archive-content-excerpt">Foreign Buyers Return as VODA Supply Evaporates \u2013 But Not Every Stock Tells the Same Story. The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Tuesday. Equity turnover surged 166.5%...</div>\n'
    '</div>\n'
    '<span class="archive-cta">Read &rarr;</span>\n'
    '</a>'
)

archive_new = (
    '<a class="archive-row" href="/dse-wrap-2026-09-16">\n'
    '<div class="archive-date">16 Sep<br/>2026</div>\n'
    '<div>\n'
    '<div class="archive-badge badge-equity">Equities</div>\n'
    '<div class="archive-content-title">Daily DSE Wrap | Wednesday, 16th September 2026</div>\n'
    '<div class="archive-content-excerpt">Order Books Tell Divergent Stories as Foreign Flows Hit Record Two-Way Levels. The Dar es Salaam Stock Exchange delivered a session of remarkable contrasts on Wednesday. Equity turnover moderated to TZS 10.18 billion as foreign participation surged to record two-way levels...</div>\n'
    '</div>\n'
    '<span class="archive-cta">Read &rarr;</span>\n'
    '</a>'
)

if archive_old in content:
    content = content.replace(archive_old, archive_new)
    print('Archive row replaced OK')
else:
    print('ERROR: archive_old still not found')
    import re
    m = re.search(r'href="/dse-wrap-2026-09-15"', content)
    if m:
        print('SNIPPET:', repr(content[m.start()-50:m.start()+400]))

# Final verification
checks = {
    'Hero date 16 Sep': '<strong>16 Sep 2026</strong>' in content,
    'Snapshot date 16 Sep': '>16 September 2026</span>' in content,
    'DSEI 4663.24': '>4,663.24<' in content,
    'TSI 10380.73': '>10,380.73<' in content,
    'Turnover 10.18bn': '10180000000' in content,
    'Gainer VODA +3.5%': '+3.5%' in content,
    'Gainer PAL +3.3%': '+3.3%' in content,
    'Loser TCCL -5.1%': '-5.1%' in content,
    'Loser TOL -4.2%': '-4.2%' in content,
    'Archive 16 Sep link': 'dse-wrap-2026-09-16' in content,
    'Old 15 Sep hero NOT present': '<strong>15 Sep 2026</strong>' not in content,
    'Old 15 Sep archive NOT present': 'href="/dse-wrap-2026-09-15"' not in content,
}

print('\n=== FINAL VERIFICATION ===')
all_ok = True
for k, v in checks.items():
    status = 'OK' if v else 'FAIL'
    if not v:
        all_ok = False
    print(f'  [{status}] {k}')

if all_ok:
    with open('market-intelligence.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('\nAll checks passed. market-intelligence.html saved.')
else:
    print('\nSome checks FAILED. File NOT saved.')
