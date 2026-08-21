import re
import os

files_to_fix = ['dse-wrap-2026-08-19.html', 'dse-wrap-2026-08-20.html', 'dse-wrap-2026-08-21.html']

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the H2 for considerations and everything until the disclaimer
    pattern = re.compile(r'(<h2[^>]*>7\.\s*Considerations for a Multi-Year Framework</h2>\s*<p>.*?</p>)\s*(<div class="article-disclaimer")', re.DOTALL)
    
    def replacer(match):
        inner_content = match.group(1).replace('<h2', '<h3').replace('</h2>', '</h3>')
        # Adjust margin of H3
        inner_content = re.sub(r'<h3[^>]*>', '<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem;">', inner_content)
        # Adjust p margin
        inner_content = re.sub(r'<p>', '<p style="margin-bottom: 0;">', inner_content)
        # Add the gold side-box wrapper
        gold_box = f'''<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">
{inner_content}
</div>
'''
        return gold_box + match.group(2)
        
    new_content = pattern.sub(replacer, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed Gold Box in {file_path}')
    else:
        print(f'No change for {file_path}')
