import json
import re

with open('articles_master_v3.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Build a mapping of Article title -> URL
title_to_url = {}
for article in articles:
    title = article['title']
    match = re.search(r'Article (\d+)\.(\d+)\s*-\s*(.*)', title)
    if match:
        mod_num = match.group(1)
        art_num = match.group(2)
        base_title = match.group(3).strip()
        url = f'article-{mod_num}-{art_num}.html'
        
        clean_base = re.sub(r'<[^>]+>', '', base_title).replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        title_to_url[clean_base.lower()] = url
        
def replace_doc_link(match):
    link_html = match.group(1)
    link_text = re.sub(r'<[^>]+>', '', link_html).replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-').strip()
    
    matched_url = None
    for clean_base, url in title_to_url.items():
        if clean_base in link_text.lower() or link_text.lower() in clean_base:
            matched_url = url
            break
            
    if matched_url:
        return f'<a href="{matched_url}" class="article-crosslink">{link_html}</a>'
    else:
        return f'<span class="article-crosslink">{link_html}</span>'

with open('article-1-1.html', 'r', encoding='windows-1252', errors='replace') as f:
    template_html = f.read()

template_html = re.sub(r'<title>.*?</title>', r'<title>{page_title}</title>', template_html)

wow_factor_css = """
        .article-container { max-width: 800px; margin: 4rem auto; padding: 3rem; background: var(--white); border-radius: 12px; box-shadow: 0 10px 30px rgba(11,29,58,0.08), 0 1px 8px rgba(11,29,58,0.03); border-top: 5px solid var(--gold); }
        body { background-color: var(--cream); }
        .article-content { font-family: 'Inter', sans-serif; color: var(--navy); }
        .article-content h1 { color: var(--navy); margin-bottom: 0.5rem; font-size: 2.5rem; font-family: 'Merriweather', serif; font-weight: 700; line-height: 1.2; letter-spacing: -0.5px; }
        .article-content h2, .article-content h3, .article-content h4 { color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.2rem; font-family: 'Merriweather', serif; font-weight: 700; }
        .article-content p { line-height: 1.8; margin-bottom: 1.8rem; font-size: 1.15rem; color: var(--navy); }
        .article-content ul, .article-content ol { margin-bottom: 1.8rem; padding-left: 2rem; color: var(--navy); }
        .article-content li { margin-bottom: 0.8rem; line-height: 1.7; font-size: 1.15rem; color: var(--navy); }
        .article-content table { width: 100%; border-collapse: collapse; margin-bottom: 2rem; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(11,29,58,0.05); }
        .article-content th, .article-content td { border: 1px solid var(--stone); padding: 1rem; text-align: left; color: var(--navy); }
        .article-content th { background-color: var(--navy); color: var(--white); font-weight: 600; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1px; }
        .article-content tr:nth-child(even) { background-color: var(--cream); }
        .apply-it, .further-reading, .article-disclaimer { background-color: var(--stone); border: 1px solid var(--gold); padding: 2rem; margin: 3rem 0; border-radius: 8px; position: relative; }
        .apply-it p, .further-reading p { color: var(--navy); }
        .apply-it p:last-child, .further-reading p:last-child { margin-bottom: 0; }
        .apply-it p:first-child strong, .further-reading p:first-child strong { color: var(--gold); text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem; display: block; margin-bottom: 0.5rem; }
        .breadcrumb { margin-bottom: 3rem; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
        .breadcrumb a { color: var(--gold); text-decoration: none; display: inline-flex; align-items: center; transition: all 0.2s ease; }
        .breadcrumb a:hover { color: var(--navy); transform: translateX(-5px); }
        .article-crosslink { color: var(--gold); font-weight: 400; text-decoration: none; border-bottom: 2px solid var(--gold); transition: all 0.2s ease; }
        .article-crosslink:hover { background-color: transparent; border-bottom-color: var(--navy); color: var(--navy); }
        .article-disclaimer p { margin-bottom: 0; color: var(--navy); font-size: 0.9rem; line-height: 1.6; text-align: justify; }
"""

template_html = re.sub(r'<style>.*?</style>', f'<style>\n{wow_factor_css}\n    </style>', template_html, flags=re.DOTALL)

pattern = r'(<div class="article-content">).*?(</div>\s*</div>\s*</main>)'
template_html = re.sub(pattern, r'\1\n                <h1>{article_title}</h1>\n                {article_content}\n            \2', template_html, flags=re.DOTALL)

def clean_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip().lower()

for article in articles:
    title = article['title']
    
    # Process content items logically
    new_content = []
    current_box = None
    box_content = []
    
    def flush_box():
        if current_box and box_content:
            new_content.append(f'<div class="{current_box}">\n' + '\n'.join(box_content) + '\n</div>')
            box_content.clear()
    
    for item in article['content']:
        clean_text = clean_tags(item)
        
        # Check if item is a disclaimer
        if "this document is for general informational and educational purposes" in clean_text:
            flush_box()
            current_box = "article-disclaimer"
            box_content.append(item)
            flush_box()
            current_box = None
            continue
            
        # Check if item is Further Reading heading
        if "further reading" in clean_text:
            flush_box()
            current_box = "further-reading"
            box_content.append(item)
            continue
            
        # Check if item is Action Step / Apply it now heading
        if "put it into practice" in clean_text or "action step" in clean_text or "apply it now" in clean_text:
            if current_box != "further-reading": # Priority to further reading if it somehow triggers this
                flush_box()
                current_box = "apply-it"
                box_content.append(item)
                continue
                
        # If in a box, append to box content, otherwise append to normal content
        if current_box:
            box_content.append(item)
        else:
            new_content.append(item)
            
    flush_box() # Flush any remaining box
    
    content_html = '\n'.join(new_content)
    
    match = re.search(r'Article (\d+)\.(\d+)', title)
    if match:
        mod_num = match.group(1)
        art_num = match.group(2)
        filename = f'article-{mod_num}-{art_num}.html'
        
        clean_title = title.replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        page_title = f"{clean_title} | Amana Capital East Africa"
        
        # Replace the doc-links
        content_html = re.sub(r'<span class="doc-link">(.*?)</span>', replace_doc_link, content_html)
        
        final_html = template_html.replace('{page_title}', page_title).replace('{article_title}', clean_title).replace('{article_content}', content_html)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Generated {filename}")

print("Done generating 37 articles using V3 layout with robust box capturing logic.")
