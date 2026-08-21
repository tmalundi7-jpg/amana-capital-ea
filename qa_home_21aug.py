import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

minus = '\u2212'
fails = 0

def chk(label, condition):
    global fails
    status = 'PASS' if condition else 'FAIL'
    if not condition:
        fails += 1
    print(f'  [{status}] {label}')

print('=== HOME PAGE QA - 21 August 2026 ===\n')
print('--- NEW DATA (must PASS) ---')

chk('Hero DSEI value = 4,250.04',          '4,250.04' in html)
chk('Hero DSEI badge minus sign + 0.2%',   (minus + '0.2%') in html)
chk('Hero Turnover = TZS 1.38 billion',    'TZS 1.38 billion' in html)
chk('Hero Turnover badge minus + 56.3%',   (minus + '56.3%') in html)
chk('Hero Top Mover = MBP +2.8%',          'MBP +2.8%' in html)
chk('Hero date badge = 21 Aug 2026',       '21 Aug 2026' in html)
chk('Snapshot date = 21 August 2026',      '21 August 2026' in html)
chk('Snapshot DSEI = 4,250.04',            'home-dsei' in html and '4,250.04' in html)
chk('Snapshot TSI = 9,321.17',             '9,321.17' in html)
chk('Snapshot Turnover = 1.38 billion',    'TZS 1.38 billion' in html)
chk('Snapshot Gainer MBP +2.8%',          '+2.8%' in html)
chk('Snapshot Gainer DSE +2.2%',          '+2.2%' in html)
chk('Snapshot Gainer TOL +1.2%',          '+1.2%' in html)
chk('Snapshot Gainer MUCOBA +1.1%',       'MUCOBA' in html and '+1.1%' in html)
chk('Snapshot Loser DCB -9.0%',           '-9.0%' in html)
chk('Snapshot Loser TTP -5.0%',           'TTP' in html and '-5.0%' in html)
chk('Snapshot Loser NICO -3.8%',          'NICO' in html and '-3.8%' in html)
chk('Snapshot Loser MCB -3.4%',           '-3.4%' in html)
chk('Snapshot footer date 21 Aug',        'End-of-day, 21 August 2026' in html)
chk('Teaser date Friday 21st Aug 2026',   'Friday, 21st August 2026' in html)
chk('Teaser title A Quiet End...',        'A Quiet End to the Week' in html)
chk('Teaser body DSEI slipping 6.91',     'slipping 6.91 points' in html)
chk('Teaser DSEI stat = 4,250.04',        'teaser-prem-stat-value' in html and '4,250.04' in html)
chk('Teaser Turnover stat = 1.38 bn',     'TZS 1.38 billion' in html)
chk('Teaser Top Gainer MBP +2.8%',       'MBP +2.8%' in html)
chk('Teaser link = dse-wrap-2026-08-21',  'dse-wrap-2026-08-21' in html)

print('\n--- OLD DATA (must be GONE) ---')
chk('20 Aug DSEI 4256.95 gone',           '4,256.95' not in html)
chk('20 Aug TSI 9343.34 gone',            '9,343.34' not in html)
chk('20 Aug Turnover 3.16bn gone',        '3.16 billion' not in html)
chk('20 Aug TCCL +7.8% gone',            'TCCL +7.8%' not in html)
chk('20 Aug date badge "20 Aug 2026" gone', '20 Aug 2026' not in html)
chk('20th August 2026 teaser date gone',  '20th August 2026' not in html)
chk('20 Aug wrap link gone from teaser',  '/dse-wrap-2026-08-20' not in html)
chk('DCB -11.2% gone from snapshot',      '-11.2%' not in html)
chk('DSE -3.1% gone from snapshot',       '-3.1%' not in html)
chk('MKCB -0.8% gone from snapshot',      '-0.8%' not in html)
chk('20 Aug date "20 August 2026" gone',  '20 August 2026' not in html)

print()
result = 'ALL PASS' if fails == 0 else f'{fails} FAILURE(S) DETECTED'
print(f'=== RESULT: {result} ===')
sys.exit(0 if fails == 0 else 1)
