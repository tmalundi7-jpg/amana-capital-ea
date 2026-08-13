import re
import docx

# 1. Parse Daily Wrap DOCX
doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 20 July 2026.docx')

paragraphs = []
table_idx = 0

for block in doc.iter_inner_content():
    if isinstance(block, docx.text.paragraph.Paragraph):
        text = block.text.strip()
        if not text: continue
        
        # Replace weird quotes and spaces - DO NOT use replace('', '-')
        text = text.replace('?', "'").replace('?', "'").replace('?', "-").replace('\u202f', ' ').replace('\ufffd', "-")
        
        # Check if it's a heading
        if text.startswith('1.') or text.startswith('2.') or text.startswith('3.') or text.startswith('4.') or text.startswith('5.') or text.startswith('6.') or text.startswith('7.') or text.startswith('8.'):
            paragraphs.append(f'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">{text.replace("<", "&lt;").replace(">", "&gt;")}</h2>')
        elif "Daily DSE Wrap | Monday, 20th July 2026" in text or "CRDB Block Wave Subsides" in text:
            continue # We handle the title and subtitle separately
        elif text.startswith('This document is for general'):
             paragraphs.append(f'<div class="article-disclaimer" style="margin-top: 3rem; font-size: 0.85rem; color: #666; border-top: 1px solid var(--stone); padding-top: 1rem;"><p><em>{text}</em></p></div>')
        elif text.startswith('¹ DCB trades under a wider') or text.startswith('1 DCB trades under a wider'):
             paragraphs.append(f'<p style="font-size: 0.85rem; color: #666; margin-bottom: 1rem;">{text.replace("<", "&lt;").replace(">", "&gt;")}</p>')
        elif text.startswith('Gainers:') or text.startswith('Losers:'):
            html_text = text.replace("<", "&lt;").replace(">", "&gt;")
            html_text = html_text.replace('Gainers:', '<strong>Gainers:</strong>')
            html_text = html_text.replace('Losers:', '<strong>Losers:</strong>')
            paragraphs.append(f'<p>{html_text}</p>')
        else:
             html_text = text.replace("<", "&lt;").replace(">", "&gt;")
             
             # Format links
             links = [
                 'How a Trade Happens',
                 'Understanding Market Data',
                 'CRDB Bank – A Fundamental Walk-Through',
                 'CRDB Bank - A Fundamental Walk-Through'
             ]
             for l in links:
                 if 'CRDB Bank - A Fundamental Walk-Through' in l:
                     html_text = html_text.replace('CRDB Bank – A Fundamental Walk-Through', f'<a href="/education" class="gold-link">CRDB Bank – A Fundamental Walk-Through</a>')
                 html_text = html_text.replace(l, f'<a href="/education" class="gold-link">{l}</a>')
                 
             if html_text.startswith('Upper limit:') or html_text.startswith('Lower limit:') or html_text.startswith('The Bank of Tanzania’s monetary policy') or html_text.startswith('Government infrastructure spending') or html_text.startswith('The CRDB block trades appear') or html_text.startswith('VODA’s full-year results') or html_text.startswith('NMB’s ex-dividend date') or html_text.startswith('Pair the Daily Wrap') or html_text.startswith('Maintain a diversified') or html_text.startswith('Think in years') or html_text.startswith('Remember the risk') or html_text.startswith('The seller — almost') or html_text.startswith('The buyer — a local') or html_text.startswith('The Bank of Tanzania\'s monetary policy') or html_text.startswith('VODA\'s full-year results') or html_text.startswith('NMB\'s ex-dividend date') or html_text.startswith('The seller - almost') or html_text.startswith('The buyer - a local'):
                 if len(paragraphs) > 0 and paragraphs[-1].endswith('</ul>'):
                     paragraphs[-1] = paragraphs[-1].replace('</ul>', f'    <li>{html_text}</li>\n</ul>')
                 else:
                     paragraphs.append(f'<ul>\n    <li>{html_text}</li>\n</ul>')
             else:
                 paragraphs.append(f'<p>{html_text}</p>')
                 
    elif isinstance(block, docx.table.Table):
        table_html = ['<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">', '<table class="data-table" style="width: 100%; border-collapse: collapse;">']
        table_html.append('  <thead>')
        table_html.append('    <tr style="background-color: var(--navy); color: var(--white); text-align: left;">')
        
        for row_idx, row in enumerate(block.rows):
            if row_idx == 0:
                for cell in row.cells:
                    cell_text = cell.text.strip().replace("<", "&lt;").replace(">", "&gt;").replace('\u202f', ' ').replace('\ufffd', '-')
                    table_html.append(f'      <th style="padding: 1rem;">{cell_text}</th>')
                table_html.append('    </tr>')
                table_html.append('  </thead>')
                table_html.append('  <tbody>')
            else:
                bg_color = ' style="background-color: var(--cream);"' if row_idx % 2 == 0 else ''
                table_html.append(f'    <tr{bg_color}>')
                for col_idx, cell in enumerate(row.cells):
                    cell_text = cell.text.strip().replace("<", "&lt;").replace(">", "&gt;").replace('\u202f', ' ')
                    
                    # Fix unicode hyphens and dashes for styling
                    # Specifically, if the text has a hyphen, we leave it. If it has a unicode minus, we swap it for standard dash.
                    cell_text = cell_text.replace('–', '-').replace('—', '-')
                    if '?' in cell_text or '\ufffd' in cell_text:
                         cell_text = re.sub(r'[^0-9A-Za-z\.\,\+\-\% ]', '-', cell_text)
                    
                    # Formatting numbers and change colors
                    style = 'padding: 1rem;'
                    if col_idx == 0:
                        style += ' font-weight: 600;'
                    
                    if ('+' in cell_text and '%' in cell_text) or ('+' in cell_text and 'pts' in cell_text) or ('+' in cell_text and '1,934' in cell_text):
                        style += ' color: var(--gain);'
                    elif ('-' in cell_text and '%' in cell_text) or ('-' in cell_text and 'pts' in cell_text):
                        style += ' color: var(--loss);'
                    elif cell_text == '0.0%':
                        style += ' color: #666; font-weight: 600;'
                    
                    if 'color:' in style and 'font-weight: 600;' not in style and '%' in cell_text and len(cell_text) < 10:
                        # For the change column in tables 2 and 3 usually
                        style += ' font-weight: 600;'
                        
                    table_html.append(f'      <td style="{style}">{cell_text}</td>')
                table_html.append('    </tr>')
                
        table_html.append('  </tbody>')
        table_html.append('</table>')
        table_html.append('</div>')
        paragraphs.extend(table_html)
        table_idx += 1

content_html = "\n".join(paragraphs)

# Fix any leftover smart quotes and weird unicode from Word
content_html = content_html.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')

# 2. Use 17 July as template
with open('dse-wrap-2026-07-17.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace canonical URL
template = template.replace('dse-wrap-2026-07-17.html', 'dse-wrap-2026-07-20.html')

# Replace Title tags
template = template.replace('Friday, 17th July 2026', 'Monday, 20th July 2026')
template = template.replace('17th July 2026', '20th July 2026')
template = template.replace('Fourth CRDB Block Trade Seals Historic Handover as Foreign Selling Drops to a Year-Low', 'CRDB Block Wave Subsides as VODA Block Surprises and NMB Hits a New Peak')

# Find start and end of content to replace
start_marker = '<p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 2rem; font-weight: 600;">CRDB Block Wave Subsides as VODA Block Surprises and NMB Hits a New Peak</p>'
if start_marker not in template:
    start_marker = '<p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 2rem; font-weight: 600;">Fourth CRDB Block Trade Seals Historic Handover as Foreign Selling Drops to a Year-Low</p>'
end_marker = '</div>\n        </div>\n    </main>'

pre_html = template[:template.find(start_marker) + len(start_marker)]
post_html = template[template.find(end_marker):]

out_html = pre_html + "\n                <hr style=\"border: none; border-top: 1px solid var(--stone); margin-bottom: 2rem;\">\n                " + content_html + "\n                \n            " + post_html

with open('dse-wrap-2026-07-20.html', 'w', encoding='utf-8') as f:
    f.write(out_html)

print("Generated absolutely clean dse-wrap-2026-07-20.html successfully.")
