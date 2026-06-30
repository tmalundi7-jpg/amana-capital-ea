import re

data = """AFRIPRISE: open 650, close 665, high 675, low 645, volume 87,996, turnover 58,468,530
CRDB: open 2,580, close 2,590, high 2,600, low 2,580, volume 928,067, turnover 2,406,357,400
DCB: open 510, close 510, volume 22,218, turnover 11,315,810
DSE: open 6,410, close 6,410, volume 1,597, turnover 10,238,430
KCB: open 1,940, close 1,950, high 2,030, low 1,930, volume 336,813, turnover 657,329,690
MBP: open 1,910, close 2,010, volume 2,405, turnover 4,812,830
MCB: open 985, close 945, volume 8,965, turnover 8,429,310
MKCB: open 4,160, close 4,400, volume 2,274, turnover 9,961,500
MUCOBA: open 490, close 490, volume 676, turnover 332,630
NICO: open 3,600, close 3,600, volume 27,437, turnover 98,845,630
NMB: open 16,110, close 16,160, high 16,200, low 16,120, volume 228,782, turnover 3,667,964,130
NMG: open 260, close 270, volume 20, turnover 5,200
PAL: open 360, close 355, volume 11,033, turnover 3,896,385
SWIS: open 2,710, close 2,700, volume 2,525, turnover 6,817,230
TBL: open 9,780, close 9,710, volume 3,813, turnover 37,028,510
TCC: open 12,450, close 12,460, volume 597, turnover 7,437,800
TCCL: open 3,300, close 3,300, volume 10,685, turnover 35,213,790
TOL: open 1,420, close 1,450, volume 6,605, turnover 9,595,670
TPCC: open 6,610, close 6,490, volume 2,638, turnover 17,135,110
TTP: open 500, close 480, volume 576, turnover 274,965
VODA: open 745, close 770, high 780, low 745, volume 48,755, turnover 37,516,390
USL: close 25, no volume
YETL: close 510, no volume"""

companies = {
    "AFRIPRISE": "Afriprise",
    "CRDB": "CRDB Bank Plc",
    "DCB": "DCB Commercial Bank",
    "DSE": "Dar es Salaam Stock Exchange",
    "KCB": "KCB Group",
    "MBP": "Mkombozi Commercial Bank",
    "MCB": "Mwalimu Commercial Bank",
    "MKCB": "Mkombozi Commercial Bank", 
    "MUCOBA": "Mucoba Bank",
    "NICO": "National Investments Co",
    "NMB": "NMB Bank Plc",
    "NMG": "Nation Media Group",
    "PAL": "PricewaterhouseCoopers",
    "SWIS": "Swissport Tanzania",
    "TBL": "Tanzania Breweries",
    "TCC": "Tanzania Cigarette Co",
    "TCCL": "Tanga Cement",
    "TOL": "TOL Gases",
    "TPCC": "Tanzania Portland Cement",
    "TTP": "Tatepa",
    "VODA": "Vodacom Tanzania",
    "USL": "Uchumi Supermarkets",
    "YETL": "YETL"
}

sectors = {
    "Banks & Finance": ["CRDB", "NMB", "DCB", "KCB", "MKCB", "MCB", "MUCOBA", "NICO", "MBP"],
    "Industrials & Allied": ["TBL", "TCC", "TCCL", "TPCC", "TOL", "PAL"],
    "Commercial Services": ["SWIS", "VODA", "NMG", "DSE", "AFRIPRISE", "TTP", "USL", "YETL"]
}

def get_sector(ticker):
    for s, ticks in sectors.items():
        if ticker in ticks:
            return s
    return "Unknown"

rows = []
for line in data.split("\n"):
    parts = line.split(":")
    ticker = parts[0].strip()
    rest = parts[1]
    
    close_match = re.search(r'close ([\d,]+)', rest)
    if not close_match: continue
    close_price = int(close_match.group(1).replace(",", ""))
    
    open_match = re.search(r'open ([\d,]+)', rest)
    if open_match:
        open_price = int(open_match.group(1).replace(",", ""))
        change = ((close_price - open_price) / open_price) * 100
        change_str = f"{change:+.2f}%"
        if change > 0:
            change_class = ' class="text-success"'
        elif change < 0:
            change_class = ' class="text-danger"'
        else:
            change_class = ""
    else:
        change_str = "—"
        change_class = ""
        
    vol_match = re.search(r'volume ([\d,]+)', rest)
    vol_str = vol_match.group(1) if vol_match else "0"
    
    turn_match = re.search(r'turnover ([\d,]+)', rest)
    turn_str = turn_match.group(1) if turn_match else "0"
    
    sec = get_sector(ticker)
    comp = companies.get(ticker, ticker)
    
    rows.append(f"<tr><td>{ticker}</td><td>{comp}</td><td><span class=\"sector-badge\">{sec}</span></td><td>{close_price:,}</td><td{change_class}>{change_str}</td><td>{vol_str}</td><td>{turn_str}</td></tr>")

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace table
table_html = """<table class="data-table">
                    <thead>
                        <tr><th>Ticker</th><th>Company Name</th><th>Sector</th><th>Last Price (TZS)</th><th>Change</th><th>Volume</th><th>Turnover (TZS)</th></tr>
                    </thead>
                    <tbody>
                        """ + "\n                        ".join(rows) + """
                    </tbody>
                </table>"""

content = re.sub(r'<table class="data-table">.*?</table>', table_html, content, flags=re.DOTALL)
content = content.replace("Data Status:</strong> End-of-day, 29 June 2026. For educational purposes only. Not real-time data. (Live API integration planned for future release).", "Data Status:</strong> End-of-day data, 29 June 2026. For educational purposes only. Not real-time data.")

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update Market Intelligence
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

new_card = """<div class="card" style="margin-bottom: 2rem;">
                <span style="font-size: 0.85rem; color: var(--navy); text-transform: uppercase; font-weight: 600;">29 June 2026</span>
                <h3>Banking Sector Leads Volume & NMB Block Trade</h3>
                <p>The banking sector drove market volumes today, highlighted by a significant block trade in NMB of 108,000 shares.</p>
                <a href="dse-wrap-2026-06-29.html">Read Full Wrap &rarr;</a>
            </div>"""
            
mi = re.sub(r'<div class="card" style="margin-bottom: 2rem;">.*?Read Full Wrap &rarr;</a>\n            </div>', new_card, mi, count=1, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi)

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()
    
idx = re.sub(r'<!-- SNAPSHOT_DATE -->.*?<!-- SNAPSHOT_DATE_END -->', '<!-- SNAPSHOT_DATE -->29 June 2026<!-- SNAPSHOT_DATE_END -->', idx, flags=re.DOTALL)
idx = idx.replace('4,040.04', '4,040.04') # just in case, wait it's already 4040.04 in index maybe
idx = idx.replace('8,734.37', '8,734.37')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
