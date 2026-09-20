import re
content = open('dse-wrap-2026-09-17.html', encoding='utf-8').read()
match = re.search(r'<main id="swup">(.*?)</main>', content, re.DOTALL)
if match:
    with open('17_main_full.txt', 'w', encoding='utf-8') as f:
        f.write(match.group(1))
