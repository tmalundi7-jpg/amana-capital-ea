
# AGENT 3 - Complete update of market-intelligence.html for 16 Sep 2026
# Applies ALL changes atomically in one pass

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('File loaded. Length:', len(content))

# Detect line ending
has_crlf = '\r\n' in content
print('CRLF line endings:', has_crlf)

# Normalize to \n for reliable string matching
content = content.replace('\r\n', '\n')

# ---- 1. Hero date ----
old = '<strong>15 Sep 2026</strong>'
new = '<strong>16 Sep 2026</strong>'
if old in content:
    content = content.replace(old, new)
    print('OK: Hero date')
else:
    print('FAIL: Hero date not found')

# ---- 2. Snapshot date ----
old = '>15 September 2026</span>'
new = '>16 September 2026</span>'
if old in content:
    content = content.replace(old, new)
    print('OK: Snapshot date')
else:
    print('FAIL: Snapshot date not found')

# ---- 3. DSEI ----
old = '<div class="snapshot-value" id="mi-dsei">4,696.11</div>'
new = '<div class="snapshot-value" id="mi-dsei">4,663.24</div>'
if old in content:
    content = content.replace(old, new)
    print('OK: DSEI')
else:
    print('FAIL: DSEI not found')

# ---- 4. TSI ----
old = '<div class="snapshot-value" id="mi-tsi">10,438.46</div>'
new = '<div class="snapshot-value" id="mi-tsi">10,380.73</div>'
if old in content:
    content = content.replace(old, new)
    print('OK: TSI')
else:
    print('FAIL: TSI not found')

# ---- 5. Turnover ----
old = 'data-tzs-value="16860000000" id="mi-turnover">TZS 16.86 bn'
new = 'data-tzs-value="10180000000" id="mi-turnover">TZS 10.18 bn'
if old in content:
    content = content.replace(old, new)
    print('OK: Turnover')
else:
    print('FAIL: Turnover not found')

# ---- 6. Top Gainers ----
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
    print('OK: Gainers')
else:
    print('FAIL: Gainers block not found')

# ---- 7. Top Losers ----
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
    print('OK: Losers')
else:
    print('FAIL: Losers block not found')

# ---- 8. Archive row ----
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
    print('OK: Archive row')
else:
    print('FAIL: Archive row not found - dumping context...')
    import re
    m = re.search(r'href="/dse-wrap-2026-09-15"', content)
    if m:
        print(repr(content[m.start()-10:m.start()+300]))

# ---- Restore CRLF if original had it ----
if has_crlf:
    content = content.replace('\n', '\r\n')
    print('Restored CRLF line endings')

# ---- Final checks ----
# Search in LF-normalized form for checks
check_content = content.replace('\r\n', '\n')
checks = {
    'Hero date 16 Sep': '<strong>16 Sep 2026</strong>' in check_content,
    'Snapshot date 16 Sep': '>16 September 2026</span>' in check_content,
    'DSEI 4663.24': '>4,663.24<' in check_content,
    'TSI 10380.73': '>10,380.73<' in check_content,
    'Turnover 10.18bn': '10180000000' in check_content,
    'Gainer VODA +3.5%': '+3.5%' in check_content,
    'Gainer PAL +3.3%': '+3.3%' in check_content,
    'Loser TCCL -5.1%': '-5.1%' in check_content,
    'Loser TOL -4.2%': '-4.2%' in check_content,
    'Archive 16 Sep link': 'dse-wrap-2026-09-16' in check_content,
    'Old 15 Sep hero NOT present': '<strong>15 Sep 2026</strong>' not in check_content,
    'Old 15 Sep archive NOT present': 'href="/dse-wrap-2026-09-15"' not in check_content,
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
    print('\nAll checks passed. market-intelligence.html SAVED.')
else:
    print('\nSome checks FAILED. File NOT saved.')
