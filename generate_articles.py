import re

# Read extracted text
with open('extracted_education.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Define article start markers
markers = [
    ("Article 1.4", "Exchange Rates and Your Investments"),
    ("Article 1.5", "The Economic Cycle: When to Plant and When to Harvest"),
    ("Article 1.6", "How Government Spending and National Debt Affect Markets")
]

# Read template from article-1-1.html
with open('article-1-1.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

# Isolate the main content area to replace
# We'll replace everything between <div class="article-content"> and </div>\n        </div>\n    </main>
start_tag = '<div class="article-content">'
end_tag = '</div>\n        </div>\n    </main>'

pre_html = template_html[:template_html.find(start_tag) + len(start_tag)]
post_html = template_html[template_html.find(end_tag):]

for article_num, title in markers:
    print(f"Generating {article_num}...")
    
    # Find start and end in text
    start_idx = text.find(f"{article_num}")
    if start_idx == -1:
        print(f"Could not find {article_num}")
        continue
        
    next_article_match = re.search(r'Article \d\.\d', text[start_idx+20:])
    if next_article_match:
        end_idx = start_idx + 20 + next_article_match.start()
        content = text[start_idx:end_idx].strip()
    else:
        content = text[start_idx:].strip()
        
    lines = content.split('\n')
    
    # Process lines to HTML
    html_lines = []
    
    # First line is title
    html_lines.append(f'\n                <h1>{lines[0].strip()}</h1>')
    
    # Rest of the lines
    in_list = False
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('This document is for general') or line.startswith('This content is for informational'):
            html_lines.append(f'<div class="article-disclaimer"><p>{line}</p></div>')
        elif line.startswith('Further Reading:'):
            html_lines.append(f'<div class="further-reading"><p><strong>Further Reading</strong></p><p>{line.replace("Further Reading: ", "")}</p></div>')
        elif line.startswith('Put It Into Practice'):
            html_lines.append(f'<div class="apply-it"><p><strong>Put It Into Practice</strong></p>')
        elif line.startswith('Open today’s') and 'Put It Into Practice' in content:
            html_lines.append(f'<p>{line}</p></div>')
        elif re.match(r'^\d\.\s', line):
            html_lines.append(f'<h3>{line}</h3>')
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{line}</p>')
            
    if in_list:
        html_lines.append('</ul>')
        
    body_html = '\n'.join(html_lines)
    
    # Replace title in <title> tag
    page_title = f"{article_num} - {title} | Amana Capital East Africa"
    # The title is currently: <title>Article 1.1 - What Is an Economy and Why Does It Matter to You? | Amana Capital East Africa</title>
    out_html = pre_html.replace('Article 1.1 - What Is an Economy and Why Does It Matter to You? | Amana Capital East Africa', page_title)
    
    # Combine
    out_html += body_html + "\n            " + post_html
    
    # Write file
    filename = f"{article_num.replace(' ', '-').replace('.', '-').lower()}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(out_html)
        
print("Done!")
