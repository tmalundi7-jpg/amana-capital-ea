import docx
import json
import re

doc = docx.Document(r'C:\Users\tmalu\OneDrive\Documents\investor education.docx')

articles = []
current_article = None

for para in doc.paragraphs:
    text = para.text.strip()
    if not text: continue
    
    match = re.match(r'^(?:Article\s+)?(\d+\.\d+)\s*[-–—]?\s*(.*)', text)
    if match:
        if current_article:
            articles.append(current_article)
        title = f"Article {match.group(1)} - {match.group(2)}"
        current_article = {'title': title, 'content': []}
    elif current_article is not None:
        html_runs = []
        for run in para.runs:
            run_text = run.text.replace('<', '&lt;').replace('>', '&gt;')
            if not run_text.strip() and not run_text.isspace():
                html_runs.append(run_text)
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
                # Approximate highlight as background color or gold text
                run_text = f'<span style="background-color: yellow; color: black;">{run_text}</span>'
                
            html_runs.append(run_text)
            
        final_html = "".join(html_runs)
        if final_html.strip():
            current_article['content'].append(f"<p>{final_html}</p>")

if current_article:
    articles.append(current_article)

with open('articles_master.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2)

print(f"Extracted {len(articles)} articles.")
