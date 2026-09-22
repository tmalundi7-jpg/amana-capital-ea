import bs4

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    soup14 = bs4.BeautifulSoup(f, 'html.parser')

body14 = soup14.find('body')
if body14:
    # print the first 20 children or elements in the body
    content = str(body14)[:1500]
    print(content)
