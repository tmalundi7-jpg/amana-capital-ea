import bs4
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    soup14 = bs4.BeautifulSoup(f, 'html.parser')

body14 = soup14.find('body')
if body14:
    content = str(body14)[1200:3000]
    print(content)
