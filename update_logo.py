import os
import glob
import re

html_files = glob.glob('*.html')
fixed_count = 0

new_logo = '''<div class="brand-text vertical-logo">
<span class="logo-word-primary">AMANA</span>
<span class="logo-word-primary">CAPITAL</span>
<span class="logo-word-secondary">EAST AFRICA LIMITED</span>
</div>'''

pattern = r'<div class="brand-text">\s*<div class="brand-title">AMANA CAPITAL</div>\s*<div class="brand-sub">EAST AFRICA</div>\s*</div>'

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
        
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    original = content
    content = re.sub(pattern, new_logo, content)
    
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"Updated logo in: {fname}")

print(f"\nTotal files updated: {fixed_count}")
