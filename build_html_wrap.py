import os
import re
from datetime import datetime
import markdown
import bs4

def build_wrap_html(markdown_path, template_path, output_path):
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file {markdown_path} not found.")
        return False
        
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Extract Title and Subtitle
    lines = md_content.split('\n')
    title_line = ""
    subtitle_line = ""
    content_lines = []
    
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip():
            title_line = line.replace('# ', '').replace('`', '').strip()
            # The next non-empty line is the subtitle
            for j in range(i+1, len(lines)):
                if lines[j].strip():
                    subtitle_line = lines[j].strip()
                    start_idx = j + 1
                    break
            break
            
    content_lines = lines[start_idx:]
    content_md = '\n'.join(content_lines)
    
    # Extract date string from title
    date_string = title_line.replace("Daily DSE Wrap |", "").strip()
    
    try:
        date_part = date_string.split(', ')[-1] if ', ' in date_string else date_string
        parsed_date = datetime.strptime(date_part.strip(), '%d %B %Y')
        yyyy_mm_dd = parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        print("Warning: Could not parse date perfectly, using default for filename URL")
        yyyy_mm_dd = "2026-08-12" # Fallback
        
    # Convert remaining markdown to HTML
    html_content = markdown.markdown(content_md, extensions=['tables'])
    
    # Use BeautifulSoup for precise table formatting
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # 1. H2 Tags
    for h2 in soup.find_all('h2'):
        h2['style'] = "color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;"
        
    # 2. Tables
    for table in soup.find_all('table'):
        # Wrap table in responsive div
        wrapper = soup.new_tag('div', style="overflow-x: auto; margin-bottom: 1rem;", **{'class': 'table-responsive'})
        table.wrap(wrapper)
        table['style'] = "width: 100%; border-collapse: collapse;"
        table['class'] = "data-table"
        
        # Format Headers
        thead = table.find('thead')
        if thead:
            for tr in thead.find_all('tr'):
                tr['style'] = "background-color: var(--navy); color: var(--white); text-align: left;"
                for th in tr.find_all('th'):
                    th['style'] = "padding: 1rem;"
                    
        # Format Body Rows
        tbody = table.find('tbody')
        if tbody:
            for i, tr in enumerate(tbody.find_all('tr')):
                if i % 2 == 1:
                    tr['style'] = "background-color: var(--cream);"
                    
                cells = tr.find_all('td')
                for j, td in enumerate(cells):
                    text_content = td.get_text().strip()
                    style = "padding: 1rem;"
                    
                    if j == 0:
                        # First column
                        style += " font-weight: 600;"
                        inner_text = td.string
                        if inner_text:
                            strong_tag = soup.new_tag('strong', style="color: #000;")
                            strong_tag.string = inner_text
                            td.string = ""
                            td.append(strong_tag)
                        else:
                            # If it already contains elements, wrap them
                            wrapper_strong = soup.new_tag('strong', style="color: #000;")
                            for child in list(td.children):
                                wrapper_strong.append(child)
                            td.append(wrapper_strong)
                    else:
                        # Gain/Loss styling
                        # Use negative lookbehind or simple matching to avoid matching the first column
                        if '+' in text_content and ('%' in text_content or 'pts' in text_content or '+' == text_content[0]):
                            style += " color: var(--gain); font-weight: 600;"
                        elif ('-' in text_content or '–' in text_content or '−' in text_content) and ('%' in text_content or 'pts' in text_content or '-' == text_content[0] or '–' == text_content[0]):
                            style += " color: var(--loss); font-weight: 600;"
                            
                    td['style'] = style
    
    # Update HTML string
    html_content = str(soup)
    
    # 3. Links
    html_content = re.sub(r'<a href=', r'<a class="gold-link" href=', html_content)
    
    # Apply to template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    final_html = template.replace('{{DATE_STRING}}', date_string)
    final_html = final_html.replace('{{YYYY_MM_DD}}', yyyy_mm_dd)
    final_html = final_html.replace('{{SUBTITLE}}', subtitle_line)
    final_html = final_html.replace('{{CONTENT}}', html_content)
    
    # Fix the considerations block formatting if it exists
    heading_pattern = r'<h[23][^>]*>(?:\d+\.\s*)?Considerations for a Multi-Year Framework</h[23]>'
    section_pattern = re.compile(rf'({heading_pattern}.*?)$', re.DOTALL)
    
    def section_replacer(m):
        sec_content = m.group(1)
        sec_content = re.sub(
            r'<h[23][^>]*>((?:\d+\.\s*)?Considerations for a Multi-Year Framework)</h[23]>', 
            r'<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem;">\1</h3>', 
            sec_content
        )
        wrapped = f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{sec_content.strip()}\n</div>'
        return wrapped

    if re.search(heading_pattern, final_html):
        final_html = section_pattern.sub(section_replacer, final_html)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Successfully built {output_path}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        build_wrap_html(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python build_html_wrap.py <input.md> <template.html> <output.html>")
