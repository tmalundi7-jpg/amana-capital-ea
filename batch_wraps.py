import os
import mammoth
from bs4 import BeautifulSoup
import re
from datetime import datetime

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

def process_wrap(day):
    date_str = f"2026-09-{day}"
    docx_path = f"C:\\Users\\tmalu\\Documents\\Daily DSE Wrap {int(day)} September 2026.docx"
    
    # Check if docx exists
    if not os.path.exists(docx_path):
        print(f"Missing {docx_path}")
        return None
        
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
    excerpt = ""
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
            
            # Capture first real paragraph for excerpt
            if not excerpt and "font-size: 1.05rem" in p.get('style', '') and p.get_text(strip=True):
                # Don't capture disclaimer or footnotes
                if "Amana Capital" not in p.get_text() and "disclaimer" not in p.get_text().lower():
                    excerpt = p.get_text(strip=True)

    # Tables styling
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

    out_file = f'dse-wrap-{date_str}.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(prefix + content + suffix)
    print(f"{out_file} generated.")
    
    # Excerpt truncation to ~170 chars
    if len(excerpt) > 170:
        excerpt = excerpt[:167] + "..."
    elif not excerpt:
        excerpt = subtitle_text
        
    return {
        'day': day,
        'title': title_text,
        'subtitle': subtitle_text,
        'excerpt': excerpt
    }

results = []
for day in ['08', '09', '10', '11']:
    res = process_wrap(day)
    if res:
        results.append(res)
        
# Generate archive rows
# The format in market-intelligence-archive.html:
# <div class="arc-row">
# <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">7 Sep 2026</div>
# <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Monday, 7th September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">Bond money floods into equities as the rotation signal fires. Equity turnover more than doubled to TZS 17.31 billion while bond turnover collapsed to TZS 7.99 billion. The TSI crossed 10,000...</div></div>
# <a href="/dse-wrap-2026-09-07" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
# </div>

import datetime
archive_rows_html = ""
for res in reversed(results): # 11, 10, 9, 8
    day = res['day']
    dt = datetime.datetime.strptime(f"2026-09-{day}", "%Y-%m-%d")
    date_formatted = f"{int(day)} Sep 2026"
    title = res['title']
    excerpt = res['subtitle'] + ". " + res['excerpt']
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."
    
    row = f'''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">{date_formatted}</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">{title}</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">{excerpt}</div></div>
<a href="/dse-wrap-2026-09-{day}" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>
'''
    archive_rows_html += row
    
# Now insert into market-intelligence-archive.html BEFORE the 7 Sep row
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arch = f.read()

target = '<div class="arc-row">\n<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">7 Sep 2026</div>'
if target in arch:
    arch = arch.replace(target, archive_rows_html + target)
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(arch)
    print("market-intelligence-archive.html successfully updated.")
else:
    print("FAIL: Could not find 7 Sep 2026 target row in archive")

