from bs4 import BeautifulSoup
import re

with open('dse-wrap-2026-09-18.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
card = h1.parent.parent

for p in card.find_all('p', recursive=False):
    text = p.get_text(strip=True)
    # Check if it starts with a number, a dot, and a space
    if re.match(r'^[1-6]\.\s+[A-Z]', text):
        p.name = 'h2'
        p['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
        # Remove any bold tags inside since h2 is naturally bold
        for b in p.find_all(['strong', 'b']):
            b.unwrap()
    elif re.match(r'^7\.\s+[A-Z]', text):
        p.name = 'h3'
        p['style'] = "color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;"
        for b in p.find_all(['strong', 'b']):
            b.unwrap()

with open('dse-wrap-2026-09-18_test.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
