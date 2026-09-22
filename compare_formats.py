with open('dse-wrap-2026-09-16.html', 'r', encoding='utf-8') as f:
    h16 = f.read()
with open('dse-wrap-2026-09-18.html', 'r', encoding='utf-8') as f:
    h18 = f.read()

import re
c16 = re.search(r'<div class="article-content">(.*?)<div class="article-disclaimer"', h16, re.DOTALL)
c18 = re.search(r'<div class="dse-header-box">(.*?)<div class="article-disclaimer"', h18, re.DOTALL)

print("16 length:", len(c16.group(1)) if c16 else "NOT FOUND")
print("18 length:", len(c18.group(1)) if c18 else "NOT FOUND")
