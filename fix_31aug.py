import re

with open('dse-wrap-2026-08-31.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix mangled characters
c = c.replace('?"', '&mdash;')
c = c.replace('?"', '&mdash;')
c = c.replace('Ahas', ' has')
c = c.replace('Acontinues', ' continues')
c = c.replace('Aremains', ' remains')
c = c.replace('Aare', ' are')
c = c.replace('AIf', ' If')
c = c.replace('AThey', ' They')
c = c.replace('ANMB', ' NMB')
c = c.replace('AThe', ' The')
c = c.replace('ADaily', ' Daily')
c = c.replace('ANever', ' Never')
c = c.replace('readA<a', 'read <a')
c = c.replace('</a>AandA<a', '</a> and <a')
c = c.replace('</a>Aand<a', '</a> and <a')

# Apply Considerations styling
split_marker = '<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h2>'
if split_marker in c:
    parts = c.split(split_marker)
    before_7 = parts[0]
    after_7 = parts[1]
    
    # Remove extra disclaimer inside the body
    after_7 = re.sub(r'<p><em>For general informational.*?</em></p>\s*(?=<div class="article-disclaimer")', '', after_7, flags=re.DOTALL)
    
    if '<div class="article-disclaimer"' in after_7:
        sub_parts = after_7.split('<div class="article-disclaimer"')
        considerations_text = sub_parts[0]
        disclaimer_html = '<div class="article-disclaimer"' + sub_parts[1]
        
        new_header = '<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h3>'
        wrapped_7 = f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{new_header}{considerations_text}\n</div>\n{disclaimer_html}'
        
        c = before_7 + wrapped_7
        print("Successfully wrapped section 7!")
    else:
        print("Could not find article-disclaimer in after_7")
else:
    print("Could not find section 7 marker!")

with open('dse-wrap-2026-08-31.html', 'w', encoding='utf-8') as f:
    f.write(c)
