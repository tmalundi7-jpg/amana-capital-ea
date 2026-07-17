import json
import re

with open('articles_master.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

new_links = {}
for article in articles:
    title = article['title']
    match = re.search(r'Article (\d+)\.(\d+)', title)
    if match:
        mod_num = match.group(1)
        art_num = match.group(2)
        filename = f'article-{mod_num}-{art_num}.html'
        clean_title = title.replace('\ufffd', '-').replace('\u2013', '-').replace('\u2014', '-')
        
        if mod_num not in new_links:
            new_links[mod_num] = []
        new_links[mod_num].append((int(art_num), f'<li><a href="/{filename.replace(".html", "")}" class="article-link">{clean_title}</a></li>'))

with open('education.html', 'r', encoding='utf-8') as f:
    edu_content = f.read()

for mod_num, links in new_links.items():
    pattern = f'(<!-- Module {mod_num} -->.*?<ul.*?>)(.*?)(</ul>)'
    match = re.search(pattern, edu_content, flags=re.DOTALL)
    
    if match:
        links.sort(key=lambda x: x[0])
        new_list_items = '\n                        '.join([l[1] for l in links])
        updated_list = '\n                        ' + new_list_items + '\n                    '
        edu_content = edu_content[:match.start(2)] + updated_list + edu_content[match.end(2):]
        print(f"Updated Module {mod_num} with {len(links)} links.")

with open('education.html', 'w', encoding='utf-8') as f:
    f.write(edu_content)
    
print("Done updating education.html")
