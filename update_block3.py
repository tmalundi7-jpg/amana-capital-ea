import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace date
c = re.sub(r'Monday, 7th September 2026', 'Wednesday, 9th September 2026', c)

# Use dictionary mapping for safety
replacements = {
    'CRDB</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">3,193,022': 'KCB</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">500,000',
    'KCB</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">500,000': 'NMB</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">639,435',
    'NMB</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">1,051,811': 'TCCL</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">127,058',
    'IEACLC-ETF</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">809,952': 'IEACLC-ETF</div>\n      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">351,927'
}

for k, v in replacements.items():
    c = c.replace(k, v)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

