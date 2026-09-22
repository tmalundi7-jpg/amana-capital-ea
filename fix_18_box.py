from bs4 import BeautifulSoup

with open('dse-wrap-2026-09-18_test.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
card = h1.parent.parent

h3_section7 = None
for child in card.children:
    if child.name == 'h3' and '7. Considerations for a Multi-Year Framework' in child.get_text():
        h3_section7 = child
        break

if h3_section7:
    div = soup.new_tag('div', style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;")
    h3_section7.insert_before(div)
    div.append(h3_section7)
    
    # move subsequent elements until disclaimer or end
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

with open('dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Fixed section 7 box!")
