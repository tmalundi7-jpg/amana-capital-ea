from bs4 import BeautifulSoup
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
# Find the H1
h1 = soup.find('h1')
print(f"H1: {h1.get_text()}")

# Find the date
date_p = h1.find_next_sibling('p')
print(f"Date: {date_p.get_text()}")

# The content starts after the date_p.
# We can just empty the parent div and rebuild it? No, the parent div also contains breadcrumbs.
parent = h1.parent
print("Children of parent:")
for c in parent.children:
    if c.name:
        print(f" - {c.name}: {c.get_text()[:30]}")
