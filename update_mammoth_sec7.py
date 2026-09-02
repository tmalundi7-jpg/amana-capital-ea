import re
from bs4 import BeautifulSoup

def update_mammoth_script():
    with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
        c = f.read()
    
    # We will inject the section 7 logic right before "return str(soup)"
    inject_code = '''
    # Wrap Section 7
    for h2 in soup.find_all('h2'):
        if h2.text.strip().startswith('7.'):
            # Change to h3
            h2.name = 'h3'
            h2['style'] = "color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;"
            
            # Wrap in cream box
            wrapper = soup.new_tag('div')
            wrapper['class'] = ['dse-header-box']
            wrapper['style'] = "background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"
            
            # Gather all subsequent elements
            siblings = list(h2.next_siblings)
            
            # Wrap h2 itself
            h2.wrap(wrapper)
            
            # Move all siblings into the wrapper
            for sibling in siblings:
                wrapper.append(sibling)
            
            break

    return str(soup)'''
    
    c = c.replace('return str(soup)', inject_code)
    
    with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
        f.write(c)

update_mammoth_script()
print("Updated mammoth_html_wrap.py with Section 7 wrapping logic!")
