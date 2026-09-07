import mammoth

with open(r'C:\Users\tmalu\Documents\Current Prices 03 September 2026.docx', 'rb') as docx:
    text = mammoth.extract_raw_text(docx).value

lines = [line.strip() for line in text.split('\n') if line.strip()]

data = []
for i in range(len(lines)):
    if lines[i] == 'AFRIPRISE':
        idx = i
        while idx < len(lines):
            ticker = lines[idx]
            if ticker == 'Block trades on the pre-arranged board today:':
                break
            
            # The structure is: Ticker, Name, Sector, Price, Change, Volume, Turnover
            try:
                change_str = lines[idx+4].replace('\ufffd', '-').replace('', '-')
                if '%' in change_str:
                    change = float(change_str.replace('%', ''))
                    data.append((ticker, change))
            except:
                pass
            idx += 7
        break

gainers = sorted([d for d in data if d[1] > 0], key=lambda x: x[1], reverse=True)[:3]
losers = sorted([d for d in data if d[1] < 0], key=lambda x: x[1])[:3]

print('Gainers:', gainers)
print('Losers:', losers)
