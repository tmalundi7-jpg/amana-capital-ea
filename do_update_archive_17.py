with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_block = '''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">17 Sep 2026</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Banks Under Pressure as a Massive NMB Block Trade Drives a 51% Turnover Surge</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Thursday. Equity turnover rose 51% to TZS 15.39 billion, driven by a massive block trade in NMB...</div></div>
<a href="/dse-wrap-2026-09-17" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>
'''

html = html.replace('<div class="arc-row">\n<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">16 Sep 2026</div>', new_block + '<div class="arc-row">\n<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">16 Sep 2026</div>')

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated market-intelligence-archive.html")

