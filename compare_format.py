import re

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    text14 = f.read()

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    text21 = f.read()

# Find the div for section 7 in both
div14_match = re.search(r'<div class="" style="background: var\(--cream\).*?</div></div>', text14, re.DOTALL)
div21_match = re.search(r'<div class="" style="background: var\(--cream\).*?</div>\n</div>', text21, re.DOTALL)
div21_alt = re.search(r'<div class="" style="background: var\(--cream\).*?</div>\s*</div>', text21, re.DOTALL)

print('--- 14 Sep Section 7 ---')
if div14_match:
    print(repr(div14_match.group(0)[-200:]))
else:
    print('Not found')

print('--- 21 Sep Section 7 ---')
if div21_alt:
    print(repr(div21_alt.group(0)[-200:]))
else:
    print('Not found')

# Also check the disclaimer format
print('--- 14 Sep Disclaimer ---')
disc14 = re.search(r'<p style="font-size: 0.85rem; color: var\(--mist\).*?</p>', text14, re.DOTALL)
if disc14: print(disc14.group(0))

print('--- 21 Sep Disclaimer ---')
disc21 = re.search(r'<div class="article-disclaimer".*?</div>', text21, re.DOTALL)
if disc21: print(disc21.group(0))
