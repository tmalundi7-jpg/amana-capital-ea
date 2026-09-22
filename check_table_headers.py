from bs4 import BeautifulSoup
with open('dse-wrap-2026-09-18.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
card = h1.parent.parent

for table in card.find_all('table'):
    for tr in table.find_all('tr')[:1]:
        print(f"Header row style: {tr.get('style')}")
        for th in tr.find_all(['th', 'td']):
            print(f"  {th.name}: {th.get_text()} | style: {th.get('style')}")
