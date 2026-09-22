import mammoth
import re
from bs4 import BeautifulSoup

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx'

with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value

soup = BeautifulSoup(html, 'html.parser')

# Get excerpt (first paragraph that's long enough)
excerpt = ""
for p in soup.find_all('p'):
    t = p.get_text(strip=True)
    if len(t) > 50 and "Friday 18th September 2026" not in t:
        excerpt = t
        break

if len(excerpt) > 200:
    excerpt = excerpt[:197] + "..."
print(f"Excerpt: {excerpt}")

# Fix headers
for h2 in soup.find_all('h2'):
    h2['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
    
for h3 in soup.find_all('h3'):
    h3['style'] = "color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;"

# Remove h1
for h1 in soup.find_all('h1'):
    h1.decompose()

# Remove the date paragraph
for p in soup.find_all('p'):
    if 'Friday 18th September 2026' in p.get_text():
        p.decompose()

# Fix Tables
for table in soup.find_all('table'):
    table['class'] = "data-table"
    table['style'] = "width: 100%; border-collapse: collapse;"
    # wrap in table-responsive
    wrapper = soup.new_tag('div', **{'class': 'table-responsive', 'style': 'overflow-x: auto; margin-bottom: 1rem;'})
    table.insert_before(wrapper)
    wrapper.append(table)
    
    # Process rows
    for i, tr in enumerate(table.find_all('tr')):
        if i == 0:
            # Header
            tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
            for th in tr.find_all(['td', 'th']):
                th.name = 'th'
                th['style'] = "padding: 1rem;"
        else:
            if i % 2 == 0:
                tr['style'] = "background-color: var(--cream);"
            for j, td in enumerate(tr.find_all('td')):
                style = "padding: 1rem;"
                # make first column bold
                if j == 0:
                    style += " font-weight: 600;"
                    # wrap content in strong
                    inner = td.get_text()
                    td.string = ''
                    s = soup.new_tag('strong', style="color: #000;")
                    s.string = inner
                    td.append(s)
                
                # Check for + / - for coloring
                txt = td.get_text()
                if '+' in txt:
                    style += " color: var(--gain); font-weight: 600;"
                elif '-' in txt or '−' in txt or '' in txt:
                    style += " color: var(--loss); font-weight: 600;"
                    
                td['style'] = style

# Reformat section 7 block
h3_section7 = None
for h3 in soup.find_all('h3'):
    if '7. Considerations for a Multi-Year Framework' in h3.get_text():
        h3_section7 = h3
        break

if h3_section7:
    div = soup.new_tag('div', style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;")
    h3_section7.insert_before(div)
    div.append(h3_section7)
    
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

body_html = "".join([str(tag) for tag in soup.contents])

# Open 17th html
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    template_soup = BeautifulSoup(f.read(), 'html.parser')

# Get card
h1 = template_soup.find('h1')
card = h1.parent.parent

# Change H1
h1.string = "Daily DSE Wrap | Friday, 18th September 2026"

# Change Date
date_p = h1.find_next_sibling('p')
# Update the title of the wrap in the date
# wait, what was the title for 18th? 
# "The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Friday..."
# Wait, let's just make the date_p text empty or extract the first bold line from the docx?
# Let's check the docx title.
