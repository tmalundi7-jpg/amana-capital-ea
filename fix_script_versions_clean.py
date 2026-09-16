import glob
import re

html_files = glob.glob('*.html')
for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test'):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any script.min.js?v=... with script.min.js?v=20260914_swup_fix
    content = re.sub(r'script\.min\.js\?v=[a-zA-Z0-9_]+', 'script.min.js?v=20260914_swup_fix', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Script cache busters updated cleanly across all HTML files.")
