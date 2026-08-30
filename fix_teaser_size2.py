import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Append a final block to further reduce the teaser stats size
reducer_css = """
/* ============================================================
   FURTHER REDUCE TEASER STATS SIZE
   ============================================================ */

/* Make the numbers themselves even smaller */
.teaser-prem-stat-value {
    font-size: 1.15rem !important;
}

/* Make the physical squares smaller by reducing their internal padding */
.teaser-prem-stats > div, .teaser-prem-stat {
    padding: 0.85rem !important;
}

/* Ensure the label is slightly smaller to match the new proportion */
.teaser-prem-stat-label {
    font-size: 0.6rem !important;
    min-height: 20px !important;
    margin-bottom: 0.25rem !important;
}

/* Mobile adjustments for the smaller size */
@media (max-width: 768px) {
    .teaser-prem-stat-value {
        font-size: 1.1rem !important;
    }
}
@media (max-width: 480px) {
    .teaser-prem-stat-value {
        font-size: 1rem !important;
    }
    .teaser-prem-stats > div, .teaser-prem-stat {
        padding: 0.6rem !important;
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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_shrink3', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Final overrides appended. Cache bumped on {bumped} files.")
