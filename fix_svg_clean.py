import glob

html_files = glob.glob('*.html')
for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test'):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the exact string
    content = content.replace('<svg aria-hidden="true" class="brand-icon" viewbox="0 0 32 44">', '<svg aria-hidden="true" class="brand-icon" viewBox="0 0 32 44" height="36" width="26">')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("SVG fixed cleanly across all HTML files.")
