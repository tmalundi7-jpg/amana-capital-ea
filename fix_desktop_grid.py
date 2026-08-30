import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

desktop_grid_override = """
/* ============================================================
   LAPTOP/DESKTOP SNAPSHOT GRID REDESIGN
   ============================================================ */
/* Instead of 5 squished columns, use a 6-column grid to create two rows */
.snapshot-grid {
    display: grid !important;
    grid-template-columns: repeat(6, 1fr) !important;
    gap: 1rem !important;
}

/* Row 1: DSEI, TSI, Turnover (each spans 2 of 6 columns) */
.snapshot-grid > :nth-child(1),
.snapshot-grid > :nth-child(2),
.snapshot-grid > :nth-child(3) {
    grid-column: span 2 !important;
}

/* Row 2: Top Gainers, Top Losers (each spans 3 of 6 columns) */
.snapshot-grid > :nth-child(4),
.snapshot-grid > :nth-child(5) {
    grid-column: span 3 !important;
}

/* On medium screens (tablets), switch to 2 columns */
@media (max-width: 1024px) {
    .snapshot-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    .snapshot-grid > :nth-child(1),
    .snapshot-grid > :nth-child(2) {
        grid-column: span 1 !important;
    }
    .snapshot-grid > :nth-child(3),
    .snapshot-grid > :nth-child(4),
    .snapshot-grid > :nth-child(5) {
        grid-column: span 2 !important;
    }
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
/* ============================================================ */
"""

css += desktop_grid_override

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_laptop', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Redesigned desktop grid. Cache bumped on {bumped} files.")
