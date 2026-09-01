import re

with open('dse-wrap-2026-09-01.html', 'r', encoding='utf-8') as f:
    c = f.read()

def repl(m):
    content = m.group(1)
    content = re.sub(r'<h2.*?>', '<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem;">', content).replace('</h2>', '</h3>')
    # Remove the extra disclaimer at the bottom of the considerations block if mammoth added it
    content = re.sub(r'<p><em>For general informational.*?</em></p>', '', content, flags=re.DOTALL)
    
    return f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{content}\n</div>'

c = re.sub(r'(<h2.*?>7\. Considerations for a Multi-Year Framework</h2>.*?)(?=<div class="article-disclaimer")', repl, c, flags=re.DOTALL)

with open('dse-wrap-2026-09-01.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed considerations")
