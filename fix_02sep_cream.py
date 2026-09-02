import re

with open('dse-wrap-2026-09-02.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Apply the cream box to section 7
# Find the start of section 7
parts = re.split(r'(<h2.*?>7\..*?</h2>)', c, flags=re.DOTALL)
if len(parts) == 3:
    pre_sec7 = parts[0]
    sec7_header = parts[1]
    post_sec7 = parts[2]
    
    # We want to wrap from sec7_header to the end of the article content, which is before <div class="article-disclaimer">
    article_parts = post_sec7.split('<div class="article-disclaimer"', 1)
    if len(article_parts) == 2:
        sec7_content = article_parts[0]
        disclaimer = '<div class="article-disclaimer"' + article_parts[1]
        
        # Now wrap the sec7_header and sec7_content in a cream box
        new_sec7 = f'''<div class="dse-article-card" style="background: var(--cream); border: 2px solid var(--gold); border-radius: 8px;">
{sec7_header}{sec7_content}</div>
'''
        c = pre_sec7 + new_sec7 + disclaimer
        with open('dse-wrap-2026-09-02.html', 'w', encoding='utf-8') as f:
            f.write(c)
        print("Successfully applied cream box to section 7.")
    else:
        print("Could not find article disclaimer to terminate section 7.")
else:
    print("Could not split by section 7.")
