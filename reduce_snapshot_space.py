import re
import glob

# 1. Update index.html section padding
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the section wrapping the snapshot
html = html.replace('<section style="padding: 5rem 0; background: var(--cream);">', '<section style="padding: 3rem 0 1rem 0; background: var(--cream);">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css to shrink the snapshot card square
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

override = """
/* ============================================================
   REDUCE SNAPSHOT SQUARE SIZE AND BOTTOM MARGIN
   ============================================================ */
.snapshot-card {
    padding: 2rem 2.5rem !important;
    margin-bottom: 0 !important;
}

@media (max-width: 768px) {
    .snapshot-card {
        padding: 1.5rem !important;
    }
}
/* ============================================================ */
"""
css += override

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_shrink_snapshot_space', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Reduced snapshot square and space. Cache bumped on {bumped} files.")
