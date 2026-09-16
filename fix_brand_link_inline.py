import glob

html_files = glob.glob('*.html')
for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test'):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<a class="brand-link" href="/">', '<a class="brand-link" href="/" style="display: flex !important; align-items: center !important; gap: 0.5rem !important; text-decoration: none !important;">')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Inline CSS injected into brand-link.")
