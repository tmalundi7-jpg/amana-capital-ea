import os
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

files = {
    '08': 'Tuesday, 8th September 2026',
    '09': 'Wednesday, 9th September 2026',
    '10': 'Thursday, 10th September 2026',
    '11': 'Friday, 11th September 2026',
    '14': 'Monday, 14th September 2026',
}

for day, date_str in files.items():
    filename = f'dse-wrap-2026-09-{day}.html'
    if not os.path.exists(filename): continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div', class_='dse-article-card')
    
    if card and not card.find('div', class_='dse-header-box'):
        header_html = f'''
<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">Daily DSE Wrap | {date_str}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">End of Day Market Intelligence</p>
</div>
'''
        header_soup = BeautifulSoup(header_html, 'html.parser')
        card.insert(0, header_soup)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Restored header in {filename}")
