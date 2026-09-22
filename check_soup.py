import bs4

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    soup14 = bs4.BeautifulSoup(f, 'html.parser')

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    soup21 = bs4.BeautifulSoup(f, 'html.parser')

print("14 Article header:")
print(soup14.find('div', class_='article-header'))

print("\n21 Article header:")
print(soup21.find('div', class_='article-header'))
