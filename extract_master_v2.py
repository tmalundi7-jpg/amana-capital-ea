import docx
import json
import re
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("Invalid parent type")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def parse_para(para):
    html_runs = []
    
    # Check if this paragraph is part of a list
    is_list = False
    if para.style.name.startswith('List') or para._element.pPr is not None and para._element.pPr.numPr is not None:
        is_list = True

    for run in para.runs:
        run_text = run.text.replace('<', '&lt;').replace('>', '&gt;')
        if not run_text:
            continue
            
        # Handle bold
        if run.bold:
            run_text = f"<strong>{run_text}</strong>"
            
        # Handle font colors
        if run.font.color and run.font.color.rgb:
            hex_color = str(run.font.color.rgb)
            if hex_color != '000000' and hex_color != 'None':
                run_text = f'<span style="color: #{hex_color};">{run_text}</span>'
        elif run.font.highlight_color:
            run_text = f'<span style="background-color: yellow; color: black;">{run_text}</span>'
            
        html_runs.append(run_text)
        
    final_html = "".join(html_runs)
    if not final_html.strip():
        return ""
        
    if is_list:
        return f"<ul><li>{final_html}</li></ul>"
    else:
        return f"<p>{final_html}</p>"

doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\investor education.docx')

articles = []
current_article = None

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        text = block.text.strip()
        if not text:
            continue
        
        match = re.match(r'^(?:Article\s+)?(\d+\.\d+)\s*[-–—]?\s*(.*)', text)
        if match:
            if current_article:
                articles.append(current_article)
            title = f"Article {match.group(1)} - {match.group(2)}"
            current_article = {'title': title, 'content': []}
        elif current_article is not None:
            html = parse_para(block)
            if html:
                # Merge consecutive <ul><li> elements
                if html.startswith('<ul>') and current_article['content'] and current_article['content'][-1].endswith('</ul>'):
                    prev = current_article['content'].pop()
                    # Remove the closing </ul> of previous, and opening <ul> of current
                    merged = prev[:-5] + html[4:]
                    current_article['content'].append(merged)
                else:
                    current_article['content'].append(html)
                    
    elif isinstance(block, Table):
        if current_article is not None:
            html = "<table>\n"
            for i, row in enumerate(block.rows):
                html += "  <tr>\n"
                for cell in row.cells:
                    cell_html = ""
                    for p in cell.paragraphs:
                        parsed = parse_para(p)
                        if parsed:
                            # Strip the outer <p> for tables to make it cleaner, if desired.
                            # But keeping it is fine. Let's strip <p> and </p> if it's the only thing.
                            if parsed.startswith('<p>') and parsed.endswith('</p>'):
                                parsed = parsed[3:-4]
                            cell_html += parsed + "<br>"
                    
                    if cell_html.endswith('<br>'):
                        cell_html = cell_html[:-4]
                        
                    tag = "th" if i == 0 else "td"
                    html += f"    <{tag}>{cell_html.strip()}</{tag}>\n"
                html += "  </tr>\n"
            html += "</table>"
            current_article['content'].append(html)

if current_article:
    articles.append(current_article)

with open('articles_master_v2.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2)

print(f"Extracted {len(articles)} articles.")
