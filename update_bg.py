import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .services-section background to cream
html = re.sub(
    r'\.services-section \{\s*background: var\(--navy\);',
    '.services-section {\n        background: var(--cream);',
    html
)
# Update 'What We Do' header in services-section to navy
html = html.replace(
    '<h2 class="section-title" style="color:var(--cream);">Our Core Services</h2>',
    '<h2 class="section-title" style="color:var(--navy);">Our Core Services</h2>'
)
html = html.replace(
    '<div class="section-eyebrow" style="color:var(--gold);">What We Do</div>',
    '<div class="section-eyebrow">What We Do</div>'
)

# 2. Update .home-teaser background to cream
html = re.sub(
    r'\.home-teaser \{\s*background: var\(--navy\);',
    '.home-teaser {\n        background: var(--cream);',
    html
)
# Make the teaser-premium CARD have the navy background instead!
html = re.sub(
    r'\.teaser-premium \{\s*background: transparent;',
    '.teaser-premium {\n        background: var(--navy);',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_cream_bg2', content)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done backgrounds.')
