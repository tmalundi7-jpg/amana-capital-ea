import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace date
html = re.sub(r'<div class="archive-date">17 Sep<br/>2026</div>', r'<div class="archive-date">18 Sep<br/>2026</div>', html)
# Replace title
html = re.sub(r'Daily DSE Wrap \| Thursday, 18th September 2026', r'Daily DSE Wrap | Friday, 18th September 2026', html)
# Replace excerpt
old_excerpt = r'The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Thursday. Equity turnover rose 51% to TZS 15.39 billion, driven by a massive block trade in NMB. Yet the All-Share Index fell 31 points, and the Tanzania Share Index dropped 160 points...'
new_excerpt = r'The Dar es Salaam Stock Exchange closed the week with a session of quiet resilience. Equity turnover fell 72% to TZS 4.30 billion from Thursday\'s block-heavy TZS 15.39 billion, and the All-Share In...'
html = html.replace(old_excerpt, new_excerpt)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated market-intelligence.html")

