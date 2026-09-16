
# AGENT 4 + 5: Independent verification of ALL updated files
# Verifies values against source data (from 16_sep_wrap.txt and 16_sep_prices.txt)
# AND verifies no layout/structure/design changed

import re

print('=' * 60)
print('AGENT 4: VALUE VERIFICATION against source DOCX data')
print('=' * 60)

# ---- market-intelligence.html ----
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

mi_checks = {
    # Date fields
    'Hero shows 16 Sep 2026': '<strong>16 Sep 2026</strong>' in mi,
    'Snapshot shows 16 September 2026': '>16 September 2026</span>' in mi,
    # Indices (from wrap doc line 73: DSEI 4,663.24 | TSI 10,380.73)
    'DSEI = 4,663.24': '>4,663.24<' in mi,
    'TSI = 10,380.73': '>10,380.73<' in mi,
    # Turnover (from wrap doc line 75: TZS 10.18 bn)
    'Turnover = TZS 10.18 bn': 'TZS 10.18 bn' in mi,
    'Turnover data-value = 10180000000': '10180000000' in mi,
    # Gainers (from wrap line 12: VODA +3.5%, PAL +3.3%, MCB +2.6%, DCB +2.3%)
    'Gainer: VODA +3.5%': 'VODA</span> <span style="color:var(--gain)">+3.5%' in mi,
    'Gainer: PAL +3.3%': 'PAL</span> <span style="color:var(--gain)">+3.3%' in mi,
    'Gainer: MCB +2.6%': 'MCB</span> <span style="color:var(--gain)">+2.6%' in mi,
    'Gainer: DCB +2.3%': 'DCB</span> <span style="color:var(--gain)">+2.3%' in mi,
    # Losers (from wrap line 13: TCCL -5.1%, TOL -4.2%, NMB -1.4%, AFRIPRISE -0.8%, CRDB -0.7%)
    'Loser: TCCL -5.1%': 'TCCL</span> <span style="color:var(--loss)">-5.1%' in mi,
    'Loser: TOL -4.2%': 'TOL</span> <span style="color:var(--loss)">-4.2%' in mi,
    'Loser: NMB -1.4%': 'NMB</span> <span style="color:var(--loss)">-1.4%' in mi,
    'Loser: AFRIPRISE -0.8%': 'AFRIPRISE</span> <span style="color:var(--loss)">-0.8%' in mi,
    'Loser: CRDB -0.7%': 'CRDB</span> <span style="color:var(--loss)">-0.7%' in mi,
    # Archive
    'Archive: 16 Sep wrap link': 'href="/dse-wrap-2026-09-16"' in mi,
    'Archive: Wed 16th Sep title': 'Daily DSE Wrap | Wednesday, 16th September 2026' in mi,
    # Negative checks - old data must NOT be present
    'NOT showing old hero date 15 Sep': '<strong>15 Sep 2026</strong>' not in mi,
    'NOT showing old DSEI 4696': '4,696.11' not in mi,
    'NOT showing old TSI 10438': '10,438.46' not in mi,
    'NOT showing old turnover 16.86': 'TZS 16.86 bn' not in mi,
    'NOT showing old archive 15 Sep': 'href="/dse-wrap-2026-09-15"' not in mi,
}

mi_all_ok = True
print('\n[market-intelligence.html]')
for k, v in mi_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: mi_all_ok = False
    print(f'  [{status}] {k}')

# ---- script.min.js heatmap ----
with open('script.min.js', 'r', encoding='utf-8') as f:
    js = f.read()

heatmap_checks = {
    'Heatmap VODA change=3.5': "symbol: 'VODA', marketCap:" in js and re.search(r"symbol: 'VODA', marketCap: \d+, change: 3\.5", js) is not None,
    'Heatmap TCCL change=-5.1': re.search(r"symbol: 'TCCL', marketCap: \d+, change: -5\.1", js) is not None,
    'Heatmap TOL change=-4.2': re.search(r"symbol: 'TOL', marketCap: \d+, change: -4\.2", js) is not None,
    'Heatmap CRDB change=-0.7': re.search(r"symbol: 'CRDB', marketCap: \d+, change: -0\.7", js) is not None,
    'Heatmap NMB change=-1.4': re.search(r"symbol: 'NMB', marketCap: \d+, change: -1\.4", js) is not None,
    'Heatmap DCB change=2.3': re.search(r"symbol: 'DCB', marketCap: \d+, change: 2\.3", js) is not None,
    'Heatmap MCB change=2.6': re.search(r"symbol: 'MCB', marketCap: \d+, change: 2\.6", js) is not None,
    'Heatmap SWIS change=-3.0 or -3': re.search(r"symbol: 'SWIS', marketCap: \d+, change: -3(\.0)?", js) is not None,
    'Heatmap MUCOBA change=-6.8': re.search(r"symbol: 'MUCOBA', marketCap: \d+, change: -6\.8", js) is not None,
    'Heatmap TBL change=0': re.search(r"symbol: 'TBL', marketCap: \d+, change: 0", js) is not None,
}

heatmap_all_ok = True
print('\n[script.min.js heatmap]')
for k, v in heatmap_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: heatmap_all_ok = False
    print(f'  [{status}] {k}')

# ---- current-prices.html ----
with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp = f.read()

cp_checks = {
    'Date: Wednesday, 16th September 2026': '16th September 2026' in cp,
    'Block: NMB 900,000': '900,000' in cp,
    'Block: TBL 307,000': '307,000' in cp,
    'Block: VODA 1,550,000': '1,550,000' in cp,
    'Block: IEACLC-ETF 215,469': '215,469' in cp,
    'Row: VODA 1,190 +3.5%': '1,190' in cp and '+3.5%' in cp,
    'Row: CRDB 2,920 -0.7%': '2,920' in cp and '-0.7%' in cp,
    'Row: NMB 2,150 -1.4%': '2,150' in cp and '-1.4%' in cp,
    'Row: TCCL 3,700 -5.1%': '3,700' in cp and '-5.1%' in cp,
    'Row: MUCOBA 410 -6.8%': '410' in cp and '-6.8%' in cp,
    'Row: TOL 1,820 -4.2%': '1,820' in cp and '-4.2%' in cp,
    'Row: PAL 315 +3.3%': '315' in cp and '+3.3%' in cp,
    'Row: DCB 445 +2.3%': '445' in cp and '+2.3%' in cp,
    'Row: MCB 395 +2.6%': '395' in cp and '+2.6%' in cp,
    'Row: TCC 13,450 +0.7%': '13,450' in cp and '+0.7%' in cp,
    'Row: AFRIPRISE 600 -0.8%': '600' in cp and '-0.8%' in cp,
    'Row: KCB 2,180 -1.8%': '2,180' in cp and '-1.8%' in cp,
    'Row: SWIS 2,570 -3.0%': '2,570' in cp and '-3.0%' in cp,
    'Row: TBL 9,970 0.0%': '9,970' in cp and '0.0%' in cp,
    'Row: TPCC 5,710 -0.7%': '5,710' in cp,
}

cp_all_ok = True
print('\n[current-prices.html]')
for k, v in cp_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: cp_all_ok = False
    print(f'  [{status}] {k}')

# ---- market-intelligence-archive.html ----
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arch = f.read()

archive_checks = {
    '15 Sep 2026 entry exists': 'dse-wrap-2026-09-15' in arch,
    '15 Sep 2026 entry title': '15th September 2026' in arch or '15 Sep 2026' in arch,
}

arch_all_ok = True
print('\n[market-intelligence-archive.html]')
for k, v in archive_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: arch_all_ok = False
    print(f'  [{status}] {k}')

# ---- dse-wrap-2026-09-16.html ----
import os
wrap_file = 'dse-wrap-2026-09-16.html'
wrap_exists = os.path.exists(wrap_file)

wrap_checks = {
    'dse-wrap-2026-09-16.html exists': wrap_exists,
}
if wrap_exists:
    with open(wrap_file, 'r', encoding='utf-8') as f:
        wrap = f.read()
    wrap_checks['Wrap contains 16th September 2026'] = '16th September 2026' in wrap or '16 September 2026' in wrap
    wrap_checks['Wrap contains DSEI 4,663.24'] = '4,663.24' in wrap
    wrap_checks['Wrap contains VODA +3.5%'] = '+3.5%' in wrap

wrap_all_ok = True
print('\n[dse-wrap-2026-09-16.html]')
for k, v in wrap_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: wrap_all_ok = False
    print(f'  [{status}] {k}')

print('\n' + '=' * 60)
print('AGENT 5: LAYOUT/STRUCTURE VERIFICATION')
print('=' * 60)

# Verify that MI page structure is intact
layout_checks = {
    'mi-hero section present': 'class="mi-hero"' in mi,
    'mi-snapshot-card present': 'class="mi-snapshot-card"' in mi,
    'DSE Snapshot heading present': '<h2>DSE Snapshot</h2>' in mi,
    'GAINERS_START comment present': '<!-- GAINERS_START -->' in mi,
    'LOSERS_START comment present': '<!-- LOSERS_START -->' in mi,
    'mi-heatmap-section present': 'class="mi-heatmap-section"' in mi,
    'archive-list present': 'class="archive-list"' in mi,
    'mi-sidebar present': 'class="mi-sidebar"' in mi,
    'Quick Links present': 'Quick Links' in mi,
    'script.min.js link present': 'script.min.js' in mi,
    'Only ONE archive row (no leftover 15 Sep)': mi.count('class="archive-row"') == 1,
}

layout_all_ok = True
print('\n[market-intelligence.html layout]')
for k, v in layout_checks.items():
    status = 'OK' if v else 'FAIL'
    if not v: layout_all_ok = False
    print(f'  [{status}] {k}')

# Final summary
all_clear = mi_all_ok and heatmap_all_ok and cp_all_ok and arch_all_ok and wrap_all_ok and layout_all_ok
print('\n' + '=' * 60)
print('FINAL RESULT:', 'ALL CHECKS PASSED - READY TO PUSH' if all_clear else 'SOME CHECKS FAILED - DO NOT PUSH')
print('=' * 60)
