from bs4 import BeautifulSoup

def count_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    h1 = soup.find('h1')
    if not h1: return {}
    card = h1.parent.parent
    tags = {}
    for child in card.children:
        if child.name:
            tags[child.name] = tags.get(child.name, 0) + 1
    return tags

print("16:", count_tags('dse-wrap-2026-09-16.html'))
print("17:", count_tags('dse-wrap-2026-09-17.html'))
print("18:", count_tags('dse-wrap-2026-09-18.html'))
