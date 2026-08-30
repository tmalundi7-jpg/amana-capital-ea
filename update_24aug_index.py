import json
import re

INDEX_PATH = "index.html"

# Load parsed data
with open('parsed_wrap_24aug.json', 'r', encoding='utf-8') as f:
    wrap_data = json.load(f)
with open('parsed_prices_24aug.json', 'r', encoding='utf-8') as f:
    prices = json.load(f)

# Calculate Gainers and Losers for Heatmap from Prices
def parse_change(c):
    if c == '0.0%': return 0.0
    c = c.replace('?', '-').replace('–', '-').replace('%', '').replace('+', '')
    try:
        return float(c)
    except:
        return 0.0

sorted_prices = sorted(prices, key=lambda x: parse_change(x.get('change_pct', '0%')), reverse=True)
gainers = [p for p in sorted_prices if parse_change(p.get('change_pct')) > 0][:3]
losers = [p for p in sorted_prices if parse_change(p.get('change_pct')) < 0]
losers.reverse()
losers = losers[:3]

top_mover = gainers[0] if gainers else {"ticker": "", "change_pct": ""}

dsei_eod = wrap_data['snapshot'].get('dsei', '4,250.04')
tsi_val = wrap_data['snapshot'].get('tsi', '9,321.17')
turnover_val = wrap_data['snapshot'].get('turnover', 'TZS 74.85 mn')

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

def swap(html, pattern, repl, flags=re.DOTALL):
    new, n = re.subn(pattern, repl, html, count=1, flags=flags)
    return new

# ── Hero stats cards ─────────────────────────────────────
# DSEI End of Day value
html = swap(html,
    r'(<div class="home-stat-label">DSEI \u2014 End of Day</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei_eod}\2'
)
# Daily Turnover value
html = swap(html,
    r'(<div class="home-stat-label">Daily Turnover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_val}\2'
)
# Top Mover value
top_mover_change = top_mover['change_pct'].replace('?', '-').replace('–', '-')
if not top_mover_change.startswith('+') and parse_change(top_mover_change) > 0:
    top_mover_change = "+" + top_mover_change
top_mover_display = f"{top_mover['ticker']} {top_mover_change}"
html = swap(html,
    r'(<div class="home-stat-label">Top Mover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{top_mover_display}\2'
)
# Date badge on top-mover card
html = swap(html,
    r'(<span class="home-stat-badge neutral">)\d+ \w+ \d+(</span>)',
    r'\g<1>24 Aug 2026\2'
)

# ── Snapshot section header date ──────────────────────────────
html = swap(html,
    r'(End-of-day\s*\u00b7\s*)\d+ \w+ \d+',
    r'\g<1>24 August 2026'
)

# ── Snapshot values ────────────────────────────────────────────────────────
html = swap(html,
    r'(<div class="snapshot-value" id="home-dsei">)[^<]*(<span)',
    rf'\g<1>{dsei_eod} \2'
)
html = swap(html,
    r'(<div class="snapshot-value" id="home-tsi">)[^<]*(<span)',
    rf'\g<1>{tsi_val} \2'
)
html = swap(html,
    r'(<div class="snapshot-value" id="home-turnover">)[^<]*(</div>)',
    rf'\g<1>{turnover_val}\2'
)

gainers_inner = "\n".join(
    f'            <span>{g["ticker"]} <span style="color:var(--gain)">{"+" + g["change_pct"].replace("?", "-").replace("–", "-").lstrip("+")}</span></span>'
    for g in gainers
)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-gainers"[^>]*>).*?(</div>)',
    rf'\g<1>\n{gainers_inner}\n</div>'
)

losers_inner = "\n".join(
    f'            <span>{l["ticker"]} <span style="color:var(--loss)">{l["change_pct"].replace("?", "-").replace("–", "-")}</span></span>'
    for l in losers
)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-losers"[^>]*>).*?(</div>)',
    rf'\g<1>\n{losers_inner}\n</div>'
)

html = swap(html,
    r'(Live Terminal Feed \| End-of-day, )\d+ \w+ \d+',
    r'\g<1>24 August 2026'
)

# ── Wrap teaser stats ───────────────────────────────────────────────────────
html = swap(html,
    r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei_eod}\2'
)
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_val}\2'
)
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Top Gainer</div>\s*<div class="teaser-prem-stat-value gain">)[^<]*(</div>)',
    rf'\g<1>{top_mover_display}\2'
)

# Replace the Read the Latest DSE Wrap link and title
# Link: href="/dse-wrap-2026-08-17" -> "/dse-wrap-2026-08-24"
html = re.sub(r'href="/dse-wrap-2026-08-\d+"', r'href="/dse-wrap-2026-08-24"', html)
html = re.sub(r'href="/dse-wrap-2026-\d{2}-\d{2}"', r'href="/dse-wrap-2026-08-24"', html)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html")
