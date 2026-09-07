import sys

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

fails = 0
def check(label, cond):
    global fails
    if cond: print(f'[PASS] {label}')
    else: print(f'[FAIL] {label}'); fails += 1

print('--- market-intelligence.html ---')
check('Hero date', '04 Sep 2026' in c)
check('Snapshot date', '4 September 2026' in c)
check('DSEI', '4,523.81' in c)
check('Turnover', 'TZS 8.18 bn' in c)
check('KCB gainer', 'KCB</span> <span style="color:var(--gain)">+3.7%' in c)
check('VODA loser', 'VODA</span> <span style="color:var(--loss)">-1.9%' in c)
check('Featured wrap', 'dse-wrap-2026-09-04' in c)

with open('current-prices.html', 'r', encoding='utf-8') as f:
    cp = f.read()

print('\n--- current-prices.html ---')
check('Table has CRDB +1.9%', 'CRDB Bank</td><td>Banks & Finance</td><td class="price-cell">2,730</td><td class="change-positive">+1.9%' in cp)
check('Table has KCB +3.7%', 'KCB Group (cross-listed)</td><td>Banks & Finance</td><td class="price-cell">2,220</td><td class="change-positive">+3.7%' in cp)
check('Date is 4th September', '4th September 2026' in cp)

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc = f.read()
print('\n--- market-intelligence-archive.html ---')
check('Has 03 Sep wrap', '03 Sep 2026' in arc and 'dse-wrap-2026-09-03' in arc)

if fails > 0: sys.exit(1)
