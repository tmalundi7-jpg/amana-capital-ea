with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

original = c
changes = []

def replace(old, new, label):
    global c
    if old in c:
        c = c.replace(old, new, 1)
        changes.append(f'[DONE] {label}')
    else:
        changes.append(f'[NOT FOUND] {label} — searched for: {repr(old[:80])}')

# 1. Snapshot subtitle date
replace(
    'End-of-day &middot; 3 September 2026</span>',
    'End-of-day &middot; 4 September 2026</span>',
    'Snapshot subtitle date'
)

# 2. DSEI value
replace(
    'id="home-dsei">4,442.62</div>',
    'id="home-dsei">4,523.81</div>',
    'DSEI value'
)

# 3. TSI value
replace(
    'id="home-tsi">9,653.89</div>',
    'id="home-tsi">9,826.80</div>',
    'TSI value'
)

# 4. Turnover value
replace(
    'id="home-turnover">TZS 42.93 bn</div>',
    'id="home-turnover">TZS 8.18 bn</div>',
    'Turnover value'
)

# 5. Gainers
replace(
    '<span>MBP <span style="color:var(--gain)">+8.2%</span></span>\n            <span>NMG <span style="color:var(--gain)">+7.9%</span></span>\n            <span>KCB <span style="color:var(--gain)">+3.9%</span></span>',
    '<span>KCB <span style="color:var(--gain)">+3.7%</span></span>\n            <span>NMB <span style="color:var(--gain)">+3.6%</span></span>\n            <span>MCB <span style="color:var(--gain)">+2.6%</span></span>',
    'Top Gainers'
)

# 6. Losers
replace(
    '<span>TCCL <span style="color:var(--loss)">-4.0%</span></span>\n            <span>TTP <span style="color:var(--loss)">-2.1%</span></span>\n            <span>DSE <span style="color:var(--loss)">-1.8%</span></span>',
    '<span>VODA <span style="color:var(--loss)">-1.9%</span></span>\n            <span>DSE <span style="color:var(--loss)">-1.4%</span></span>\n            <span>TOL <span style="color:var(--loss)">-0.5%</span></span>',
    'Top Losers'
)

# 7. Terminal Feed date
replace(
    'Terminal Feed | End-of-day &middot; 3 September 2026</div>',
    'Terminal Feed | End-of-day &middot; 4 September 2026</div>',
    'Terminal Feed date'
)

# 8. Teaser date
replace(
    '<div class="teaser-prem-date">Thursday, 3rd September 2026</div>',
    '<div class="teaser-prem-date">Friday, 4th September 2026</div>',
    'Teaser date'
)

# 9. Teaser title
replace(
    '<h3 class="teaser-prem-title">Daily DSE Wrap | Thursday, 3rd September 2026</h3>',
    '<h3 class="teaser-prem-title">Daily DSE Wrap | Friday, 4th September 2026</h3>',
    'Teaser title'
)

# 10. Teaser body text
replace(
    'The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion \u2014 the highest single-day figure in months. The driver was a single block trade in CRDB involving 11.2 million shares worth approximately TZS 30 billion, the largest such transaction in recent memory. Foreign investors sold nearly a third of the day\'s turnover, yet CRDB closed higher.',
    'The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730. The All-Share Index surged 81 points to 4,523.81, the highest level since the NMB share split recalibrated the index.',
    'Teaser body text'
)

# 11. Teaser DSEI stat value
replace(
    '<div class="teaser-prem-stat-value">4,442.62</div>',
    '<div class="teaser-prem-stat-value">4,523.81</div>',
    'Teaser DSEI stat'
)

# 12. Teaser Turnover stat value
replace(
    '<div class="teaser-prem-stat-value">TZS 42.93 bn</div>',
    '<div class="teaser-prem-stat-value">TZS 8.18 bn</div>',
    'Teaser Turnover stat'
)

# 13. Teaser Top Gainer (MBP -> KCB)
replace(
    '<span>MBP</span> <span style="color: #22c55e;">+8.2%</span>',
    '<span>KCB</span> <span style="color: #22c55e;">+3.7%</span>',
    'Teaser Top Gainer'
)

# 14. Teaser read link
replace(
    'href="/dse-wrap-2026-09-03">Read the Full Wrap',
    'href="/dse-wrap-2026-09-04">Read the Full Wrap',
    'Teaser read link'
)

# Write only if changes were made
if c != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("File written successfully.\n")
else:
    print("No changes made — file unchanged.\n")

for ch in changes:
    print(ch)
