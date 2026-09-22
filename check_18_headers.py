from bs4 import BeautifulSoup
with open('dse-wrap-2026-09-18_test.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
h1 = soup.find('h1')
card = h1.parent.parent

for child in card.children:
    if child.name:
        print(f"{child.name}: {child.get_text()[:40]}")
