import os
import mammoth
from bs4 import BeautifulSoup
import re

def build_wrap():
    # 1. Read the 07 Sep wrap to get prefix and suffix
    with open('dse-wrap-2026-09-07.html', 'r', encoding='utf-8') as f:
        html_07 = f.read()

    split_start = html_07.find('<div class="card dse-article-card" style="padding: 3rem;">')
    if split_start == -1:
        print("FAIL: Could not find card start")
        return
        
    prefix = html_07[:split_start]
    
    # The card ends before:
    # </div>
    # </div>
    # </main>
    # Let's find </main> and go back two divs.
    split_end = html_07.find('</div>\n          </div>\n      </main>')
    if split_end == -1:
        # Fallback search
        split_end = html_07.find('</div>\n</div>\n</main>')
        if split_end == -1:
            split_end = html_07.find('</main>') - 25 # approximate
    
    # Let's just find the closing tags safely by regex
    m = re.search(r'(</div>\s*</div>\s*</main>)', html_07)
    if m:
        suffix = m.group(1) + html_07[m.end(1):]
    else:
        print("FAIL: Could not find suffix")
        return

    # 2. Extract content from DOCX 14 Sep
    docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 14 September 2026.docx'
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        raw_html = result.value

    soup = BeautifulSoup(raw_html, 'html.parser')

    # Title and Subtitle
    title_p = soup.find('p')
    title_text = title_p.get_text(strip=True) if title_p else ''
    if title_p: title_p.extract()

    subtitle_p = soup.find('p')
    subtitle_text = subtitle_p.get_text(strip=True) if subtitle_p else ''
    if subtitle_p: subtitle_p.extract()

    # Generate header box matching 07 Sep
    header_box_html = f'''<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">{title_text}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{subtitle_text}</p>
</div>'''
    
    header_soup = BeautifulSoup(header_box_html, 'html.parser')
    soup.insert(0, header_soup.div)

    # Style paragraphs and h2s
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
                    next_p['style'] = "color: var(--navy); line-height: 1.8;"
                    new_div.append(next_p)
            else:
                p['style'] = "font-size: 1.05rem; color: var(--navy); line-height: 1.7; margin-bottom: 1.25rem;"
        else:
            p['style'] = "font-size: 1.05rem; color: var(--navy); line-height: 1.7; margin-bottom: 1.25rem;"

    # Tables styling
    for table in soup.find_all('table'):
        table['class'] = "data-table"
        table['style'] = "width: 100%; border-collapse: collapse;"
        
        # wrap table in a div
        wrapper = soup.new_tag('div', **{'class': 'table-responsive', 'style': 'overflow-x: auto; margin-bottom: 1rem;'})
        table.wrap(wrapper)

        # Style header
        thead = soup.new_tag('thead')
        first_tr = table.find('tr')
        if first_tr:
            first_tr.wrap(thead)
            first_tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
            for th in first_tr.find_all('td'):
                th.name = 'th'
                th['style'] = "padding: 1rem;"

        # Style body
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

    # The disclaimer is usually the last paragraph
    last_p = soup.find_all('p')[-1]
    last_p['style'] = "font-size: 0.85rem; color: var(--mist); margin-top: 3rem; border-top: 1px solid rgba(200, 150, 46, 0.2); padding-top: 1rem;"

    content = f'<div class="card dse-article-card" style="padding: 3rem;">\n{str(soup)}\n</div>'

    # Fix title in prefix
    prefix = prefix.replace('<title>Daily DSE Wrap | Monday, 7th September 2026 | Amana Capital East Africa</title>', f'<title>{title_text} | Amana Capital East Africa</title>')
    prefix = prefix.replace('content="Daily DSE Wrap | Monday, 7th September 2026"', f'content="{title_text}"')

    with open('dse-wrap-2026-09-14.html', 'w', encoding='utf-8') as f:
        f.write(prefix + content + suffix)
    print("dse-wrap-2026-09-14.html successfully fixed.")

build_wrap()
