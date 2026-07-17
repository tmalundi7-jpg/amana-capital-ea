import docx
import re

filepath = r"C:\Users\tmalu\OneDrive\Documents\investor education.docx"
doc = docx.Document(filepath)

target_articles = ["Article 1.4", "Article 1.5", "Article 1.6"]
current_article = None
articles_content = { "Article 1.4": [], "Article 1.5": [], "Article 1.6": [] }

from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P): yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl): yield Table(child, parent)

def get_html_from_paragraph(p):
    html = ""
    raw_text = p.text.strip()
    if not raw_text: return ""
    
    # If the paragraph is very long and mostly bold, it's a mistake by the doc author
    # We should only keep bold if it's a small portion
    bold_len = sum(len(run.text) for run in p.runs if run.bold)
    keep_bold = bold_len < len(raw_text) * 0.5
    
    for run in p.runs:
        text = run.text.replace("<", "&lt;").replace(">", "&gt;")
        if not text: continue
        if run.bold and keep_bold:
            text = f"<strong>{text}</strong>"
        if run.italic:
            text = f"<em>{text}</em>"
        html += text
    return html.strip()

in_list = False

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        text = block.text.strip()
        
        match = re.match(r'^(Article 1\.[456])\s*[-–—]\s*(.*)', text)
        if match:
            if in_list and current_article:
                articles_content[current_article].append("</ul>")
                in_list = False
            current_article = match.group(1)
            title = match.group(2)
            articles_content[current_article].append(f"<h1>Article {current_article[-3:]} - {title}</h1>")
            continue
            
        if text.startswith("Article 2.1"):
            if in_list and current_article:
                articles_content[current_article].append("</ul>")
                in_list = False
            break
            
        if current_article:
            html_text = get_html_from_paragraph(block)
            if not html_text: continue
            
            # Handle bullet points (if it starts with a dash or bullet char)
            # Some docx bullets might not have a text bullet, but let's check for standard text bullets
            is_bullet = False
            if html_text.startswith("- ") or html_text.startswith("• "):
                is_bullet = True
                html_text = html_text[2:].strip()
                
            if is_bullet:
                if not in_list:
                    articles_content[current_article].append("<ul>")
                    in_list = True
                articles_content[current_article].append(f"<li>{html_text}</li>")
                continue
            else:
                if in_list:
                    articles_content[current_article].append("</ul>")
                    in_list = False

            if html_text.startswith("By Amana Capital"):
                articles_content[current_article].append(f"<p><em><strong>{html_text}</strong></em></p>")
            elif html_text.startswith("This document is for general") or "This content is for informational" in html_text:
                articles_content[current_article].append(f'<div class="article-disclaimer"><p>{html_text}</p></div>')
            elif "Further Reading" in html_text:
                articles_content[current_article].append(f'<div class="further-reading"><p><strong>Further Reading</strong></p><p>{html_text.replace("Further Reading: ", "").replace("<strong>Further Reading</strong>", "")}</p></div>')
            elif "Put It Into Practice" in html_text:
                articles_content[current_article].append(f'<div class="apply-it"><p><strong>Put It Into Practice</strong></p>')
            elif "Open today" in html_text or ("daily DSE wrap" in html_text.lower() and "practice" in "".join(articles_content[current_article][-2:]).lower()):
                 articles_content[current_article].append(f'<p>{html_text}</p></div>')
            elif re.match(r'^<strong>\d\.\s', html_text) or re.match(r'^\d\.\s', html_text):
                articles_content[current_article].append(f"<h3>{html_text.replace('<strong>', '').replace('</strong>', '')}</h3>")
            elif html_text.lower() == "key takeaway":
                articles_content[current_article].append(f"<h3>Key Takeaway</h3>")
            else:
                articles_content[current_article].append(f"<p>{html_text}</p>")
                
    elif isinstance(block, Table):
        if current_article:
            if in_list:
                articles_content[current_article].append("</ul>")
                in_list = False
            table_html = ["<table>"]
            for row_idx, row in enumerate(block.rows):
                table_html.append("  <tr>")
                for cell in row.cells:
                    cell_html = "<br/>".join([get_html_from_paragraph(p) for p in cell.paragraphs if p.text.strip()])
                    if row_idx == 0:
                        table_html.append(f"    <th><strong>{cell_html.replace('<strong>','').replace('</strong>','')}</strong></th>")
                    else:
                        table_html.append(f"    <td>{cell_html}</td>")
                table_html.append("  </tr>")
            table_html.append("</table>")
            articles_content[current_article].append("\n".join(table_html))

with open('article-1-1.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

start_tag = '<div class="article-content">'
end_tag = '</div>\n        </div>\n    </main>'

pre_html = template_html[:template_html.find(start_tag) + len(start_tag)]
post_html = template_html[template_html.find(end_tag):]

titles = {
    "Article 1.4": "Article 1.4 - Exchange Rates and Your Investments",
    "Article 1.5": "Article 1.5 - The Economic Cycle: When to Plant and When to Harvest",
    "Article 1.6": "Article 1.6 - How Government Spending and National Debt Affect Markets"
}

for article_num, lines in articles_content.items():
    if not lines: continue
    
    body_html = "\n".join(lines)
    
    if '<div class="apply-it">' in body_html and '</div>' not in body_html.split('<div class="apply-it">')[-1]:
        body_html += '</div>'
        
    page_title = f"{titles[article_num]} | Amana Capital East Africa"
    out_html = pre_html.replace('Article 1.1 - What Is an Economy and Why Does It Matter to You? | Amana Capital East Africa', page_title)
    
    out_html += "\n" + body_html + "\n            " + post_html
    
    filename = f"{article_num.replace(' ', '-').replace('.', '-').lower()}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(out_html)
        
print("Successfully regenerated all 3 articles!")
