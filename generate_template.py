import json
import re

# Read the original article 1.1 template
with open('old_article_template_utf8.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

# Replace the <title> tag
template_html = re.sub(r'<title>.*?</title>', r'<title>{page_title}</title>', template_html)

# Replace the h1 and everything inside <div class="article-content">
# We want to replace everything from <h1> to the end of the div
pattern = r'(<div class="article-content">).*?(</div>\s*</div>\s*</main>)'
template_html = re.sub(pattern, r'\1\n                <h1>{article_title}</h1>\n                {article_content}\n            \2', template_html, flags=re.DOTALL)

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
        
        clean_title = title.replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        page_title = f"{clean_title} | Amana Capital East Africa"
        
        # Style the apply-it blocks
        content_html = re.sub(r'<p>(<strong>(?:Put It Into Practice|Action Step|APPLY IT NOW).*?)</p>', r'<div class="apply-it"><p>\1</p></div>', content_html, flags=re.IGNORECASE)
        
        final_html = template_html.replace('{page_title}', page_title).replace('{article_title}', clean_title).replace('{article_content}', content_html)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Generated {filename}")

print("Done generating 37 articles using the original template.")
