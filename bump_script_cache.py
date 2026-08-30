import glob
import re

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Bump script cache buster
    content = re.sub(r'script\.min\.js\?v=[a-zA-Z0-9_]+', 'script.min.js?v=20260830_3', content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated script cache busters.')
