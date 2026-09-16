import os
import re

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

for day in ['08', '09', '10', '11', '14']:
    filename = f'dse-wrap-2026-09-{day}.html'
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Regex to find all <th ...>...</th> and <td ...>...</td>
    # and remove <p> and </p> just inside them.
    # We can do this safely using beautifulsoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # We only care about tables inside .data-table
    for table in soup.find_all('table', class_='data-table'):
        for th in table.find_all('th'):
            # replace <p> tags with their contents
            for p in th.find_all('p'):
                p.unwrap()
        for td in table.find_all('td'):
            for p in td.find_all('p'):
                p.unwrap()
                
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed table formatting in {filename}")
