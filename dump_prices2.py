import os
import mammoth
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')
with open("C:\\Users\\tmalu\\Documents\\Current Prices 14 September 2026.docx", 'rb') as f:
    html = mammoth.convert_to_html(f).value
soup = BeautifulSoup(html, 'html.parser')
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) >= 4:
        symbol = tds[0].get_text(strip=True)
        if symbol in ['NMB', 'TBL', 'CRDB', 'VODA', 'TPCC', 'NICO', 'KCB', 'TCCL', 'TOL', 'SWIS', 'DCB', 'MBP', 'MCB', 'NMG']:
            change = tds[3].get_text(strip=True)
            print(f"{symbol}: {change}")
