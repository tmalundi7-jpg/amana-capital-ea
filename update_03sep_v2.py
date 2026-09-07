import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Data ─────────────────────────────────────────────────────────────────────
DATE_LONG    = "Thursday, 3rd September 2026"
DATE_SHORT   = "03 Sep 2026"
YYYY_MM_DD   = "2026-09-03"
DSEI         = "4,442.62"
TSI          = "9,653.89"
TURNOVER     = "TZS 42.93 bn"

GAINERS = [("MBP", "+8.2%"), ("NMG", "+7.9%"), ("KCB", "+3.9%")]
LOSERS  = [("TCCL", "-4.0%"), ("TTP", "-2.1%"), ("DSE", "-1.8%")]

HEADLINE = "A TZS 30 Billion Block Trade in CRDB Absorbed Without a Flinch — The Handoff is Complete"
INTRO    = ("The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on "
            "Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day "
            "figure in months. The driver was a single block trade in CRDB involving 11.2 million "
            "shares worth approximately TZS 30 billion, the largest such transaction in recent memory. "
            "Foreign investors sold nearly a third of the day's turnover, yet CRDB closed higher.")

WRAP_URL = "/dse-wrap-2026-09-03"

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK  {path}")


# ═══════════════════════════════════════════════════════════════════════════
# 1. index.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── index.html ──")
c = read("index.html")

# (a) Snapshot title subtitle  "End-of-day · 2 September 2026"
c = re.sub(
    r'(End-of-day &middot; )\d[^<]+',
    r'\g<1>3 September 2026',
    c)

# (b) Terminal feed note  "Terminal Feed | End-of-day · 2 September 2026"
c = re.sub(
    r'(Terminal Feed \| End-of-day &middot; )\d[^<]+',
    r'\g<1>3 September 2026',
    c)

# (c) Core metrics via existing IDs
c = re.sub(r'(id="home-dsei"[^>]*>)[^<]*(</)',     rf'\g<1>{DSEI}\2',     c)
c = re.sub(r'(id="home-tsi"[^>]*>)[^<]*(</)',      rf'\g<1>{TSI}\2',      c)
c = re.sub(r'(id="home-turnover"[^>]*>)[^<]*(</)', rf'\g<1>{TURNOVER}\2', c)

# (d) Gainers — replace the entire inner content of id="home-gainers" ... </div>
gainers_html = "\n" + "".join(
    f'            <span>{t} <span style="color:var(--gain)">{ch}</span></span>\n'
    for t, ch in GAINERS)
c = re.sub(
    r'(id="home-gainers"[^>]*>)(.*?)(</div>)',
    lambda m: m.group(1) + gainers_html + "          " + m.group(3),
    c, flags=re.DOTALL)

# (e) Losers
losers_html = "\n" + "".join(
    f'            <span>{t} <span style="color:var(--loss)">{ch}</span></span>\n'
    for t, ch in LOSERS)
c = re.sub(
    r'(id="home-losers"[^>]*>)(.*?)(</div>)',
    lambda m: m.group(1) + losers_html + "          " + m.group(3),
    c, flags=re.DOTALL)

# (f) Teaser date
c = re.sub(r'(<div class="teaser-prem-date">)[^<]*(</div>)',
           rf'\g<1>{DATE_LONG}\2', c)

# (g) Teaser title (h3)
c = re.sub(r'(<h3 class="teaser-prem-title">)[^<]*(</h3>)',
           rf'\g<1>Daily DSE Wrap | {DATE_LONG}\2', c)

# (h) Teaser body paragraph
c = re.sub(r'(<p class="teaser-prem-body">)[^<]*(</p>)',
           rf'\g<1>{INTRO}\2', c)

# (i) Teaser mini-stats — DSEI and Turnover inside teaser-prem-stats
#     Pattern: <div class="teaser-prem-stats" ...> contains stat blocks
c = re.sub(
    r'(class="teaser-prem-stats"[^>]*>)(.*?)(</div>\s*</div>\s*<!-- TEASER_CARD_END)',
    lambda m: m.group(1) + re.sub(
        r'(class="tps-val"[^>]*>)([^<]+)(</)',
        lambda mm: mm.group(1) + (DSEI if 'dsei' in mm.group(2).lower() or ',' in mm.group(2) else TURNOVER) + mm.group(3),
        m.group(2)) + m.group(3),
    c, flags=re.DOTALL)

# simpler approach: update individual stat values by matching their labels
# Find teaser-prem-stats block and update known values
def replace_teaser_stat(html, label_text, new_val):
    pattern = rf'({re.escape(label_text)}.*?class="tps-val"[^>]*>)[^<]*(</)'
    return re.sub(pattern, rf'\g<1>{new_val}\2', html, flags=re.DOTALL)

c = replace_teaser_stat(c, 'DSEI', DSEI)
c = replace_teaser_stat(c, 'Turnover', TURNOVER)

# (j) CTA button href
c = re.sub(r'(href="/dse-wrap-2026-\d{2}-\d{2}"[^>]*>Read the Full Wrap)',
           rf'href="{WRAP_URL}">Read the Full Wrap', c)

write("index.html", c)


# ═══════════════════════════════════════════════════════════════════════════
# 2. market-intelligence.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── market-intelligence.html ──")
c = read("market-intelligence.html")

# (a) Hero report date  "<strong>02 Sep 2026</strong>"
c = re.sub(r'(<strong>)\d{2} \w+ \d{4}(</strong>\s*Latest Report)',
           rf'\g<1>{DATE_SHORT}\2', c)

# (b) Snapshot date label
c = re.sub(
    r'(\d+ September 2026)(</span>)',
    f'3 September 2026\\2',
    c)

# (c) Core metrics
c = re.sub(r'(id="mi-dsei"[^>]*>)[^<]*(</)',     rf'\g<1>{DSEI}\2',     c)
c = re.sub(r'(id="mi-tsi"[^>]*>)[^<]*(</)',      rf'\g<1>{TSI}\2',      c)
c = re.sub(r'(id="mi-turnover"[^>]*>)[^<]*(</)', rf'\g<1>{TURNOVER}\2', c)

# (d) Gainers — replace between <!-- GAINERS_START --> and <!-- GAINERS_END -->
gainers_mi = "\n      <div style=\"display:flex; flex-direction:column; gap:0.15rem; width:100%;\">\n"
for t, ch in GAINERS:
    gainers_mi += (f'        <div style="display:flex; justify-content:space-between; font-size:0.75rem; '
                   f'font-weight:700; color:var(--cream);"><span>{t}</span> '
                   f'<span style="color:var(--gain)">{ch}</span></div>\n')
gainers_mi += "      </div>\n      "
c = re.sub(r'(<!-- GAINERS_START -->)(.*?)(<!-- GAINERS_END -->)',
           lambda m: m.group(1) + gainers_mi + m.group(3),
           c, flags=re.DOTALL)

# (e) Losers
losers_mi = "\n      <div style=\"display:flex; flex-direction:column; gap:0.15rem; width:100%;\">\n"
for t, ch in LOSERS:
    losers_mi += (f'        <div style="display:flex; justify-content:space-between; font-size:0.75rem; '
                  f'font-weight:700; color:var(--cream);"><span>{t}</span> '
                  f'<span style="color:var(--loss)">{ch}</span></div>\n')
losers_mi += "      </div>\n      "
c = re.sub(r'(<!-- LOSERS_START -->)(.*?)(<!-- LOSERS_END -->)',
           lambda m: m.group(1) + losers_mi + m.group(3),
           c, flags=re.DOTALL)

# (f) Archive-list featured spotlight — replace the single <a class="archive-row">
new_spotlight = f'''<a class="archive-row" href="{WRAP_URL}">
<div class="archive-date">{DATE_SHORT[:2]} {DATE_SHORT[3:6]}<br/>{DATE_SHORT[7:]}</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | {DATE_LONG}</div>
<div class="archive-content-excerpt">{INTRO[:180]}...</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>'''
c = re.sub(r'<a class="archive-row"[^>]*>.*?</a>',
           new_spotlight, c, count=1, flags=re.DOTALL)

write("market-intelligence.html", c)


# ═══════════════════════════════════════════════════════════════════════════
# 3. market-intelligence-archive.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n── market-intelligence-archive.html ──")
c = read("market-intelligence-archive.html")

if "dse-wrap-2026-09-03" not in c:
    # Find first arc-row; new entry goes before it (no bg = clean white)
    # Existing first row needs bg added
    new_entry = (
        f'<div class="arc-row">\n'
        f'                <div class="arc-date">{DATE_LONG}</div>\n'
        f'                <div class="arc-title">\n'
        f'                    <a href="{WRAP_URL}">Daily DSE Wrap | {DATE_LONG}</a>\n'
        f'                </div>\n'
        f'                <div class="arc-excerpt">{INTRO[:200]}...</div>\n'
        f'            </div>\n'
        f'            <div class="arc-row" style="background: rgba(11,29,58,0.02);">'
    )
    c = c.replace('<div class="arc-row">', new_entry, 1)
    write("market-intelligence-archive.html", c)
else:
    print("  Already present, skipping.")


print("\nAll 3 files updated. Now run current-prices.html update separately.")
