from bs4 import BeautifulSoup
import re

with open('dse-wrap-2026-09-18.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
card = h1.parent.parent

# 1. Fix Headings
for p in card.find_all('p', recursive=False):
    text = p.get_text(strip=True)
    if re.match(r'^[1-6]\.\s+[A-Z]', text):
        p.name = 'h2'
        p['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
        for b in p.find_all(['strong', 'b']): b.unwrap()
    elif re.match(r'^7\.\s+[A-Z]', text):
        p.name = 'h3'
        p['style'] = "color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;"
        for b in p.find_all(['strong', 'b']): b.unwrap()

# 2. Fix Section 7 Cream Box
h3_section7 = None
for child in card.children:
    if child.name == 'h3' and '7. Considerations for a Multi-Year Framework' in child.get_text():
        h3_section7 = child
        break

if h3_section7:
    div = soup.new_tag('div', style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;")
    h3_section7.insert_before(div)
    div.append(h3_section7)
    
    curr = div.find_next_sibling()
    while curr:
        nxt = curr.find_next_sibling()
        if curr.name == 'div' and 'article-disclaimer' in curr.get('class', []):
            break
        if curr.name == 'p' and 'For general informational and educational purposes only' in curr.get_text():
            curr.name = 'p'
            curr.string = ''
            em = soup.new_tag('em')
            em.string = 'For general informational and educational purposes only; not financial, legal, or tax advice. All investment decisions are solely your responsibility. Capital is at risk, and past performance does not guarantee future results. Amana Capital East Africa Limited registration under CMSA, Tanzania is pending. Registration does not imply CMSA endorsement.'
            curr.append(em)
            div.append(curr)
            curr = nxt
            continue
            
        div.append(curr)
        curr = nxt

# 3. Fix Table cell <p> tags
for table in card.find_all('table'):
    for cell in table.find_all(['th', 'td']):
        # If the cell has a <p> inside, unwrap it.
        for p in cell.find_all('p'):
            p.unwrap()

with open('dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("All fixes applied perfectly!")
