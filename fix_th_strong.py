import os
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

for day in ['08', '09', '10', '11', '14']:
    filename = f'dse-wrap-2026-09-{day}.html'
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    for table in soup.find_all('table', class_='data-table'):
        for th in table.find_all('th'):
            for strong in th.find_all('strong'):
                if 'style' in strong.attrs:
                    strong['style'] = strong['style'].replace('color: #000;', 'color: var(--white);')
                    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed th strong tags in {filename}")
