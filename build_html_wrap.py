import os
import re
from datetime import datetime
import markdown

def build_wrap_html(markdown_path, template_path, output_path):
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file {markdown_path} not found.")
        return False
        
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Extract Title and Subtitle
    # Assuming first line is title e.g. "Daily DSE Wrap | Friday, 12 August 2026"
    lines = md_content.split('\n')
    title_line = ""
    subtitle_line = ""
    content_lines = []
    
    # We might have some blank lines at the top
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
    
    # Parse date string for YYYY-MM-DD
    # E.g. "Friday, 7 August 2026" or "12 August 2026"
    try:
        # Try to extract just the date part if there's a day of week
        date_part = date_string.split(', ')[-1] if ', ' in date_string else date_string
        parsed_date = datetime.strptime(date_part.strip(), '%d %B %Y')
        yyyy_mm_dd = parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        print("Warning: Could not parse date perfectly, using default for filename URL")
        yyyy_mm_dd = "2026-08-12" # Fallback
        
    # Convert remaining markdown to HTML
    html_content = markdown.markdown(content_md, extensions=['tables'])
    
    # Apply specific CSS styling
    # 1. H2 Tags
    html_content = re.sub(r'<h2>', r'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">', html_content)
    
    # 2. H3 Tags (for "Considerations for a Multi-Year Framework" etc)
    html_content = re.sub(r'<h3>', r'<h3 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">', html_content)
    
    # 3. Tables
    html_content = re.sub(
        r'<table>', 
        r'<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">\n<table class="data-table" style="width: 100%; border-collapse: collapse;">', 
        html_content
    )
    html_content = re.sub(r'</table>', r'</table>\n</div>', html_content)
    
    # Table headers
    html_content = re.sub(r'<thead>', r'<thead>\n<tr style="background-color: var(--navy); color: var(--white); text-align: left;">', html_content)
    html_content = re.sub(r'<th>', r'<th style="padding: 1rem;">', html_content)
    
    # Remove the default <tr> inside <thead> because we just added one
    html_content = re.sub(r'<tr style="background-color: var\(--navy\); color: var\(--white\); text-align: left;">\s*<tr>', r'<tr style="background-color: var(--navy); color: var(--white); text-align: left;">', html_content)
    
    # Table body rows - alternate colors
    tbody_split = html_content.split('<tbody>')
    if len(tbody_split) > 1:
        new_html = tbody_split[0]
        for i in range(1, len(tbody_split)):
            tbody_part = tbody_split[i]
            trs = tbody_part.split('<tr>')
            new_tbody = trs[0]
            for j in range(1, len(trs)):
                if j % 2 == 0:
                    new_tbody += '<tr style="background-color: var(--cream);">' + trs[j]
                else:
                    new_tbody += '<tr>' + trs[j]
            new_html += '<tbody>' + new_tbody
        html_content = new_html

    # Table cells
    html_content = re.sub(r'<td>', r'<td style="padding: 1rem;">', html_content)
    
    # Links
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
