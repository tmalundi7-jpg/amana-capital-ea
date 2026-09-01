import re
import glob

html_files = glob.glob('*.html')
updated = 0
tags_to_add = """<meta content="https://www.amana-capital-ea.co.tz/og-image-v2.png" property="og:image"/>
<meta content="image/png" property="og:image:type"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="https://www.amana-capital-ea.co.tz/og-image-v2.png" name="twitter:image"/>"""

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    if "og:image:width" not in c and "og:image" in c:
        new_c = re.sub(r'<meta content="https://www\.amana-capital-ea\.co\.tz/og-image-v2\.png" property="og:image"/>', tags_to_add, c)
        if new_c != c:
            updated += 1
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_c)

print(f"Added comprehensive OG tags to {updated} files.")
