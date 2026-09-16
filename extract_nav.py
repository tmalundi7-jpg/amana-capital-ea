import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<nav class="navbar">.*?</nav>', content, flags=re.DOTALL)
if match:
    nav = match.group(0)
    # Remove the svg brand icon if present
    nav = re.sub(r'<svg aria-hidden=\"true\" class=\"brand-icon\".*?</svg>\s*', '', nav, flags=re.DOTALL)
    print(nav)
