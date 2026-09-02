import re

with open('dse-wrap-2026-09-02.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Check if section 7 cream box is present and correctly closed
match = re.search(r'<div class="dse-article-card" style="background: var\(--cream\).*?<h2.*?>7\..*?</h2>(.*?)</div>', c, re.DOTALL)
if match:
    print('Found cream box around section 7')
    print('Content inside box ends with:', repr(match.group(1)[-100:]))
else:
    print('No cream box found around section 7')
