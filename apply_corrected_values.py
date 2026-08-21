import json, re, sys, shutil
sys.stdout.reconfigure(encoding="utf-8")

with open("extracted_dse_data.json", encoding="utf-8") as f:
    d = json.load(f)

dsei         = d["dsei_end_of_day"]
tsi          = d["live_dse_snapshot"]["tsi"]
turnover_raw = d["daily_turnover"]
turnover_bn  = "TZS 4.77bn"
top_mover    = d["top_mover"]
gainers      = d["live_dse_snapshot"]["top_gainers"]
losers       = d["live_dse_snapshot"]["top_losers"]

top_mover_display = f"{top_mover['name']} {top_mover['change']}"
raw_pct = float(top_mover["change"].replace("%","").replace("+","").replace(",",""))
tg_display = f"{top_mover['name']} +{abs(raw_pct):.1f}%"

shutil.copy2("index.html", "index.html.bak_17aug_corrected")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = []

def swap(h, pat, rep, label, flags=re.DOTALL):
    new, n = re.subn(pat, rep, h, count=1, flags=flags)
    changes.append(("[OK]" if n else "[MISS]") + " " + label)
    return new

# Hero stats
html = swap(html,
    r'(<div class="home-stat-label">DSEI \u2014 End of Day</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei}\2', "Hero DSEI")
html = swap(html,
    r'(<div class="home-stat-label">Daily Turnover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_raw}\2', "Hero Turnover")
html = swap(html,
    r'(<div class="home-stat-label">Top Mover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{top_mover_display}\2', "Hero Top Mover")
html = swap(html,
    r'(<span class="home-stat-badge neutral">)\d+ \w+ \d+(</span>)',
    r'\g<1>17 Aug 2026\2', "Hero date badge")

# Snapshot header date
html = swap(html,
    r'(End-of-day\s*\u00b7\s*)\d+ \w+ \d+',
    r'\g<1>17 August 2026', "Snapshot header date")

# Snapshot values
html = swap(html,
    r'(<div class="snapshot-value" id="home-dsei">)[^<]*(<span)',
    rf'\g<1>{dsei} \2', "Snapshot DSEI")
html = swap(html,
    r'(<div class="snapshot-value" id="home-tsi">)[^<]*(<span)',
    rf'\g<1>{tsi} \2', "Snapshot TSI")
html = swap(html,
    r'(<div class="snapshot-value" id="home-turnover">)[^<]*(</div>)',
    rf'\g<1>{turnover_raw}\2', "Snapshot Turnover")

# Gainers -- build inner HTML without f-string CSS var conflict
g_lines = []
for g in gainers:
    g_lines.append('            <span>' + g["name"] + ' <span style="color:var(--gain)">' + g["change"] + '</span></span>')
gainers_inner = "\n".join(g_lines)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-gainers"[^>]*>).*?(</div>)',
    r'\g<1>' + "\n" + gainers_inner + "\n" + r'</div>',
    "Snapshot Gainers")

# Losers
l_lines = []
for l in losers:
    l_lines.append('            <span>' + l["name"] + ' <span style="color:var(--loss)">' + l["change"] + '</span></span>')
losers_inner = "\n".join(l_lines)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-losers"[^>]*>).*?(</div>)',
    r'\g<1>' + "\n" + losers_inner + "\n" + r'</div>',
    "Snapshot Losers")

# Snapshot footer date
html = swap(html,
    r'(Live Terminal Feed \| End-of-day, )\d+ \w+ \d+',
    r'\g<1>17 August 2026', "Snapshot footer date")

# Wrap teaser
html = swap(html,
    r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei}\2', "Teaser DSEI")
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_bn}\2', "Teaser Turnover")
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Top Gainer</div>\s*<div class="teaser-prem-stat-value gain">)[^<]*(</div>)',
    rf'\g<1>{tg_display}\2', "Teaser Top Gainer")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

for c in changes:
    print(c)
print("\nDone -- index.html updated with corrected 17-Aug values.")
