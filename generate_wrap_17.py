import re
import docx

# 1. Parse Daily Wrap DOCX
doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 17 July 2026.docx')

paragraphs = []
for block in doc.iter_inner_content():
    if isinstance(block, docx.text.paragraph.Paragraph):
        text = block.text.strip()
        if not text: continue
        
        # Check if it's a bold heading
        bold_len = sum(len(run.text) for run in block.runs if run.bold)
        if bold_len > len(text) * 0.5 and (text[0].isdigit() or text.startswith('In Focus') or text.startswith('Strategic')):
            paragraphs.append(f'<h3 style="color: var(--navy); margin-top: 2rem;">{text.replace("<", "&lt;").replace(">", "&gt;")}</h3>')
        elif text == "Daily DSE Wrap | Friday, 17th July 2026" or "Fourth CRDB Block Trade" in text:
            continue # We handle the title and subtitle separately
        elif text.startswith('This document is for general'):
             paragraphs.append(f'<div class="article-disclaimer" style="margin-top: 3rem; font-size: 0.85rem; color: #666; border-top: 1px solid var(--stone); padding-top: 1rem;"><p><em>{text}</em></p></div>')
        else:
             html_text = text.replace("<", "&lt;").replace(">", "&gt;")
             paragraphs.append(f'<p>{html_text}</p>')
             
    elif isinstance(block, docx.table.Table):
        table_html = ['<div style="overflow-x: auto; margin-bottom: 2rem;">', '<table class="data-table">']
        for row_idx, row in enumerate(block.rows):
            table_html.append('  <tr>')
            for cell in row.cells:
                cell_text = cell.text.strip().replace("<", "&lt;").replace(">", "&gt;")
                if row_idx == 0:
                    table_html.append(f'    <th>{cell_text}</th>')
                else:
                    table_html.append(f'    <td>{cell_text}</td>')
            table_html.append('  </tr>')
        table_html.append('</table>')
        table_html.append('</div>')
        paragraphs.extend(table_html)

content_html = "\n".join(paragraphs)

# 2. Use 16 July as template
with open('dse-wrap-2026-07-16.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace canonical URL
template = template.replace('dse-wrap-2026-07-16.html', 'dse-wrap-2026-07-17.html')

# Replace Title tags
template = template.replace('Thursday, 16th July 2026', 'Friday, 17th July 2026')
template = template.replace('16th July 2026', '17th July 2026')
template = template.replace('Third CRDB Block Seals the Handover as Foreign Buyers Begin to Return', 'Fourth CRDB Block Trade Seals Historic Handover as Foreign Selling Drops to a Year-Low')

# Find start and end of content to replace
start_marker = '<p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 2rem; font-weight: 600;">Fourth CRDB Block Trade Seals Historic Handover as Foreign Selling Drops to a Year-Low</p>'
end_marker = '</div>\n        </div>\n    </main>'

pre_html = template[:template.find(start_marker) + len(start_marker)]
post_html = template[template.find(end_marker):]

out_html = pre_html + "\n                <hr style=\"border: none; border-top: 1px solid var(--stone); margin-bottom: 2rem;\">\n                " + content_html + "\n                \n            " + post_html

with open('dse-wrap-2026-07-17.html', 'w', encoding='utf-8') as f:
    f.write(out_html)

print("Generated dse-wrap-2026-07-17.html successfully.")
