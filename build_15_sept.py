import re
import os
import mammoth
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 15 September 2026.docx'

with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    raw_html = result.value

soup = BeautifulSoup(raw_html, 'html.parser')

title_p = soup.find('p')
title_text = title_p.get_text(strip=True) if title_p else ''
if title_p:
    title_p.extract()

subtitle_p = soup.find('p')
subtitle_text = subtitle_p.get_text(strip=True) if subtitle_p else ''
if subtitle_p:
    subtitle_p.extract()

header_box_html = f'''<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">{title_text}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{subtitle_text}</p>
</div>'''

header_soup = BeautifulSoup(header_box_html, 'html.parser')
soup.insert(0, header_soup.div)

for p in soup.find_all('p'):
    strong = p.find('strong')
    if strong and p.get_text(strip=True) == strong.get_text(strip=True):
        text = p.get_text(strip=True)
        if re.match(r'^[1-6]\.', text):
            new_h2 = soup.new_tag('h2', style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;")
            new_h2.string = text
            p.replace_with(new_h2)
        elif re.match(r'^7\.', text):
            sec7_div = BeautifulSoup(f'''<div class="" style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">
    <h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">{text}</h3>
</div>''', 'html.parser').div
            p.insert_after(sec7_div)
            current = sec7_div.next_sibling
            while current:
                next_sib = current.next_sibling
                if current.name == 'p' and current.get_text(strip=True).startswith('For general informational'):
                    break
                sec7_div.append(current)
                current = next_sib
            p.extract()

for p in soup.find_all('p'):
    if p.get_text(strip=True).startswith('For general informational'):
        disclaimer_html = f'''<div class="article-disclaimer" style="margin-top: 3rem; font-size: 0.85rem; color: #666; border-top: 1px solid var(--stone); padding-top: 1rem;">
<p><em>{p.get_text(strip=True)}</em></p>
</div>'''
        p.replace_with(BeautifulSoup(disclaimer_html, 'html.parser').div)

for elem in soup.find_all(string=re.compile('\ufffd')):
    elem.replace_with(elem.replace('\ufffd', '-'))

for table in soup.find_all('table'):
    table['class'] = 'data-table'
    table['style'] = "width: 100%; border-collapse: collapse;"
    
    wrapper = soup.new_tag('div', **{'class': 'table-responsive', 'style': 'overflow-x: auto; margin-bottom: 1rem;'})
    table.wrap(wrapper)
    
    thead = table.find('thead')
    if thead:
        tr = thead.find('tr')
        if tr:
            tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
            for th in tr.find_all('th'):
                th['style'] = "padding: 1rem; color: #ffffff !important;"
                if th.p:
                    th.string = th.p.get_text()

    tbody = table.find('tbody')
    if tbody:
        for i, tr in enumerate(tbody.find_all('tr')):
            if i % 2 != 0:
                tr['style'] = "background-color: var(--cream);"
            
            for j, td in enumerate(tr.find_all('td')):
                td['style'] = "padding: 1rem;"
                if td.p:
                    strong_tag = td.p.find('strong')
                    if strong_tag:
                        td.clear()
                        new_strong = soup.new_tag('strong')
                        if j == 0:
                            new_strong['style'] = "color: #000;"
                        new_strong.string = strong_tag.get_text()
                        td.append(new_strong)
                    else:
                        td.string = td.p.get_text()
                
                cell_text = td.get_text(strip=True)
                if cell_text.startswith('+'):
                    td['style'] += " color: var(--gain); font-weight: 600;"
                elif cell_text.startswith('-'):
                    td['style'] += " color: var(--loss); font-weight: 600;"

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

template_soup = BeautifulSoup(template_html, 'html.parser')

title_tag = template_soup.find('title')
if title_tag:
    title_tag.string = 'Daily DSE Wrap | Tuesday, 15th September 2026 | Amana Capital East Africa'

desc_tag = template_soup.find('meta', attrs={'name': 'description'})
if desc_tag:
    desc_tag['content'] = 'Read our daily Dar es Salaam Stock Exchange (DSE) wrap for 15 Sep 2026. Get institutional-grade market intelligence, top movers, and equity research from Amana Capital East Africa.'

canonical_tag = template_soup.find('link', attrs={'rel': 'canonical'})
if canonical_tag:
    canonical_tag['href'] = 'https://www.amana-capital-ea.co.tz/dse-wrap-2026-09-15.html'

for span in template_soup.find_all('span'):
    if span.get_text() == '14 Sep 2026':
        span.string = '15 Sep 2026'

card = template_soup.find('div', class_='card dse-article-card')
if card:
    card.clear()
    for child in list(soup.contents):
        card.append(child)

output_html = str(template_soup)
output_html = output_html.replace('&#169;', '&copy;')
output_html = output_html.replace('&#183;', '&middot;')

with open('dse-wrap-2026-09-15.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

print("Created dse-wrap-2026-09-15.html")
