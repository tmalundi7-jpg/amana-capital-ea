import docx
import re

filepath = r"C:\Users\tmalu\OneDrive\Documents\To update investor education page of Amana Capital EA website.docx"
doc = docx.Document(filepath)

target_article = "Article 1.7"
lines_content = []

from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P): yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl): yield Table(child, parent)

def get_html_from_paragraph(p):
    # Returns a list of lines since a paragraph can contain \n
    lines = []
    current_line = ""
    raw_text = p.text.strip()
    if not raw_text: return []
    
    bold_len = sum(len(run.text) for run in p.runs if run.bold)
    keep_bold = bold_len < len(raw_text) * 0.5
    
    for run in p.runs:
        text = run.text.replace("<", "&lt;").replace(">", "&gt;")
        if not text: continue
        
        parts = text.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                lines.append(current_line.strip())
                current_line = ""
            
            if part.strip():
                if run.bold and keep_bold:
                    current_line += f"<strong>{part}</strong>"
                elif run.italic:
                    current_line += f"<em>{part}</em>"
                else:
                    current_line += part
                    
    if current_line.strip():
        lines.append(current_line.strip())
        
    return lines

in_list = False
found_article = False

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        text = block.text.strip()
        
        match = re.match(r'^(Article 1\.7)\s*[-–—]\s*(.*)', text)
        if match:
            found_article = True
            title = match.group(2)
            lines_content.append(f"<h1>Article 1.7 - {title}</h1>")
            continue
            
        if found_article and (re.match(r'^Article \d\.\d', text) or "Article 6.6" in text):
            if in_list:
                lines_content.append("</ul>")
                in_list = False
            break
            
        if found_article:
            html_lines = get_html_from_paragraph(block)
            for html_text in html_lines:
                if not html_text: continue
                
                is_bullet = False
                if html_text.startswith("- ") or html_text.startswith("• "):
                    is_bullet = True
                    html_text = html_text[2:].strip()
                    
                if is_bullet:
                    if not in_list:
                        lines_content.append("<ul>")
                        in_list = True
                    lines_content.append(f"<li>{html_text}</li>")
                    continue
                else:
                    if in_list:
                        lines_content.append("</ul>")
                        in_list = False

                if html_text.startswith("By Amana Capital"):
                    lines_content.append(f"<p><em><strong>{html_text}</strong></em></p>")
                elif html_text.startswith("This document is for general") or "This content is for informational" in html_text:
                    lines_content.append(f'<div class="article-disclaimer"><p>{html_text}</p></div>')
                elif "Further Reading" in html_text:
                    if html_text == "Further Reading":
                        continue
                    lines_content.append(f'<div class="further-reading"><p><strong>Further Reading</strong></p><p>{html_text.replace("Further Reading: ", "").replace("<strong>Further Reading</strong>", "")}</p></div>')
                elif "Put It Into Practice" in html_text:
                    lines_content.append(f'<div class="apply-it"><p><strong>Put It Into Practice</strong></p>')
                elif "Open today" in html_text or ("daily DSE wrap" in html_text.lower() and "practice" in "".join(lines_content[-2:]).lower()):
                     lines_content.append(f'<p>{html_text}</p></div>')
                elif re.match(r'^<strong>\d\.\s', html_text) or re.match(r'^\d\.\s', html_text):
                    lines_content.append(f"<h3>{html_text.replace('<strong>', '').replace('</strong>', '')}</h3>")
                elif html_text.lower() == "key takeaway":
                    lines_content.append(f"<h3>Key Takeaway</h3>")
                else:
                    lines_content.append(f"<p>{html_text}</p>")
                
    elif isinstance(block, Table):
        if found_article:
            if in_list:
                lines_content.append("</ul>")
                in_list = False
            table_html = ["<table>"]
            for row_idx, row in enumerate(block.rows):
                table_html.append("  <tr>")
                for cell in row.cells:
                    cell_html = "<br/>".join([" ".join(get_html_from_paragraph(p)) for p in cell.paragraphs if p.text.strip()])
                    if row_idx == 0:
                        table_html.append(f"    <th><strong>{cell_html.replace('<strong>','').replace('</strong>','')}</strong></th>")
                    else:
                        table_html.append(f"    <td>{cell_html}</td>")
                table_html.append("  </tr>")
            table_html.append("</table>")
            lines_content.append("\n".join(table_html))

with open('article-1-1.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

start_tag = '<div class="article-content">'
end_tag = '</div>\n        </div>\n    </main>'

pre_html = template_html[:template_html.find(start_tag) + len(start_tag)]
post_html = template_html[template_html.find(end_tag):]

body_html = "\n".join(lines_content)

if '<div class="apply-it">' in body_html and '</div>' not in body_html.split('<div class="apply-it">')[-1]:
    body_html += '</div>'
    
page_title = "Article 1.7 - How Global Markets Affect the DSE | Amana Capital East Africa"
out_html = pre_html.replace('Article 1.1 - What Is an Economy and Why Does It Matter to You? | Amana Capital East Africa', page_title)

out_html += "\n" + body_html + "\n            " + post_html

filename = "article-1-7.html"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(out_html)
    
print("Successfully generated article 1.7!")
