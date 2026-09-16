import os
import mammoth
from bs4 import BeautifulSoup
import re

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

def process_wrap(day):
    date_str = f"2026-09-{day}"
    day_no_pad = str(int(day))
    docx_path = f"C:\\Users\\tmalu\\Documents\\Daily DSE Wrap {day_no_pad} September 2026.docx"
    if not os.path.exists(docx_path):
        docx_path = f"C:\\Users\\tmalu\\Documents\\Daily DSE Wrap {day} September 2026.docx"
        if not os.path.exists(docx_path):
            print(f"Missing {docx_path}")
            return
            
    with open('dse-wrap-2026-09-07.html', 'r', encoding='utf-8') as f:
        html_07 = f.read()

    split_start = html_07.find('<div class="card dse-article-card" style="padding: 3rem;">')
    prefix = html_07[:split_start]
    
    m = re.search(r'(</div>\s*</div>\s*</main>)', html_07)
    suffix = m.group(1) + html_07[m.end(1):]

    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        raw_html = result.value

    soup = BeautifulSoup(raw_html, 'html.parser')

    title_p = soup.find('p')
    title_text = title_p.get_text(strip=True) if title_p else ''
    if title_p: title_p.extract()

    subtitle_p = soup.find('p')
    subtitle_text = subtitle_p.get_text(strip=True) if subtitle_p else ''
    if subtitle_p: subtitle_p.extract()

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
</div>''', 'html.parser')
                new_div = sec7_div.div
                p.replace_with(new_div)
                next_p = new_div.find_next_sibling('p')
                if next_p:
                    next_p.extract()
                    new_div.append(next_p)
            else:
                pass
        else:
            pass

    for table in soup.find_all('table'):
        table['class'] = "data-table"
        table['style'] = "width: 100%; border-collapse: collapse;"
        
        wrapper = soup.new_tag('div', **{'class': 'table-responsive', 'style': 'overflow-x: auto; margin-bottom: 1rem;'})
        table.wrap(wrapper)

        thead = soup.new_tag('thead')
        first_tr = table.find('tr')
        if first_tr:
            first_tr.wrap(thead)
            first_tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
            for th in first_tr.find_all('td'):
                th.name = 'th'
                th['style'] = "padding: 1rem;"

        tbody = soup.new_tag('tbody')
        for i, tr in enumerate(table.find_all('tr')):
            if tr.parent.name == 'thead': continue
            tr.wrap(tbody)
            if i % 2 == 1:
                tr['style'] = "background-color: var(--cream);"
            for td in tr.find_all('td'):
                td['style'] = "padding: 1rem;"
                if '+' in td.get_text():
                    td['style'] += " color: var(--gain); font-weight: 600;"
                elif '-' in td.get_text() or '–' in td.get_text():
                    td['style'] += " color: var(--loss); font-weight: 600;"
                    
                strong_text = td.find('strong')
                if strong_text:
                    strong_text['style'] = "color: #000;"

    last_p = soup.find_all('p')[-1]
    last_p['style'] = "font-size: 0.85rem; color: var(--mist); margin-top: 3rem; border-top: 1px solid rgba(200, 150, 46, 0.2); padding-top: 1rem;"

    content = f'<div class="card dse-article-card" style="padding: 3rem;">\n{str(soup)}\n</div>'

    prefix = prefix.replace('<title>Daily DSE Wrap | Monday, 7th September 2026 | Amana Capital East Africa</title>', f'<title>{title_text} | Amana Capital East Africa</title>')
    prefix = prefix.replace('content="Daily DSE Wrap | Monday, 7th September 2026"', f'content="{title_text}"')
    
    prefix = prefix.replace('dse-wrap-2026-09-07.html', f'dse-wrap-{date_str}.html')

    out_file = f'dse-wrap-{date_str}.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(prefix + content + suffix)
    print(f"{out_file} successfully regenerated.")

for day in ['08', '09']:
    process_wrap(day)

