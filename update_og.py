import re
import glob

html_files = glob.glob('*.html')
updated = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    new_c = c.replace('og-image.jpg', 'og-image.png')
    # Let's ensure it has an absolute path
    new_c = new_c.replace('content="og-image.png"', 'content="https://www.amana-capital-ea.co.tz/og-image.png"')
    
    if new_c != c:
        updated += 1
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_c)

print(f"Updated og-image in {updated} files.")
