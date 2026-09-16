
# AGENT 3 - Apply all content-only updates to market-intelligence.html for 16 Sep 2026

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hero date
content = content.replace('<strong>15 Sep 2026</strong>', '<strong>16 Sep 2026</strong>')

# 2. Snapshot date
content = content.replace('>15 September 2026</span>', '>16 September 2026</span>')

# 3. DSEI value
content = content.replace(
    '<div class="snapshot-value" id="mi-dsei">4,696.11</div>',
    '<div class="snapshot-value" id="mi-dsei">4,663.24</div>'
)

# 4. TSI value
content = content.replace(
    '<div class="snapshot-value" id="mi-tsi">10,438.46</div>',
    '<div class="snapshot-value" id="mi-tsi">10,380.73</div>'
)

# 5. Turnover
content = content.replace(
    'data-tzs-value="16860000000" id="mi-turnover">TZS 16.86 bn',
    'data-tzs-value="10180000000" id="mi-turnover">TZS 10.18 bn'
)

# 6. Top Gainers block
gainers_old = (
    '  <!-- GAINERS_START -->\n'
    '      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+3.6%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--gain)">+2.6%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--gain)">+2.2%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+0.9%</span></div>\n'
    '      </div>\n'
    '      <!-- GAINERS_END -->'
)

gainers_new = (
    '  <!-- GAINERS_START -->\n'
    '      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+3.5%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>PAL</span> <span style="color:var(--gain)">+3.3%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+2.6%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DCB</span> <span style="color:var(--gain)">+2.3%</span></div>\n'
    '      </div>\n'
    '      <!-- GAINERS_END -->'
)

if gainers_old in content:
    content = content.replace(gainers_old, gainers_new)
    print('Gainers replaced OK')
else:
    print('WARNING: gainers_old not found - checking whitespace variant...')
    # Try with \r\n
    gainers_old_crlf = gainers_old.replace('\n', '\r\n')
    if gainers_old_crlf in content:
        gainers_new_crlf = gainers_new.replace('\n', '\r\n')
        content = content.replace(gainers_old_crlf, gainers_new_crlf)
        print('Gainers replaced OK (CRLF)')
    else:
        print('ERROR: gainers block not found at all')

# 7. Top Losers block
losers_old = (
    '  <!-- LOSERS_START -->\n'
    '      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DCB</span> <span style="color:var(--loss)">-3.3%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--loss)">-2.5%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>CRDB</span> <span style="color:var(--loss)">-1.4%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.1%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCC</span> <span style="color:var(--loss)">-1.0%</span></div>\n'
    '      </div>\n'
    '      <!-- LOSERS_END -->'
)

losers_new = (
    '  <!-- LOSERS_START -->\n'
    '      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--loss)">-5.1%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-4.2%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--loss)">-1.4%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>AFRIPRISE</span> <span style="color:var(--loss)">-0.8%</span></div>\n'
    '        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>CRDB</span> <span style="color:var(--loss)">-0.7%</span></div>\n'
    '      </div>\n'
    '      <!-- LOSERS_END -->'
)

if losers_old in content:
    content = content.replace(losers_old, losers_new)
    print('Losers replaced OK')
else:
    losers_old_crlf = losers_old.replace('\n', '\r\n')
    if losers_old_crlf in content:
        losers_new_crlf = losers_new.replace('\n', '\r\n')
        content = content.replace(losers_old_crlf, losers_new_crlf)
        print('Losers replaced OK (CRLF)')
    else:
        print('ERROR: losers block not found')

# 8. Archive row - replace 15 Sep row with 16 Sep row
archive_old = (
    '<a class="archive-row" href="/dse-wrap-2026-09-15">\r\n'
    '<div class="archive-date">15 Sep<br/>2026</div>\r\n'
    '<div>\r\n'
    '<div class="archive-badge badge-equity">Equities</div>\r\n'
    '<div class="archive-content-title">Daily DSE Wrap | Tuesday, 15th September 2026</div>\r\n'
    '<div class="archive-content-excerpt">Foreign Buyers Return as VODA Supply Evaporates \u2013 But Not Every Stock Tells the Same Story. The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Tuesday. Equity turnover surged 166.5%...</div>\r\n'
    '</div>\r\n'
    '<span class="archive-cta">Read &rarr;</span>\r\n'
    '</a>'
)

archive_new = (
    '<a class="archive-row" href="/dse-wrap-2026-09-16">\r\n'
    '<div class="archive-date">16 Sep<br/>2026</div>\r\n'
    '<div>\r\n'
    '<div class="archive-badge badge-equity">Equities</div>\r\n'
    '<div class="archive-content-title">Daily DSE Wrap | Wednesday, 16th September 2026</div>\r\n'
    '<div class="archive-content-excerpt">Order Books Tell Divergent Stories as Foreign Flows Hit Record Two-Way Levels. The Dar es Salaam Stock Exchange delivered a session of remarkable contrasts on Wednesday. Equity turnover moderated to TZS 10.18 billion as foreign participation surged to record two-way levels...</div>\r\n'
    '</div>\r\n'
    '<span class="archive-cta">Read &rarr;</span>\r\n'
    '</a>'
)

if archive_old in content:
    content = content.replace(archive_old, archive_new)
    print('Archive row replaced OK')
else:
    print('WARNING: archive_old not found - trying grep...')
    import re
    m = re.search(r'archive-row.*?dse-wrap-2026-09-15.*?</a>', content, re.DOTALL)
    if m:
        print('Found archive section at:', m.start(), '-', m.end())
        print('SNIPPET:', repr(content[m.start():m.start()+200]))
    else:
        print('ERROR: archive section not found')

# Verify
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
}

print('\n=== VERIFICATION ===')
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
