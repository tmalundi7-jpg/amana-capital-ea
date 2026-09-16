import re
import os

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update date
text = text.replace('14 September 2026', '15 September 2026')
text = text.replace('14th September 2026', '15th September 2026')
text = text.replace('Monday, 15th', 'Tuesday, 15th') # In case of replacing 14th resulted in this

# Update Snapshot Values
text = re.sub(r'(<div class="snapshot-value" id="mi-dsei">)[\d,\.]+</div>', r'\g<1>4,696.11</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="mi-tsi">)[\d,\.]+</div>', r'\g<1>10,438.46</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="mi-turnover">)TZS [\d\.]+ bn</div>', r'\g<1>TZS 16.86 bn</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="mi-volume">)[\d,\.]+</div>', r'\g<1>7,954,485</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="mi-deals">)[\d,\.]+</div>', r'\g<1>3,516</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="mi-bonds">)TZS [\d\.]+ bn</div>', r'\g<1>TZS 26.61 bn</div>', text)

# Latest Report Wrap Link and text
# The link is currently pointing to dse-wrap-2026-09-14.html
text = text.replace('dse-wrap-2026-09-14.html', 'dse-wrap-2026-09-15.html')

excerpt = "The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Tuesday. Equity turnover surged 166.5% to TZS 16.86 billion, driven by four major block trades. The All-Share Index closed at a new post-split high of 4,696.11..."
text = re.sub(r'(<div class="archive-content-excerpt">).*?(</div>)', r'\g<1>' + excerpt + r'\g<2>', text, count=1, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated market-intelligence.html')
