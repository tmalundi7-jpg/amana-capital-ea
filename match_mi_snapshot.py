import re
import glob

# 1. Get the snapshot-card from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

snapshot_card = re.search(r'<div class="snapshot-card">.*?<div class="snapshot-footer-link">.*?</div>\s*</div>', index_html, flags=re.DOTALL).group(0)

# 2. Replace the mi-snapshot-card in market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

# The mi-snapshot-card block
mi_html = re.sub(r'<div class="mi-snapshot-card">.*?</div>\s*</div>\s*</div>', snapshot_card, mi_html, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

# 3. Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_match_mi_snapshot', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Replaced MI snapshot with Homepage snapshot. Cache bumped on {bumped} files.")
