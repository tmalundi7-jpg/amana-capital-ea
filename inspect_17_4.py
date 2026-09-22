from bs4 import BeautifulSoup
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
card = h1.parent.parent
tables = card.find_all('div', class_='table-responsive')
for t in tables[:1]:
    print(str(t))
