import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    'TZS 6.84 billion',
    'DCB +13.2%',
    '18th August 2026',
    'End-of-day · 18 August 2026',
    'End-of-day, 18 August 2026',
    'DCB <span style=\"color:var(--gain)\">+13.2%</span>',
    'MCB <span style=\"color:var(--gain)\">+3.7%</span>',
    'KCB <span style=\"color:var(--gain)\">+1.0%</span>',
    'NICO <span style=\"color:var(--gain)\">+0.8%</span>',
    'TCCL <span style=\"color:var(--loss)\">-3.6%</span>',
    'TBL <span style=\"color:var(--loss)\">-1.4%</span>',
    'SWIS <span style=\"color:var(--loss)\">-0.8%</span>',
    'CRDB <span style=\"color:var(--loss)\">-0.4%</span>',
    'Tuesday, 18th August 2026'
]

for check in checks:
    if check in text:
        print(f'PASS: {check}')
    else:
        print(f'FAIL: {check}')
