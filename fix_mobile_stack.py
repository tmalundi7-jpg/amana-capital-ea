import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will revert the side-by-side mobile grid and make them stack sequentially (after each other)
# by making them both span 2 columns again on mobile.

old_pattern = r'/\* Make Turnover span 2 so Top Gainers and Top Losers sit next to each other \*/.*?\.snapshot-grid > :nth-child\(4\), \.snapshot-grid > :nth-child\(5\) \{\s*grid-column: span 1 !important;\s*\}'
new_pattern = """/* Stack Gainers and Losers sequentially (one after another) to prevent squishing */
    .snapshot-grid > :nth-child(3) {
        grid-column: span 2 !important; /* Turnover full width */
    }
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 2 !important; /* Gainers and Losers each get their own full row */
    }"""

if re.search(old_pattern, css, flags=re.DOTALL):
    css = re.sub(old_pattern, new_pattern, css, flags=re.DOTALL)
else:
    # Just append an absolute override to force it
    css += """
/* ============================================================
   PLACE LOSERS AFTER GAINERS ON MOBILE
   ============================================================ */
@media (max-width: 768px) {
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 2 !important;
    }
}
/* ============================================================ */
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_stack', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Set gainers and losers to stack sequentially. Cache bumped on {bumped} files.")
