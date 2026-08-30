import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add an absolute master override at the very bottom of the file
# to guarantee the snapshot grid is ALWAYS swipeable on mobile
# and fixes any other mobile grid issues.

override = """
/* ============================================================
   ABSOLUTE MOBILE RESPONSIVENESS OVERRIDE
   ============================================================ */
/* 1. DSE Snapshot must ALWAYS be side-by-side (swipeable) on mobile, NOT vertical columns */
@media (max-width: 900px) {
    .snapshot-card .snapshot-grid,
    .mi-snapshot-card .snapshot-grid,
    .snapshot-grid {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        -webkit-overflow-scrolling: touch !important;
        gap: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        justify-content: flex-start !important;
    }
    
    .snapshot-item {
        flex: 0 0 auto !important;
        min-width: min-content !important;
    }

    /* Hide the scrollbar for a cleaner look but keep it swipeable */
    .snapshot-grid::-webkit-scrollbar {
        display: none;
    }
    .snapshot-grid {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
}

/* 2. Ensure general sections fit well on mobile */
@media (max-width: 768px) {
    .why-section, .services-section, .home-teaser {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .why-grid, .services-grid {
        display: flex !important;
        flex-direction: column !important;
        gap: 1.5rem !important;
    }
    
    /* Ensure the Top Gainers / Losers raw text doesn't overflow */
    .snapshot-mover {
        white-space: nowrap !important;
    }
}
/* ============================================================ */
"""
css += override

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_fix_final', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Fixed mobile responsiveness. Cache bumped on {bumped} files.")
