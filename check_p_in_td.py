from bs4 import BeautifulSoup

for file in ['dse-wrap-2026-09-17.html', 'dse-wrap-2026-09-18.html']:
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    h1 = soup.find('h1')
    if not h1: continue
    card = h1.parent.parent
    table = card.find('table')
    if not table: continue
    print(f"{file} first header: {str(table.find('th'))}")
