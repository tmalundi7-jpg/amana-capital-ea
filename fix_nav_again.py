import glob
import re

html_files = glob.glob('*.html')

dropdown_pattern = re.compile(
    r'<li class="nav-item-dropdown">\s*<a href="/market-intelligence">Market Intelligence.*?</li>',
    re.DOTALL
)

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace the dropdown block with a simple link
    new_content = dropdown_pattern.sub(r'<li><a href="/market-intelligence">Market Intelligence</a></li>', content)
    
    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed navigation in {fname}")

print('Done removing dropdown.')
