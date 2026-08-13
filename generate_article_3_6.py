import docx
import re
import os

filepath = r"C:\Users\tmalu\OneDrive\Documents\To update investor education page of Amana Capital EA website.docx"
doc = docx.Document(filepath)

target_article = "Article 3.6"
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
is_put_it_into_practice = False

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        text = block.text.strip()
        
        match = re.match(r'^(Article 3\.6)\s*[-–—]\s*(.*)', text)
        if match:
            found_article = True
            title = match.group(2)
            lines_content.append(f"<h1>Article 3.6 - {title}</h1>")
            continue
            
        if found_article and (re.match(r'^Article \d\.\d', text) or "Article 4." in text):
            if in_list:
                lines_content.append("</ul>")
                in_list = False
            if is_put_it_into_practice:
                 lines_content.append("</div>")
                 is_put_it_into_practice = False
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
                    lines_content.append(f"<p><em>{html_text}</em></p>")
                elif html_text.startswith("This document is for general") or "This content is for informational" in html_text:
                    if is_put_it_into_practice:
                        lines_content.append("</div>")
                        is_put_it_into_practice = False
                    # Make sure the disclaimer is identical to the bottom footer text.
                    disclaimer_text = "This document is for general informational and educational purposes only. Nothing contained herein constitutes financial, investment, legal, or tax advice and should not be relied upon as such. Any investment decision you make is solely your own responsibility. The value of investments and the income from them can go down as well as up, and you may not get back the amount originally invested. Past performance is not a reliable indicator of future results. Capital is at risk, and you may incur losses — including the total loss of your invested capital — which you alone will bear. Amana Capital East Africa Limited is a registered investment advisory and fund management firm under the Capital Markets and Securities Authority (CMSA), Tanzania. Licence number: [pending]. Our registration does not imply that CMSA approves or endorses the contents of this material."
                    lines_content.append(f'<div class="article-disclaimer">\n<p><em>{disclaimer_text}</em></p>\n</div>')
                elif "Further Reading" in html_text:
                    if is_put_it_into_practice:
                        lines_content.append("</div>")
                        is_put_it_into_practice = False
                    if html_text == "Further Reading":
                        continue
                    
                    # We only expect a paragraph under Further Reading, so we don't handle a link here if there's none in docx,
                    # but we will manually fix any link later.
                    inner_text = html_text.replace("Further Reading: ", "").replace("<strong>Further Reading</strong>", "").strip()
                    lines_content.append(f'<div class="further-reading">\n<p><strong>Further Reading</strong></p>\n<p>{inner_text}</p>\n</div>')
                elif "Put It Into Practice" in html_text:
                    is_put_it_into_practice = True
                    lines_content.append(f'<div class="apply-it">\n<p><strong>Put It Into Practice</strong></p>')
                elif re.match(r'^<strong>\d\.\s', html_text) or re.match(r'^\d\.\s', html_text) or html_text == "Key terms you need to know" or html_text == "What is a bond?":
                    # Headings logic. If no number is present we still want some items to be h3s.
                    if is_put_it_into_practice:
                        lines_content.append("</div>")
                        is_put_it_into_practice = False
                    lines_content.append(f"<h3>{html_text.replace('<strong>', '').replace('</strong>', '')}</h3>")
                elif html_text.lower() == "key takeaway":
                    if is_put_it_into_practice:
                        lines_content.append("</div>")
                        is_put_it_into_practice = False
                    lines_content.append(f"<h3>Key Takeaway</h3>")
                elif html_text.endswith(":") and len(html_text) < 70 and "By Amana" not in html_text:
                     # Looks like a heading
                     if is_put_it_into_practice:
                        lines_content.append("</div>")
                        is_put_it_into_practice = False
                     lines_content.append(f"<h3>{html_text.replace('<strong>', '').replace('</strong>', '')}</h3>")
                else:
                    # In docx some paragraphs have bold prefixes like "Face value: "
                    if html_text.startswith("<strong>") and "</strong>:" in html_text:
                        pass # Valid as a paragraph
                    lines_content.append(f"<p>{html_text}</p>")
                
    elif isinstance(block, Table):
        if found_article:
            if in_list:
                lines_content.append("</ul>")
                in_list = False
            if is_put_it_into_practice:
                lines_content.append("</div>")
                is_put_it_into_practice = False
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

with open('article-1-7.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

start_tag = '<div class="article-content">'
end_tag = '</div>\n        </div>\n    </main>'

pre_html = template_html[:template_html.find(start_tag) + len(start_tag)]
post_html = template_html[template_html.find(end_tag):]

body_html = "\n".join(lines_content)

if is_put_it_into_practice:
    body_html += "\n</div>"
    
page_title = "Article 3.6 - How to Invest in Government and Corporate Bonds on the DSE | Amana Capital East Africa"
out_html = pre_html.replace('Article 1.7 - How Global Markets Affect the DSE | Amana Capital East Africa', page_title)

# Update breadcrumb to go back to education hub, not change it.
out_html += "\n" + body_html + "\n            " + post_html

filename = "article-3-6.html"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(out_html)
    
print("Successfully generated article 3.6!")
