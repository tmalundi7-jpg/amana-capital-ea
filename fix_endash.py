import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

# use actual character
endash = chr(0x2013)
text = re.sub(r'(class="text-right change-negative"><strong>)-(.*?</strong)', r'\g<1>' + endash + r'\g<2>', text)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(r'(class="teaser-prem-stat-value loss"[^>]*>\s*<span>.*?</span>\s*<span[^>]*>)-(.*?</span>)', r'\g<1>' + endash + r'\g<2>', idx)
# The id="home-losers" could have multiple spans
# Let's just find and replace in that specific section
start_idx = idx.find('id="home-losers"')
if start_idx != -1:
    end_idx = idx.find('</div>', start_idx)
    losers_html = idx[start_idx:end_idx]
    losers_html = losers_html.replace('>-', f'>{endash}')
    idx = idx[:start_idx] + losers_html + idx[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
