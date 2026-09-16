import re
import json

with open('extracted_data.json', 'r', encoding='utf-8') as f:
    wrap_data = json.load(f)

text = wrap_data['text']

# Basic formatting: convert text paragraphs to HTML <p> or <h2> based on starting numbers or content
body_html = ''
for p in text:
    if p.startswith('Daily DSE Wrap |'):
        continue
    if p.startswith('Based on Wednesday\'s closing prices') or p.startswith('Before placing any order') or p.startswith('For a complete guide'):
        body_html += f'<p>{p}</p>\n'
    elif p.startswith('1. ') or p.startswith('2. ') or p.startswith('3. ') or p.startswith('4. ') or p.startswith('5. ') or p.startswith('6. '):
        body_html += f'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">{p}</h2>\n'
    elif p.startswith('7. '):
        body_html += f'''<div class="" style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">
<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">{p}</h3>
'''
    elif p.startswith('For general informational'):
        body_html += f'''</div>

<div class="article-disclaimer" style="margin-top: 3rem; font-size: 0.85rem; color: #666; border-top: 1px solid var(--stone); padding-top: 1rem;">
<p><em>{p}</em></p>
</div>'''
    elif p.startswith('Wednesday\'s session'):
        body_html += f'<p>{p}</p>\n'
    else:
        # Just simple paragraphs for now, we don't have bold markdown in raw extracted text
        body_html += f'<p>{p}</p>\n'

with open('dse-wrap-2026-09-07.html', 'r', encoding='utf-8') as f:
    tmpl = f.read()

# Replace dates
tmpl = re.sub(r'07 Sep 2026', '09 Sep 2026', tmpl)
tmpl = re.sub(r'7 September 2026', '9 September 2026', tmpl)
tmpl = re.sub(r'Monday, 7th September 2026', 'Wednesday, 9th September 2026', tmpl)

# Replace the inner body
tmpl = re.sub(r'(<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">1\..*?)<div class="article-disclaimer"', body_html + '\n<div class="article-disclaimer"', tmpl, flags=re.DOTALL)

with open('dse-wrap-2026-09-09.html', 'w', encoding='utf-8') as f:
    f.write(tmpl)

print('Created dse-wrap-2026-09-09.html')
