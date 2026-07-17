import json
import re
import os

with open('articles_master.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for article in articles:
    title = article['title']
    content_html = '\n'.join(article['content'])
    
    match = re.search(r'Article (\d+)\.(\d+)', title)
    if match:
        mod_num = match.group(1)
        art_num = match.group(2)
        filename = f'article-{mod_num}-{art_num}.html'
        
        # Format the content
        clean_title = title.replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        content_html = content_html.replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        
        # Inject an h1 for the title
        inner_html = f"<h1>{clean_title}</h1>\n{content_html}"
        
        # Apply the apply-it styling block if applicable
        inner_html = re.sub(r'<p>(<strong>(?:Put It Into Practice|Action Step|APPLY IT NOW).*?)</p>', r'<div class="apply-it"><p>\1</p></div>', inner_html, flags=re.IGNORECASE)
        
        if os.path.exists(filename):
            with open(filename, 'r', encoding='windows-1252', errors='replace') as f:
                html_content = f.read()
                
            # Replace the contents of <div class="article-content">
            pattern = r'(<div class="article-content">)(.*?)(</div>\s*</div>\s*</main>)'
            
            # Check if pattern matches
            if re.search(pattern, html_content, flags=re.DOTALL):
                new_html = re.sub(pattern, r'\1\n' + inner_html.replace('\\', '\\\\') + r'\n\3', html_content, flags=re.DOTALL)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                print(f"Updated {filename}")
            else:
                print(f"Pattern not found in {filename}. Skipping.")
        else:
            print(f"File {filename} does not exist. Skipping.")
            
print("Done updating articles.")
