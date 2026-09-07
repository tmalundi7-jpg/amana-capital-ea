import re
import mammoth
from bs4 import BeautifulSoup

# ── Data from source documents ──────────────────────────────────────────────
DATE_LONG      = "Thursday, 3rd September 2026"
DATE_ORDINAL   = "Thursday, 3rd September 2026"
DATE_SHORT     = "03 Sep 2026"
YYYY_MM_DD     = "2026-09-03"
DSEI           = "4,442.62"
TSI            = "9,653.89"
TURNOVER       = "TZS 42.93 bn"
SHARES         = "14,412,543"
DEALS          = "1,326"

GAINERS = [
    ("MBP",  "+8.2%"),
    ("NMG",  "+7.9%"),
    ("KCB",  "+3.9%"),
]
LOSERS = [
    ("TCCL", "-4.0%"),
    ("TTP",  "-2.1%"),
    ("DSE",  "-1.8%"),
]

HEADLINE = "A TZS 30 Billion Block Trade in CRDB Absorbed Without a Flinch — The Handoff is Complete"
INTRO    = ("The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on "
            "Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day "
            "figure in months. The driver was a single block trade in CRDB involving 11.2 million shares "
            "worth approximately TZS 30 billion, the largest such transaction in recent memory. Foreign "
            "investors sold nearly a third of the day's turnover, yet CRDB closed higher.")

WRAP_URL = "/dse-wrap-2026-09-03"

# ── Helper: write changed file ───────────────────────────────────────────────
def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✔  Updated {path}")


# ═══════════════════════════════════════════════════════════════════════════
# 1.  index.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── index.html ──")
c = read("index.html")

# Snapshot date labels
c = re.sub(r'(id="snapshot-date"[^>]*>)[^<]*(</)', r'\g<1>As of ' + DATE_LONG + r'\2', c)
c = re.sub(r'(id="terminal-date"[^>]*>)[^<]*(</)', r'\g<1>' + DATE_LONG + r'\2', c)

# Core metrics
c = re.sub(r'(id="home-dsei"[^>]*>)[^<]*(</)', r'\g<1>' + DSEI + r'\2', c)
c = re.sub(r'(id="home-tsi"[^>]*>)[^<]*(</)',  r'\g<1>' + TSI  + r'\2', c)
c = re.sub(r'(id="home-turnover"[^>]*>)[^<]*(</)', r'\g<1>' + TURNOVER + r'\2', c)

# Gainers (just update inner spans, never touch outer divs)
for i, (ticker, change) in enumerate(GAINERS, 1):
    c = re.sub(
        rf'(id="home-gainer-{i}-ticker"[^>]*>)[^<]*(</)',
        rf'\g<1>{ticker}\2', c)
    c = re.sub(
        rf'(id="home-gainer-{i}-change"[^>]*>)[^<]*(</)',
        rf'\g<1>{change}\2', c)

# Losers
for i, (ticker, change) in enumerate(LOSERS, 1):
    c = re.sub(
        rf'(id="home-loser-{i}-ticker"[^>]*>)[^<]*(</)',
        rf'\g<1>{ticker}\2', c)
    c = re.sub(
        rf'(id="home-loser-{i}-change"[^>]*>)[^<]*(</)',
        rf'\g<1>{change}\2', c)

# Bottom teaser
c = re.sub(r'(id="teaser-date"[^>]*>)[^<]*(</)', r'\g<1>' + DATE_LONG + r'\2', c)
c = re.sub(r'(id="teaser-title"[^>]*>)[^<]*(</)', r'\g<1>' + HEADLINE + r'\2', c)
c = re.sub(r'(id="teaser-intro"[^>]*>)[^<]*(</)', r'\g<1>' + INTRO + r'\2', c)
c = re.sub(r'(id="teaser-turnover"[^>]*>)[^<]*(</)', r'\g<1>' + TURNOVER + r'\2', c)
c = re.sub(r'(id="teaser-dsei"[^>]*>)[^<]*(</)', r'\g<1>' + DSEI + r'\2', c)

# CTA button href
c = re.sub(r'(id="teaser-link"[^>]*href=")[^"]*(")', r'\g<1>' + WRAP_URL + r'\2', c)

write("index.html", c)


# ═══════════════════════════════════════════════════════════════════════════
# 2.  market-intelligence.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── market-intelligence.html ──")
c = read("market-intelligence.html")

# Hero report date
c = re.sub(r'(id="mi-report-date"[^>]*>)[^<]*(</)', r'\g<1>' + DATE_LONG + r'\2', c)

# Core metrics (reuse same IDs pattern as index)
c = re.sub(r'(id="mi-dsei"[^>]*>)[^<]*(</)', r'\g<1>' + DSEI + r'\2', c)
c = re.sub(r'(id="mi-tsi"[^>]*>)[^<]*(</)',  r'\g<1>' + TSI  + r'\2', c)
c = re.sub(r'(id="mi-turnover"[^>]*>)[^<]*(</)', r'\g<1>' + TURNOVER + r'\2', c)

# Gainers
for i, (ticker, change) in enumerate(GAINERS, 1):
    c = re.sub(rf'(id="mi-gainer-{i}-ticker"[^>]*>)[^<]*(</)', rf'\g<1>{ticker}\2', c)
    c = re.sub(rf'(id="mi-gainer-{i}-change"[^>]*>)[^<]*(</)', rf'\g<1>{change}\2', c)

# Losers
for i, (ticker, change) in enumerate(LOSERS, 1):
    c = re.sub(rf'(id="mi-loser-{i}-ticker"[^>]*>)[^<]*(</)', rf'\g<1>{ticker}\2', c)
    c = re.sub(rf'(id="mi-loser-{i}-change"[^>]*>)[^<]*(</)', rf'\g<1>{change}\2', c)

# Featured spotlight
c = re.sub(r'(id="mi-spotlight-link"[^>]*href=")[^"]*(")', r'\g<1>' + WRAP_URL + r'\2', c)
c = re.sub(r'(id="mi-spotlight-date"[^>]*>)[^<]*(</)', r'\g<1>' + DATE_LONG + r'\2', c)
c = re.sub(r'(id="mi-spotlight-title"[^>]*>)[^<]*(</)', r'\g<1>' + HEADLINE + r'\2', c)
c = re.sub(r'(id="mi-spotlight-excerpt"[^>]*>)[^<]*(</)', r'\g<1>' + INTRO[:200] + '...' + r'\2', c)

write("market-intelligence.html", c)


# ═══════════════════════════════════════════════════════════════════════════
# 3.  market-intelligence-archive.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── market-intelligence-archive.html ──")
c = read("market-intelligence-archive.html")

# Check if already added
if "dse-wrap-2026-09-03" not in c:
    # Find the first arc-row to determine the alternating pattern
    first_row = re.search(r'(<div class="arc-row")', c)
    if first_row:
        # New entry goes at top — determine bg of second row to keep alternation
        second_row_match = re.search(
            r'arc-row.*?arc-row.*?background:\s*(rgba\([^)]+\))',
            c, re.DOTALL)
        # new top entry should have no bg (white), pushing existing first to have bg
        new_entry = f'''<div class="arc-row">
                <div class="arc-date">{DATE_LONG}</div>
                <div class="arc-title">
                    <a href="{WRAP_URL}">{HEADLINE}</a>
                </div>
                <div class="arc-excerpt">{INTRO[:180]}...</div>
            </div>
            <div class="arc-row" style="background: rgba(11,29,58,0.02);">'''

        c = c.replace('<div class="arc-row">', new_entry, 1)

write("market-intelligence-archive.html", c)


print("\nAll done — ready to update current-prices.html next.")
