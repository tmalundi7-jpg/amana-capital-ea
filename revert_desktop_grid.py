import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will replace the 6-column override with a 5-column override to revert the desktop layout
# while preserving the mobile stacking I did earlier.

old_pattern = r'/\* ============================================================\n   LAPTOP/DESKTOP SNAPSHOT GRID REDESIGN\n   ============================================================ \*/.*?/\* ============================================================ \*/'
new_pattern = """/* ============================================================
   REVERT DESKTOP SNAPSHOT GRID (BACK TO 5 COLUMNS)
   ============================================================ */
.snapshot-grid {
    display: grid !important;
    grid-template-columns: repeat(5, 1fr) !important;
    gap: 1rem !important;
}

/* Ensure all items just take 1 column on desktop */
.snapshot-grid > * {
    grid-column: span 1 !important;
}

/* On small screens (mobile), stack everything sequentially */
@media (max-width: 768px) {
    .snapshot-grid {
        grid-template-columns: 1fr !important;
    }
    .snapshot-grid > * {
        grid-column: span 1 !important;
    }
}
/* ============================================================ */"""

if re.search(old_pattern, css, flags=re.DOTALL):
    css = re.sub(old_pattern, new_pattern, css, flags=re.DOTALL)
else:
    # Just append an absolute override to force it
    css += new_pattern

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_revert_laptop', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Reverted desktop grid. Cache bumped on {bumped} files.")
