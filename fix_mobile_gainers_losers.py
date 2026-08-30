import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I want to replace the span 2 logic in the mobile grid
# Old:
# .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
#     grid-column: span 2 !important;
# }

# New:
# /* Make Turnover span 2, so Gainers and Losers can be next to each other */
# .snapshot-grid > :nth-child(3) {
#     grid-column: span 2 !important;
# }
# .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
#     grid-column: span 1 !important;
# }

old_pattern = r'\.snapshot-grid > :nth-child\(4\), \.snapshot-grid > :nth-child\(5\) \{\s*grid-column: span 2 !important;\s*\}'
new_pattern = """/* Make Turnover span 2 so Top Gainers and Top Losers sit next to each other */
    .snapshot-grid > :nth-child(3) {
        grid-column: span 2 !important;
    }
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 1 !important;
    }"""

if re.search(old_pattern, css):
    css = re.sub(old_pattern, new_pattern, css)
else:
    # Just append an absolute override to force it
    css += """
/* ============================================================
   PLACE GAINERS AND LOSERS NEXT TO EACH OTHER ON MOBILE
   ============================================================ */
@media (max-width: 768px) {
    .snapshot-grid > :nth-child(3) {
        grid-column: span 2 !important;
    }
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 1 !important;
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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_sidebyside', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Set gainers and losers side by side. Cache bumped on {bumped} files.")
