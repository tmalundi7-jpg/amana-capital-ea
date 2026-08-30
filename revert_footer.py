import re
import glob

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Revert footer
    bad_footer = r'<div style="font-family: \'Cormorant Garamond\', serif; color: var\(--gold\); font-weight: 600; letter-spacing: 3px; font-size: 1\.6rem; margin-bottom: 0\.3rem;">AMANA CAPITAL EAST AFRICA</div>'
    original_footer = r'<div style="color: var(--gold); font-weight: 800; letter-spacing: 0.1em; font-size: 0.85rem; margin-bottom: 0.3rem;">AMANA CAPITAL EAST AFRICA</div>'
    content = re.sub(bad_footer, original_footer, content)

    # Bump cache
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_9', content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

print('Reverted footer and bumped cache')
