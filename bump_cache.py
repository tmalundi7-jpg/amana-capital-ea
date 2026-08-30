import glob

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'style.css?v=20260830"' in content:
        content = content.replace('style.css?v=20260830"', 'style.css?v=20260830_3"')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
print('Updated cache busters.')
