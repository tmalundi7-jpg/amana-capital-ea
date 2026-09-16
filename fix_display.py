import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<svg aria-hidden=\"true\" class=\"brand-icon\".*?</svg>\s*', '', content, flags=re.DOTALL)

tbody_match = re.search(r'<tbody>(.*?)</tbody>', content, flags=re.DOTALL)
if tbody_match:
    tbody_content = tbody_match.group(1)
    tbody_content = tbody_content.replace('<strong>', '').replace('</strong>', '')
    content = content[:tbody_match.start(1)] + tbody_content + content[tbody_match.end(1):]

content = re.sub(r'\.gold-grid-table td:nth-child\(1\) \{\s*font-weight: 700 !important;\s*\}\s*', '', content)
content = re.sub(r'font-weight: 700 !important;\s*', '', content)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
