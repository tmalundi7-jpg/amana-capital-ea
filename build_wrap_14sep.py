import re
import os
import mammoth
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 14 September 2026.docx'

with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    raw_html = result.value

# Use BeautifulSoup to parse and manipulate
soup = BeautifulSoup(raw_html, 'html.parser')

# Find the first paragraph (Title)
title_p = soup.find('p')
title_text = title_p.get_text(strip=True) if title_p else ''
if title_p:
    title_p.extract()

# Find the second paragraph (Subtitle)
subtitle_p = soup.find('p')
subtitle_text = subtitle_p.get_text(strip=True) if subtitle_p else ''
if subtitle_p:
    subtitle_p.extract()

# Generate header box
header_box_html = f'''<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">{title_text}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{subtitle_text}</p>
</div>'''

header_soup = BeautifulSoup(header_box_html, 'html.parser')
soup.insert(0, header_soup.div)

# Process paragraphs and tables
for p in soup.find_all('p'):
    strong = p.find('strong')
    if strong and p.get_text(strip=True) == strong.get_text(strip=True):
        text = p.get_text(strip=True)
        if re.match(r'^[1-6]\.', text):
            new_h2 = soup.new_tag('h2', style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;")
            new_h2.string = text
            p.replace_with(new_h2)
        elif re.match(r'^7\.', text):
            # Section 7 Multi-year framework
            sec7_div = BeautifulSoup(f'''<div class="" style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">
    <h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">{text}</h3>
</div>''', 'html.parser')
            new_div = sec7_div.div
            p.replace_with(new_div)
            # Find next paragraph and insert into div
            next_p = new_div.find_next_sibling('p')
            if next_p:
                next_p.extract()
                next_p['style'] = "color: var(--navy); line-height: 1.8;"
                new_div.append(next_p)
        else:
            p['style'] = "font-size: 1.05rem; color: var(--navy); line-height: 1.7; margin-bottom: 1.25rem;"
    else:
        p['style'] = "font-size: 1.05rem; color: var(--navy); line-height: 1.7; margin-bottom: 1.25rem;"

# Tables styling
for table in soup.find_all('table'):
    table['class'] = "data-table gold-grid-table"
    table['style'] = "width: 100%; border-collapse: collapse; margin-bottom: 2rem; background-color: var(--cream); color: var(--navy);"
    for th in table.find_all('th'):
        th['style'] = "padding: 1rem; border-bottom: 2px solid var(--gold); background-color: rgba(200, 150, 46, 0.1); color: var(--navy);"
    for td in table.find_all('td'):
        td['style'] = "padding: 1rem; border-bottom: 1px solid rgba(200, 150, 46, 0.2);"
        if 'TZS' in td.get_text() or '%' in td.get_text() or re.match(r'^[\d,\.]+$', td.get_text().strip()):
            td['class'] = "text-right"
        if '+' in td.get_text():
            td['class'] = td.get('class', '') + " change-positive"
        elif '-' in td.get_text():
            td['class'] = td.get('class', '') + " change-negative"

# The disclaimer is usually the last paragraph. Let's make it small.
last_p = soup.find_all('p')[-1]
last_p['style'] = "font-size: 0.85rem; color: var(--mist); margin-top: 3rem; border-top: 1px solid rgba(200, 150, 46, 0.2); padding-top: 1rem;"

with open('wrap_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Make sure title is updated
template = template.replace('<title>Daily DSE Wrap | Amana Capital East Africa</title>', f'<title>{title_text} | Amana Capital East Africa</title>')
template = template.replace('<!-- WRAP_CONTENT -->', str(soup))

with open('dse-wrap-2026-09-14.html', 'w', encoding='utf-8') as f:
    f.write(template)
print('dse-wrap-2026-09-14.html generated')

