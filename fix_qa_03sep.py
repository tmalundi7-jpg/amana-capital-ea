import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── FIX 1: index.html teaser headline ─────────────────────────────────────
c = open('index.html', encoding='utf-8').read()

# Show what's in h3 teaser-prem-title
idx = c.find('teaser-prem-title')
print("Current h3 teaser-prem-title:")
print(c[idx:idx+150])

# The headline as it appears in the wrap
HEADLINE = "A TZS 30 Billion Block Trade in CRDB Absorbed Without a Flinch — The Handoff is Complete"
DATE_LONG = "Thursday, 3rd September 2026"

# Replace the h3 teaser-prem-title — it may span multiple content types
c = re.sub(
    r'(<h3 class="teaser-prem-title">)(.*?)(</h3>)',
    rf'\g<1>Daily DSE Wrap | {DATE_LONG}\g<3>',
    c, flags=re.DOTALL)

# Also update the teaser-prem-body to contain intro with the headline mention
INTRO = ("The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on "
         "Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day "
         "figure in months. The driver was a single block trade in CRDB involving 11.2 million "
         "shares worth approximately TZS 30 billion, the largest such transaction in recent memory. "
         "Foreign investors sold nearly a third of the day's turnover, yet CRDB closed higher.")

c = re.sub(
    r'(<p class="teaser-prem-body">)(.*?)(</p>)',
    lambda m: m.group(1) + INTRO + m.group(3),
    c, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("  OK  index.html h3 + body updated")

# ── FIX 2: current-prices.html TCCL -4.0% ─────────────────────────────────
c2 = open('current-prices.html', encoding='utf-8').read()
idx2 = c2.find('TCCL')
if idx2 != -1:
    print(f"\nCurrent TCCL context:")
    print(repr(c2[idx2:idx2+200]))

# ── FIX 3: dse-wrap NBSP ─────────────────────────────────────────────────
c3 = open('dse-wrap-2026-09-03.html', encoding='utf-8').read()
cnt = c3.count('\xa0')
print(f"\nNBSP count in wrap: {cnt}")
c3 = c3.replace('\xa0', ' ')
with open('dse-wrap-2026-09-03.html', 'w', encoding='utf-8') as f:
    f.write(c3)
print("  OK  NBSP cleaned from wrap")
