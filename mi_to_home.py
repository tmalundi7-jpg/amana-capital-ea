import re
import glob

# 1. Grab the mi-snapshot-card from market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

mi_snap = re.search(r'<div class="mi-snapshot-card">.*?</div>\s*</div>\s*</div>', mi_html, flags=re.DOTALL).group(0)

# 2. Add the homepage footer stuff to it so we keep the link
footer = """
  <div class="snapshot-note" id="home-snapshot-date" style="margin-top: 1rem; font-size: 0.8rem; color: rgba(11,29,58,0.6);">Terminal Feed | End-of-day, 28 August 2026</div>
  <div class="snapshot-footer-link" style="margin-top: 0.5rem;"><a class="gold-link" href="/market-intelligence" style="font-weight:600; font-size:0.9rem;">View Full Market Intelligence →</a></div>
"""
new_snap = mi_snap + footer

# 3. Replace the snapshot-card in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# The current snapshot card in index is <div class="snapshot-card">...</div>
old_snap = re.search(r'<div class="snapshot-card">.*?<div class="snapshot-footer-link">.*?</div>', index_html, flags=re.DOTALL).group(0)

index_html = index_html.replace(old_snap, new_snap)

# Also wrap it in a div with max-width so it looks like a card on the homepage
index_html = index_html.replace(new_snap, f'<div class="home-mi-wrapper" style="max-width:900px; margin: 0 auto; margin-top: -2rem; position:relative; z-index:10;">\n{new_snap}\n</div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

# 4. Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mi_to_home', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Copied MI snapshot to Home. Cache bumped on {bumped} files.")
