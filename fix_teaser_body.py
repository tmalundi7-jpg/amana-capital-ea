import re

new_teaser = "The Dar es Salaam Stock Exchange closed the week on a strong note, with both indices reaching new post-split highs and equity turnover recovering above the TZS 3 billion mark. Yet the most significant development was not in the equity market at all &mdash; it was in the bond market, where turnover contracted for the third consecutive session. This is the pattern that experienced investors watch for: when institutional money steps away from fixed income while equities attract fresh capital, a rotation may be quietly underway. For everyday investors, this is a moment to pay close attention."

# Fix index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()
idx_html = re.sub(r'<p class="teaser-prem-body">.*?</p>', f'<p class="teaser-prem-body">{new_teaser}</p>', idx_html, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)

# Fix market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()
mi_html = re.sub(r'<div class="archive-content-excerpt">.*?</div>', f'<div class="archive-content-excerpt">{new_teaser}</div>', mi_html, flags=re.DOTALL)
with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

print("SUCCESS")
