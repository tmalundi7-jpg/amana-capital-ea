import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    soup21 = bs4.BeautifulSoup(f, 'html.parser')

body21 = soup21.find('body')
if body21:
    content = str(body21)[1200:3000]
    print(content)
