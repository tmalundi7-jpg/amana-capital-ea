import sys

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

passes = 0
fails = 0

def check(label, condition):
    global passes, fails
    if condition:
        print(f'  [PASS] {label}')
        passes += 1
    else:
        print(f'  [FAIL] {label}')
        fails += 1

print('=== VERIFYING 04 SEPTEMBER DATA IN index.html ===\n')

print('--- Live DSE Snapshot ---')
check('Snapshot date: 4 September 2026', 'End-of-day &middot; 4 September 2026</span>' in c)
check('DSEI = 4,523.81', 'id="home-dsei">4,523.81</div>' in c)
check('TSI = 9,826.80', 'id="home-tsi">9,826.80</div>' in c)
check('Turnover = TZS 8.18 bn', 'id="home-turnover">TZS 8.18 bn</div>' in c)
check('Gainer 1: KCB +3.7%', 'KCB <span style="color:var(--gain)">+3.7%</span>' in c)
check('Gainer 2: NMB +3.6%', 'NMB <span style="color:var(--gain)">+3.6%</span>' in c)
check('Gainer 3: MCB +2.6%', 'MCB <span style="color:var(--gain)">+2.6%</span>' in c)
check('Loser 1: VODA -1.9%', 'VODA <span style="color:var(--loss)">-1.9%</span>' in c)
check('Loser 2: DSE -1.4%', 'DSE <span style="color:var(--loss)">-1.4%</span>' in c)
check('Loser 3: TOL -0.5%', 'TOL <span style="color:var(--loss)">-0.5%</span>' in c)
check('Terminal Feed date: 4 September 2026', 'End-of-day &middot; 4 September 2026</div>' in c)

print('\n--- Daily DSE Wrap Teaser ---')
check('Teaser date: Friday, 4th September 2026', 'teaser-prem-date">Friday, 4th September 2026</div>' in c)
check('Teaser title: 4th September 2026', 'Daily DSE Wrap | Friday, 4th September 2026</h3>' in c)
check('Teaser body mentions TZS 8.18 billion', 'TZS 8.18 billion' in c)
check('Teaser DSEI stat: 4,523.81', 'teaser-prem-stat-value">4,523.81</div>' in c)
check('Teaser Turnover stat: TZS 8.18 bn', 'teaser-prem-stat-value">TZS 8.18 bn</div>' in c)
check('Teaser Top Gainer: KCB', '<span>KCB</span>' in c)
check('Teaser Top Gainer: +3.7%', '+3.7%</span>' in c)
check('Teaser link: /dse-wrap-2026-09-04', 'href="/dse-wrap-2026-09-04">Read the Full Wrap' in c)

print('\n--- OLD values removed ---')
check('OLD DSEI 4,442.62 is gone', '4,442.62' not in c)
check('OLD Turnover TZS 42.93 bn is gone', 'TZS 42.93 bn' not in c)
check('OLD date 3 September 2026 is gone', '3 September 2026' not in c)
check('OLD gainer MBP +8.2% is gone', 'MBP <span style="color:var(--gain)">+8.2%</span>' not in c)
check('OLD loser TCCL -4.0% is gone', 'TCCL <span style="color:var(--loss)">-4.0%</span>' not in c)

print(f'\n=== RESULT: {passes} PASSED, {fails} FAILED ===')
if fails > 0:
    sys.exit(1)
