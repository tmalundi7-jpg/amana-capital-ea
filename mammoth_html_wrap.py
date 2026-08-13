import os
import re
import argparse
import mammoth
from bs4 import BeautifulSoup
import datetime

def process_mammoth_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Format headings
    for p in soup.find_all('p'):
        if p.find('strong') and p.text.strip() == p.find('strong').text.strip():
            text = p.text.strip()
            if re.match(r'^\d+\.\s', text):
                new_h2 = soup.new_tag('h2')
                new_h2['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
                new_h2.string = text
                p.replace_with(new_h2)

    # Format tables
    for table in soup.find_all('table'):
        table['class'] = ['data-table']
        table['style'] = "width: 100%; border-collapse: collapse;"
        
        wrapper = soup.new_tag('div')
        wrapper['class'] = ['table-responsive']
        wrapper['style'] = "overflow-x: auto; margin-bottom: 1rem;"
        table.wrap(wrapper)
        
        thead = table.find('thead')
        if thead:
            for tr in thead.find_all('tr'):
                tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
                for th in tr.find_all('th'):
                    th['style'] = "padding: 1rem;"
                    if th.find('p'):
                        th.string = th.find('p').text

        tbody = table.find('tbody')
        if tbody:
            for i, tr in enumerate(tbody.find_all('tr')):
                if i % 2 == 1:
                    tr['style'] = "background-color: var(--cream);"
                
                tds = tr.find_all('td')
                for col_idx, td in enumerate(tds):
                    td['style'] = "padding: 1rem;"
                    if td.find('p'):
                        text = td.find('p').text
                        td.clear()
                        td.append(text)

                    if col_idx == 0 and td.text.strip().isupper():
                        td['style'] = "padding: 1rem; font-weight: 600;"
                        strong = soup.new_tag('strong')
                        strong['style'] = "color: #000;"
                        strong.string = td.text
                        td.clear()
                        td.append(strong)
                        
                    if '%' in td.text:
                        text = td.text.strip()
                        if text.startswith('+'):
                            td['style'] = "padding: 1rem; color: var(--gain); font-weight: 600;"
                        elif text.startswith('-') or text.startswith('–'):
                            td['style'] = "padding: 1rem; color: var(--loss); font-weight: 600;"
    
    return str(soup)

def main():
    parser = argparse.ArgumentParser(description="Generate styled DSE wrap HTML from a Word Document")
    parser.add_argument("docx_path", help="Path to the input .docx file")
    parser.add_argument("date", help="Date in YYYY-MM-DD format (e.g. 2026-08-13)")
    args = parser.parse_args()

    docx_path = args.docx_path
    yyyy_mm_dd = args.date
    
    date_obj = datetime.datetime.strptime(yyyy_mm_dd, '%Y-%m-%d')
    date_str = date_obj.strftime(f'%A, {date_obj.day} %B %Y')

    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        raw_html = result.value

    # Extract title and subtitle
    match = re.match(r'<p><strong>(.*?)</strong></p><p><strong>(.*?)</strong></p>(.*)', raw_html, re.DOTALL)
    if not match:
        match2 = re.match(r'<p><strong>(.*?)</strong></p><p>(.*?)</p>(.*)', raw_html, re.DOTALL)
        if not match2:
            print("Failed to find title/subtitle. Ensure the docx starts with a bold title and subtitle.")
            return
        else:
            title = match2.group(1)
            subtitle = match2.group(2)
            rest_of_article = match2.group(3)
    else:
        title = match.group(1)
        subtitle = match.group(2)
        rest_of_article = match.group(3)

    # Process the HTML
    processed_html = process_mammoth_html(rest_of_article)

    # Create the full article HTML
    article_html = f'''<div class=\"dse-header-box\" style=\"background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);\">
                    <h1 style=\"margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;\">{title}</h1>
                    <p style=\"font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;\">{subtitle}</p>
                </div>
                {processed_html}
'''

    template_path = os.path.join("templates", "wrap_template.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    final_html = template.replace('{{DATE_STRING}}', date_str)
    final_html = final_html.replace('{{YYYY_MM_DD}}', yyyy_mm_dd)
    final_html = final_html.replace('{{SUBTITLE}}', subtitle)
    final_html = final_html.replace('{{CONTENT}}', article_html)

    output_path = f"dse-wrap-{yyyy_mm_dd}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Successfully created {output_path} with 07 August formatting!")

if __name__ == "__main__":
    main()
