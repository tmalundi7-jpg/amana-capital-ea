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
            # add color to th itself
            current_style = th.get('style', '')
            if 'color' not in current_style:
                th['style'] = current_style.rstrip(';') + '; color: #ffffff !important;'
            else:
                import re
                th['style'] = re.sub(r'color\s*:[^;]+;', 'color: #ffffff !important;', current_style)
                
            # force any strong inside to inherit
            for strong in th.find_all('strong'):
                strong_style = strong.get('style', '')
                if 'color' in strong_style:
                    strong['style'] = re.sub(r'color\s*:[^;]+;', 'color: inherit !important;', strong_style)
                    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Forced th white in {filename}")
