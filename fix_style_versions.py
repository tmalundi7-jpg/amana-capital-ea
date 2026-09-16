import glob
import re

html_files = glob.glob('*.html')
for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test'):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any style.css?v=... with style.css?v=20260914_logo_fix
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260914_logo_fix', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Style versions updated across all HTML files.")
