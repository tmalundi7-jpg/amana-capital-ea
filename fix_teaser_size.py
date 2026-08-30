import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Append a final block to reduce the size of the teaser card and its elements

reducer_css = """
/* ============================================================
   REDUCE TEASER SQUARE SIZE AND STATS
   ============================================================ */

/* Reduce padding on the entire teaser card to make the square smaller */
.teaser-prem-left {
    padding: 2.5rem !important;
}

.teaser-prem-right {
    padding: 2.5rem !important;
}

/* Reduce the font size of the stats as requested */
.teaser-prem-stat-value {
    font-size: 1.5rem !important;
}

/* Slightly reduce the title size to match the smaller card footprint */
.teaser-prem-title {
    font-size: 1.75rem !important;
    margin-bottom: 1rem !important;
}

/* Slightly reduce the margin of the body text */
.teaser-prem-body {
    margin-bottom: 1.5rem !important;
}

/* On mobile, shrink stats a bit more so they fit well */
@media (max-width: 768px) {
    .teaser-prem-left, .teaser-prem-right {
        padding: 1.5rem !important;
    }
    .teaser-prem-stat-value {
        font-size: 1.25rem !important;
    }
    .teaser-prem-title {
        font-size: 1.5rem !important;
    }
}
@media (max-width: 480px) {
    .teaser-prem-stat-value {
        font-size: 1.1rem !important;
    }
}
/* ============================================================ */
"""

css += reducer_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bump cache on all HTML files
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_shrink', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Final overrides appended. Cache bumped on {bumped} files.")
