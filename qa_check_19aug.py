
def check(label, found):
    status = 'PASS' if found else 'FAIL'
    print(f'  [{status}] {label}')
    return found

def fc(path, text):
    with open(path, encoding='utf-8', errors='replace') as f:
        content = f.read()
    return text in content

def fnc(path, text):
    return not fc(path, text)

base = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea'
mi   = base + r'\market-intelligence.html'
arc  = base + r'\market-intelligence-archive.html'
cp   = base + r'\current-prices.html'
js   = base + r'\script.min.js'

all_pass = True

print('=== market-intelligence.html QA ===')
results = [
    # Archive section: only ONE wrap entry (19-Aug)
    check('Archive: only 19 Aug entry present',    fc(mi, 'dse-wrap-2026-08-19')),
    check('Archive: 17 Aug entry REMOVED',         fnc(mi, 'dse-wrap-2026-08-17')),
    check('Archive list headline correct',         fc(mi, 'Market Holds Firm as Block Trades Continue')),
    # Heatmap section present
    check('Heatmap section present',               fc(mi, 'DSE Market Heatmap')),
    # Snapshot values still correct from previous task
    check('Snapshot DSEI 4,255.50',               fc(mi, '4,255.50')),
    check('Snapshot TSI 9,327.78',                fc(mi, '9,327.78')),
    check('Snapshot Turnover 7.15 bn',            fc(mi, '7.15 bn')),
    check('Snapshot date 19 August 2026',         fc(mi, '19 August 2026')),
    check('Latest report 19 Aug 2026',            fc(mi, '<strong>19 Aug 2026</strong>')),
    check('Gainer MBP +9.9%',                    fc(mi, 'MBP')),
    check('Loser TCCL -3.9%',                    fc(mi, 'TCCL')),
    # Ensure old 18-Aug wrap is NOT in archive section
    check('NO 18-Aug in archive section',         fnc(mi, 'dse-wrap-2026-08-18')),
]
all_pass = all_pass and all(results)

print()
print('=== market-intelligence-archive.html QA ===')
results2 = [
    check('19 Aug entry at top of archive',       fc(arc, 'dse-wrap-2026-08-19')),
    check('19 Aug headline in archive',           fc(arc, 'Market Holds Firm as Block Trades Continue')),
    check('18 Aug still in archive',              fc(arc, 'dse-wrap-2026-08-18')),
    check('17 Aug added to archive',              fc(arc, 'dse-wrap-2026-08-17')),
    check('17 Aug headline correct',              fc(arc, "DCB's Block Trade and the Power of Local Demand")),
    check('14 Aug still in archive',              fc(arc, 'dse-wrap-2026-08-14')),
    check('19 Aug appears BEFORE 18 Aug',         arc and (open(arc, encoding='utf-8', errors='replace').read().index('08-19') < open(arc, encoding='utf-8', errors='replace').read().index('08-18'))),
    check('17 Aug appears AFTER 18 Aug',          arc and (open(arc, encoding='utf-8', errors='replace').read().index('08-17') > open(arc, encoding='utf-8', errors='replace').read().index('08-18'))),
    check('17 Aug appears BEFORE 14 Aug',         arc and (open(arc, encoding='utf-8', errors='replace').read().index('08-17') < open(arc, encoding='utf-8', errors='replace').read().index('08-14'))),
]
all_pass = all_pass and all(results2)

print()
print('=== current-prices.html QA ===')
results3 = [
    # Date header
    check('Date: 19 August 2026',               fc(cp, 'End-of-Day, 19 August 2026')),
    check('NO old date 18 August',              fnc(cp, 'End-of-Day, 18 August 2026')),
    # 19 Aug data present
    check('AFRIPRISE 615 -1.6%',               fc(cp, '>615<') and fc(cp, '&#8211;1.6%')),
    check('CRDB 2,690 +0.4%',                  fc(cp, '>2,690<') and fc(cp, '>+0.4%<')),
    check('DCB 625 +4.2%',                     fc(cp, '>625<') and fc(cp, '>+4.2%<')),
    check('DSE 6,540 +1.6%',                   fc(cp, '>6,540<') and fc(cp, '>+1.6%<')),
    check('JATU 270 +1.9%',                    fc(cp, '>270<') and fc(cp, '>+1.9%<')),
    check('KCB 1,980 0.0%',                    fc(cp, '>1,980<')),
    check('MBP 1,770 +9.9%',                   fc(cp, '>1,770<') and fc(cp, '>+9.9%<')),
    check('MCB 450 +7.1%',                     fc(cp, '>450<') and fc(cp, '>+7.1%<')),
    check('MKCB 3,770 +1.3%',                  fc(cp, '>3,770<') and fc(cp, '>+1.3%<')),
    check('MUCOBA 450 0.0%',                   fc(cp, 'MUCOBA')),
    check('NICO 4,000 -0.5%',                  fc(cp, '>4,000<') and fc(cp, '&#8211;0.5%')),
    check('NMB 17,700 0.0%',                   fc(cp, '>17,700<')),
    check('PAL 305 -4.7%',                     fc(cp, '>305<') and fc(cp, '&#8211;4.7%')),
    check('SWIS 2,560 0.0%',                   fc(cp, '>2,560<')),
    check('TBL 9,870 +0.7%',                   fc(cp, '>9,870<') and fc(cp, '>+0.7%<')),
    check('TCC 12,520 0.0%',                   fc(cp, '>12,520<')),
    check('TCCL 3,710 -3.9%',                  fc(cp, '>3,710<') and fc(cp, '&#8211;3.9%')),
    check('TOL 1,690 +7.0%',                   fc(cp, '>1,690<') and fc(cp, '>+7.0%<')),
    check('TPCC 6,000 -0.5%',                  fc(cp, '>6,000<')),
    check('TTP 500 0.0%',                      fc(cp, '>500<')),
    check('VODA 1,030 0.0%',                   fc(cp, '>1,030<')),
    # Footnote updated
    check('Footnote: CRDB block trade',        fc(cp, '150,000-share block trade in CRDB')),
    check('Footnote: KCB block trade',         fc(cp, '253,019-share block trade in KCB')),
    check('NO old NICO footnote',              fnc(cp, '19,185')),
    # Old 18-Aug data NOT present
    check('NO old CRDB 2,680',               fnc(cp, '>2,680<')),
    check('NO old DCB 600 +13.2%',           fnc(cp, '>+13.2%<')),
    check('NO old MBP 1,610 -4.7%',         fnc(cp, '>1,610<')),
    check('NO old TBL 9,800',               fnc(cp, '>9,800<')),
    check('NO old TCCL -3.5%',             fnc(cp, '>-3.5%<') and fnc(cp, '&#8211;3.5%')),
    check('NO old TOL 1,580',               fnc(cp, '>1,580<')),
    check('NO old TPCC 6,030',             fnc(cp, '>6,030<')),
    check('NO old DSE 6,440',              fnc(cp, '>6,440<')),
    check('NO old PAL 320 0.0%',          fnc(cp, '>320<')),
]
all_pass = all_pass and all(results3)

print()
print('=== script.min.js Heatmap QA ===')
results4 = [
    check('Heatmap function present',           fc(js, 'initDSEHeatmap')),
    check('TBL 0.7% change',                   fc(js, "symbol: 'TBL'") and fc(js, 'change:  0.7')),
    check('NMB 0.0% change',                   fc(js, "symbol: 'NMB'") and fc(js, "change:  0.0")),
    check('CRDB 0.4% change',                  fc(js, "symbol: 'CRDB'") and fc(js, 'change:  0.4')),
    check('VODA 0.0% change',                  fc(js, "symbol: 'VODA'")),
    check('KCB added to heatmap',              fc(js, "symbol: 'KCB'")),
    check('NICO added to heatmap',             fc(js, "symbol: 'NICO'")),
    check('DSE 1.6% change',                   fc(js, "symbol: 'DSE'") and fc(js, 'change:  1.6')),
    check('TCCL -3.9% change',                 fc(js, "symbol: 'TCCL'") and fc(js, 'change: -3.9')),
    check('MBP 9.9% change',                   fc(js, "symbol: 'MBP'") and fc(js, 'change:  9.9')),
    check('MCB 7.1% change',                   fc(js, "symbol: 'MCB'") and fc(js, 'change:  7.1')),
    check('TOL 6.9% change',                   fc(js, "symbol: 'TOL'") and fc(js, 'change:  6.9')),
    check('DCB 4.2% change',                   fc(js, "symbol: 'DCB'") and fc(js, 'change:  4.2')),
    check('PAL -4.7% change',                  fc(js, "symbol: 'PAL'") and fc(js, 'change: -4.7')),
    check('AFRIPRISE -1.6% change',            fc(js, "symbol: 'AFRIPRISE'") and fc(js, 'change: -1.6')),
    check('NO old DCB 14.0%',                  fnc(js, 'change: 14.0')),
    check('NO old TTP 11.1%',                  fnc(js, 'change: 11.1')),
    check('NO old KA 9.1%',                    fnc(js, "'KA'")),
    check('NO old PAL -7.2%',                  fnc(js, 'change: -7.2')),
    check('NO old CRDB -0.4%',                 fnc(js, 'change: -0.4')),
    check('NO old MUCOBA -1.1%',              fnc(js, 'change: -1.1')),
]
all_pass = all_pass and all(results4)

print()
if all_pass:
    print('OVERALL RESULT: ALL CHECKS PASSED')
else:
    print('OVERALL RESULT: SOME CHECKS FAILED - review above')
