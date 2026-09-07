import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mammoth

# ── Parse Current Prices DOCX ─────────────────────────────────────────────
with open(r'C:\Users\tmalu\Documents\Current Prices 03 September 2026.docx', 'rb') as docx:
    text = mammoth.extract_raw_text(docx).value

lines = [line.strip() for line in text.split('\n') if line.strip()]

# ── Build stock rows ───────────────────────────────────────────────────────
HEADERS = ['Ticker','Company','Sector','Last Price (TZS)','Change (%)','Volume','Turnover (TZS)']
stocks = []
i = 0
while i < len(lines):
    # Detect ticker: all caps, 2-8 chars, not a header or note line
    line = lines[i]
    if (line.isupper() and 2 <= len(line) <= 10 and
            'TICKER' not in line and 'BLOCK' not in line and
            'CHANGE' not in line and 'CURRENT' not in line):
        try:
            ticker   = lines[i]
            company  = lines[i+1]
            sector   = lines[i+2]
            price    = lines[i+3]
            change   = lines[i+4].replace('\ufffd', '-').replace('\xa0', '')
            volume   = lines[i+5]
            turnover = lines[i+6]
            
            # Validate: price should be numeric-ish
            price_clean = price.replace(',', '')
            float(price_clean)
            
            stocks.append({
                'ticker': ticker,
                'company': company,
                'sector': sector,
                'price': price,
                'change': change,
                'volume': volume,
                'turnover': turnover,
            })
            i += 7
            continue
        except (ValueError, IndexError):
            pass
    i += 1

print(f"Parsed {len(stocks)} stocks:")
for s in stocks:
    print(f"  {s['ticker']:8s} {s['price']:>10s} {s['change']:>8s}")

# ── Build HTML table rows ─────────────────────────────────────────────────
def fmt_change(ch):
    ch = ch.strip()
    if ch.startswith('+'):
        return f'<td class="change-positive">{ch}</td>'
    elif ch.startswith('-'):
        return f'<td class="change-negative">{ch}</td>'
    else:
        return f'<td class="change-neutral">{ch}</td>'

rows_html = ""
for s in stocks:
    rows_html += (
        f'<tr>'
        f'<td class="ticker-cell">{s["ticker"]}</td>'
        f'<td>{s["company"]}</td>'
        f'<td>{s["sector"]}</td>'
        f'<td class="price-cell">{s["price"]}</td>'
        f'{fmt_change(s["change"])}'
        f'<td>{s["volume"]}</td>'
        f'<td>{s["turnover"]}</td>'
        f'</tr>\n'
    )

# ── Snapshot values ───────────────────────────────────────────────────────
DATE_LONG  = "Thursday, 3rd September 2026"
DATE_SHORT = "03 Sep 2026"
DSEI       = "4,442.62"
TSI        = "9,653.89"
TURNOVER_TOTAL = "TZS 42.93 bn"

# ── Update current-prices.html ─────────────────────────────────────────────
c = open("current-prices.html", encoding='utf-8').read()

# (a) Update snapshot bar: date
c = re.sub(r'(End-of-day[,:]?\s*(?:&middot;\s*)?)[\w, ]+\d{4}',
           rf'\g<1>{DATE_LONG}', c)
c = re.sub(r'(\d+ \w+ 2026|Thursday[^<]+2026)', DATE_LONG, c)

# (b) Subtitle date paragraph
c = re.sub(r'(class="[^"]*subtitle[^"]*"[^>]*>)[^<]*(</)',
           rf'\g<1>Prices as of end-of-day {DATE_LONG}\2', c)
c = re.sub(r'(Prices as of[^<]+20\d\d)',
           f'Prices as of end-of-day {DATE_LONG}', c)

# (c) DSEI, TSI, Turnover in snapshot bar
c = re.sub(r'(id="cp-dsei"[^>]*>)[^<]*(</)',     rf'\g<1>{DSEI}\2',          c)
c = re.sub(r'(id="cp-tsi"[^>]*>)[^<]*(</)',      rf'\g<1>{TSI}\2',           c)
c = re.sub(r'(id="cp-turnover"[^>]*>)[^<]*(</)', rf'\g<1>{TURNOVER_TOTAL}\2', c)

# (d) Replace the <tbody> content
c = re.sub(r'(<tbody[^>]*>)(.*?)(</tbody>)',
           lambda m: m.group(1) + '\n' + rows_html + m.group(3),
           c, flags=re.DOTALL)

with open("current-prices.html", 'w', encoding='utf-8') as f:
    f.write(c)
print("\nOK  current-prices.html")
