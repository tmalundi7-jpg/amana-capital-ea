import mammoth
import re
from bs4 import BeautifulSoup
import os

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx'

with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value

soup = BeautifulSoup(html, 'html.parser')

# Get excerpt (first paragraph)
excerpt = ""
for p in soup.find_all('p'):
    if len(p.get_text(strip=True)) > 20:
        excerpt = p.get_text(strip=True)
        break

# Truncate excerpt
if len(excerpt) > 200:
    excerpt = excerpt[:197] + "..."

print(f"Excerpt: {excerpt}")

# Fix headers
for h2 in soup.find_all('h2'):
    h2['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
    
for h3 in soup.find_all('h3'):
    h3['style'] = "color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;"

# Reformat the section 7 block if it exists
h3_section7 = None
for h3 in soup.find_all('h3'):
    if '7. Considerations for a Multi-Year Framework' in h3.get_text():
        h3_section7 = h3
        break
        
if h3_section7:
    # Wrap section 7 in the special div
    div = soup.new_tag('div', style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;")
    h3_section7.insert_before(div)
    div.append(h3_section7)
    
    # move subsequent paragraphs into the div until disclaimer or end
    curr = div.find_next_sibling()
    while curr:
        nxt = curr.find_next_sibling()
        if curr.name == 'p' and 'For general informational and educational purposes only' in curr.get_text():
            curr.name = 'p'
            curr.string = ''
            em = soup.new_tag('em')
            em.string = 'For general informational and educational purposes only; not financial, legal, or tax advice. All investment decisions are solely your responsibility. Capital is at risk, and past performance does not guarantee future results. Amana Capital East Africa Limited registration under CMSA, Tanzania is pending. Registration does not imply CMSA endorsement.'
            curr.append(em)
            div.append(curr)
            break
        div.append(curr)
        curr = nxt

body_html = str(soup)

# Remove the title/date if mammoth extracted it as p or h1
body_html = re.sub(r'<h1>.*?</h1>', '', body_html)
body_html = re.sub(r'<p><strong>Friday 18th September 2026</strong></p>', '', body_html)
body_html = re.sub(r'<p>Friday 18th September 2026</p>', '', body_html)

# Read 17th html
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace body
new_html = re.sub(r'(<div class="article-content">).*?(<div class="article-disclaimer")', fr'\g<1>{body_html}\g<2>', template, flags=re.DOTALL)

# Replace Date strings
new_html = new_html.replace('Thursday, 17th September 2026', 'Friday, 18th September 2026')
new_html = new_html.replace('17 Sep 2026', '18 Sep 2026')

with open('dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Created dse-wrap-2026-09-18.html")
with open('temp_excerpt.txt', 'w', encoding='utf-8') as f:
    f.write(excerpt)

