import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mammoth

with open(r'C:\Users\tmalu\Documents\Current Prices 04 September 2026.docx', 'rb') as docx:
    text = mammoth.extract_raw_text(docx).value

lines = [line.strip() for line in text.split('\n') if line.strip()]

stocks = []
i = 0
while i < len(lines):
    line = lines[i]
    if (line.isupper() and 2 <= len(line) <= 10 and
            'TICKER' not in line and 'BLOCK' not in line and
            'CHANGE' not in line and 'CURRENT' not in line):
        try:
            ticker   = lines[i]
            company  = lines[i+1]
            sector   = lines[i+2]
            price    = lines[i+3]
            # Replace various dashes with standard minus
            change   = lines[i+4].replace('\ufffd', '-').replace('\xa0', '').replace('–', '-')
            volume   = lines[i+5]
            turnover = lines[i+6]
            
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

DATE_LONG  = "Friday, 4th September 2026"
DATE_SHORT = "04 Sep 2026"
DSEI       = "4,523.81"
TSI        = "9,826.80"
TURNOVER_TOTAL = "TZS 8.18 bn"
VOLUME = "4,156,108" # From wrap

c = open("current-prices.html", encoding='utf-8').read()

# Replace the date part in the span showing "03 Sep 2026"
c = re.sub(
    r'(<div class="market-date">)[^<]*(</div>)',
    r'\g<1>04 Sep 2026\g<2>',
    c
)

c = re.sub(r'(Prices as of end-of-day )[^<]*', f'Prices as of end-of-day {DATE_LONG}', c)

c = re.sub(r'(id="cp-dsei"[^>]*>)[^<]*(</)',     rf'\g<1>{DSEI}\2',          c)
c = re.sub(r'(id="cp-tsi"[^>]*>)[^<]*(</)',      rf'\g<1>{TSI}\2',           c)
c = re.sub(r'(id="cp-turnover"[^>]*>)[^<]*(</)', rf'\g<1>{TURNOVER_TOTAL}\2', c)
c = re.sub(r'(id="cp-volume"[^>]*>)[^<]*(</)',   rf'\g<1>{VOLUME}\2', c)

c = re.sub(r'(<tbody[^>]*>)(.*?)(</tbody>)',
           lambda m: m.group(1) + '\n' + rows_html + m.group(3),
           c, flags=re.DOTALL)

with open("current-prices.html", 'w', encoding='utf-8') as f:
    f.write(c)
print("\nOK current-prices.html")
