from bs4 import BeautifulSoup

with open('dse-wrap-2026-09-18.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
content = soup.find('div', class_='article-content')
for p in content.find_all('p'):
    text = p.get_text(strip=True)
    if len(text) > 50:
        print(f"Good excerpt: {text}")
        break
