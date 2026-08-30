import re
import glob

# 1. Restore index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace flex-start with space-between for both Gainers and Losers in index.html
html = re.sub(r'justify-content:flex-start; gap: 0\.5rem;', r'justify-content:space-between;', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Restore market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

mi_html = re.sub(r'justify-content:flex-start; gap: 0\.5rem;', r'justify-content:space-between;', mi_html)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)


# 3. Bump cache on all HTML files
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_revert', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Reverted to space-between. Cache bumped on {bumped} files.")
