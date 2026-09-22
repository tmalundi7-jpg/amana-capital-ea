from bs4 import BeautifulSoup
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
h1 = soup.find('h1')
print("Parent of H1 has class:", h1.parent.get('class'))
print("Parent of Parent of H1 has class:", h1.parent.parent.get('class'))
