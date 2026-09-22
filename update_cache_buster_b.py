import glob

html_files = glob.glob('*.html')
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if 'script.min.js?v=20260922' in text:
        text = text.replace('script.min.js?v=20260922', 'script.min.js?v=20260922b')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
