import re
from docx import Document

# 1. Read the DOCX
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')

paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

tables = []
for t in doc.tables[:4]:
    table_data = []
    for row in t.rows:
        table_data.append([cell.text.strip().replace('\n', ' ') for cell in row.cells])
    tables.append(table_data)

html_parts = []

def wrap_strong(text):
    return text.replace('HIGH', '<strong>HIGH</strong>').replace('AFRIPRISE', '<strong>AFRIPRISE</strong>').replace('VODA', '<strong>VODA</strong>').replace('CRDB', '<strong>CRDB</strong>').replace('NMB', '<strong>NMB</strong>').replace('PAL', '<strong>PAL</strong>').replace('DCB', '<strong>DCB</strong>')

i = 1
while i < len(paragraphs) and '1. Market Snapshot' not in paragraphs[i]:
    if i == 1:
        html_parts.append(f'<p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{paragraphs[i]}</p>\n</div>\n')
    else:
        html_parts.append(f'<p>{paragraphs[i]}</p>')
    i += 1

if i < len(paragraphs):
    html_parts.append(f'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">{paragraphs[i]}</h2>')
    i += 1
    
    t0 = tables[0]
    html_parts.append('<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">')
    html_parts.append('<table class="data-table" style="width: 100%; border-collapse: collapse;">')
    html_parts.append('<thead><tr style="background-color: var(--navy); color: var(--white); text-align: left;">')
    for th in t0[0]: html_parts.append(f'<th style="padding: 1rem;">{th}</th>')
    html_parts.append('</tr></thead><tbody>')
    for r_idx, row in enumerate(t0[1:]):
        bg = 'background-color: var(--cream);' if r_idx % 2 == 1 else ''
        html_parts.append(f'<tr style="{bg}">')
        html_parts.append(f'<td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">{row[0]}</strong></td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[1]}</td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[2]}</td>')
        
        change_text = row[3]
        if '+' in change_text:
            change_style = 'color: var(--gain); font-weight: 600;'
        elif '-' in change_text or '' in change_text or '' in change_text:
            change_text = change_text.replace('', '&minus;')
            change_style = 'color: var(--loss); font-weight: 600;'
        else:
            change_style = 'font-weight: 600;'
        html_parts.append(f'<td style="padding: 1rem; {change_style}">{change_text}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table></div>')

while i < len(paragraphs) and '2. Top Movers' not in paragraphs[i]:
    html_parts.append(f'<p>{wrap_strong(paragraphs[i])}</p>')
    i += 1

if i < len(paragraphs):
    html_parts.append(f'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">{paragraphs[i]}</h2>')
    i += 1
    
    t1 = tables[1]
    html_parts.append('<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">')
    html_parts.append('<table class="data-table" style="width: 100%; border-collapse: collapse;">')
    html_parts.append('<thead><tr style="background-color: var(--navy); color: var(--white); text-align: left;">')
    for th in t1[0]: html_parts.append(f'<th style="padding: 1rem;">{th}</th>')
    html_parts.append('</tr></thead><tbody>')
    for r_idx, row in enumerate(t1[1:]):
        bg = 'background-color: var(--cream);' if r_idx % 2 == 1 else ''
        html_parts.append(f'<tr style="{bg}">')
        html_parts.append(f'<td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">{row[0]}</strong></td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[1]}</td>')
        
        change_text = row[2]
        if '+' in change_text:
            change_style = 'color: var(--gain); font-weight: 600;'
        elif '-' in change_text or '' in change_text or '' in change_text:
            change_text = change_text.replace('', '&minus;')
            change_style = 'color: var(--loss); font-weight: 600;'
        else:
            change_style = ''
        html_parts.append(f'<td style="padding: 1rem; {change_style}">{change_text}</td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[3]}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table></div>')

while i < len(paragraphs) and '3. In Focus' not in paragraphs[i]:
    if 'Gainers:' in paragraphs[i] or 'Losers:' in paragraphs[i]:
        text = paragraphs[i].replace('', '&minus;')
        html_parts.append(f'<p>{text}</p>')
    else:
        text = wrap_strong(paragraphs[i])
        html_parts.append(f'<p>{text}</p>')
    i += 1

if i < len(paragraphs):
    html_parts.append(f'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">{paragraphs[i]}</h2>')
    i += 1

    html_parts.append(f'<p>{paragraphs[i]}</p>')
    i += 1

    t2 = tables[2]
    html_parts.append('<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">')
    html_parts.append('<table class="data-table" style="width: 100%; border-collapse: collapse;">')
    html_parts.append('<thead><tr style="background-color: var(--navy); color: var(--white); text-align: left;">')
    for th in t2[0]: html_parts.append(f'<th style="padding: 1rem;">{th}</th>')
    html_parts.append('</tr></thead><tbody>')
    for r_idx, row in enumerate(t2[1:]):
        bg = 'background-color: var(--cream);' if r_idx % 2 == 1 else ''
        html_parts.append(f'<tr style="{bg}">')
        html_parts.append(f'<td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">{row[0]}</strong></td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[1]}</td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[2]}</td>')
        
        ratio = row[3]
        if float(ratio.replace('x','')) > 1:
            ratio_style = 'color: var(--gain); font-weight: 600;'
        else:
            ratio_style = 'color: var(--loss); font-weight: 600;'
            
        html_parts.append(f'<td style="padding: 1rem; {ratio_style}">{ratio}</td>')
        html_parts.append(f'<td style="padding: 1rem;">{row[4]}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table></div>')

while i < len(paragraphs) and 'For the daily price band' not in paragraphs[i]:
    if 'What does this mean' in paragraphs[i]:
        html_parts.append(f'<p><strong>{paragraphs[i]}</strong></p>')
    elif 'pay attention to the order book' in paragraphs[i]:
        html_parts.append(f'<p>The lesson is simple: <strong>pay attention to the order book, not just the price.</strong> A stock that falls on heavy volume with a balanced book may be near a bottom. A stock that falls with an offer-heavy book may have further to go. A stock that rises with a bid-heavy book may have further to run.</p>')
    else:
        html_parts.append(f'<p>{wrap_strong(paragraphs[i])}</p>')
    i += 1

html_parts.append('<div style="background-color: rgba(200, 150, 46, 0.05); border-left: 4px solid var(--gold); padding: 1.5rem; margin: 2rem 0; border-radius: 0 8px 8px 0;">')
html_parts.append('<h3 style="color: var(--navy); margin-top: 0; font-family: var(--heading-font); margin-bottom: 1rem;">Understanding Price Bands</h3>')

if i < len(paragraphs):
    html_parts.append(f'<p style="margin-bottom: 1rem;">{paragraphs[i]}</p>')
    i += 1
    
    html_parts.append('<ul style="margin-bottom: 1rem; color: var(--navy);">')
    html_parts.append(f'<li><strong>Upper limit:</strong> {paragraphs[i].replace("Upper limit:", "").replace("", "&times;")}</li>')
    i += 1
    html_parts.append(f'<li><strong>Lower limit:</strong> {paragraphs[i].replace("Lower limit:", "").replace("", "&times;")}</li>')
    i += 1
    html_parts.append('</ul>')
    
    html_parts.append(f'<p style="margin-bottom: 1rem;">{paragraphs[i]}</p>')
    i += 1

    t3 = tables[3]
    html_parts.append('<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">')
    html_parts.append('<table class="data-table" style="width: 100%; border-collapse: collapse; background-color: #fff;">')
    html_parts.append('<thead><tr style="background-color: var(--navy); color: var(--white); text-align: left;">')
    for th in t3[0]: html_parts.append(f'<th style="padding: 0.75rem;">{th}</th>')
    html_parts.append('</tr></thead><tbody>')
    for r_idx, row in enumerate(t3[1:]):
        bg = 'background-color: var(--cream);' if r_idx % 2 == 1 else ''
        html_parts.append(f'<tr style="{bg}">')
        html_parts.append(f'<td style="padding: 0.75rem; font-weight: 600;">{row[0].replace("", "&lowast;")}</td>')
        html_parts.append(f'<td style="padding: 0.75rem;">{row[1]}</td>')
        html_parts.append(f'<td style="padding: 0.75rem;">{row[2]}</td>')
        html_parts.append(f'<td style="padding: 0.75rem;">{row[3]}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table></div>')

while i < len(paragraphs):
    if 'DCB and MCB trade' in paragraphs[i]:
        html_parts.append(f'<p style="margin-bottom: 1rem; font-size: 0.9rem;"><em>{paragraphs[i].replace("", "&lowast;")}</em></p>')
    else:
        html_parts.append(f'<p style="margin-bottom: 0;">{paragraphs[i]}</p>')
    i += 1

html_parts.append('</div>')

new_article_body = '\n'.join(html_parts)

# Now read dse-wrap-2026-09-17.html completely
with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    content_17 = f.read()

# Replace the title and headers
content_17 = content_17.replace('17th September 2026', '18th September 2026')
content_17 = content_17.replace('Thursday, 18th', 'Friday, 18th') 
content_17 = content_17.replace('Thursday, 17th', 'Friday, 18th')
content_17 = content_17.replace('17 Sep 2026', '18 Sep 2026')
content_17 = content_17.replace('dse-wrap-2026-09-17.html', 'dse-wrap-2026-09-18.html')
content_17 = content_17.replace('Amana-DSE-Wrap-17-Sept.pdf', 'Amana-DSE-Wrap-18-Sept.pdf')

# We know that in 17th, the body starts after </h1> and ends before <div class="article-disclaimer"
match = re.search(r'(</h1>)(.*?)(<div class="article-disclaimer")', content_17, re.DOTALL)
if match:
    full_html = content_17[:match.start(2)] + '\n' + new_article_body + '\n' + content_17[match.end(2):]
    with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Perfect rebuild complete!")
else:
    print("Could not match the structure in 17!")

