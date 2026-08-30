import glob
import re

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    changed = False

    if fname == 'market-intelligence.html':
        # Remove 'Live Feed'
        content = re.sub(r'<span class="mi-badge">[^<]*Live Feed[^<]*</span>', '', content)
        # Fix Latest Report
        content = re.sub(r'28 Aug 2026\s*<br>\s*Latest Report\s*issued today', '28 Aug 2026<br>Latest Report', content)
        content = re.sub(r'28 Aug 2026[\s\S]*?Latest Report\s*issued today', '28 Aug 2026<br>Latest Report', content)
        changed = True

    if fname == 'index.html':
        content = re.sub(r'\.service-card \{\s*background: #[A-Za-z0-9]+;', '.service-card {\n        background: var(--navy);', content)
        content = re.sub(r'\.service-card h3 \{\s*font-family', '.service-card h3 {\n        color: var(--cream);\n        font-family', content)
        content = re.sub(r'\.service-card p \{\s*font-size: 1rem;\s*color: rgba[^;]+;', '.service-card p {\n        font-size: 1rem;\n        color: #fbf7f0;', content)
        content = re.sub(r'\.service-num \{', '.service-num {\n        color: var(--gold);', content)
        changed = True

    if changed:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()
# Replace gap: 2rem with gap: 1rem
css = re.sub(r'gap: 2rem;', 'gap: 1.2rem;', css) # Let's make it 1.2rem
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_spacing_navy', content)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done python modifications')
