import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Append the final targeted overrides at the very end of style.css
# This guarantees it wins over any previous !important declarations

final_overrides = """
/* ============================================================
   USER REQUESTED OVERRIDES (TEASER DESIGN MATCH)
   ============================================================ */

/* 1. Ensure the right panel has a solid dark navy blue background */
.teaser-prem-right {
    background: var(--navy) !important;
}

/* 2. Ensure teaser stats font exactly matches main snapshot (2rem, 400 weight) */
.teaser-prem-stat-value {
    font-size: 2rem !important;
    font-weight: 400 !important;
    font-family: 'Cormorant Garamond', serif !important;
}

/* On mobile, shrink slightly but remain larger than before */
@media (max-width: 768px) {
    .teaser-prem-stat-value {
        font-size: 1.5rem !important;
    }
}
@media (max-width: 480px) {
    .teaser-prem-stat-value {
        font-size: 1.25rem !important;
    }
}
/* ============================================================ */
"""

css += final_overrides

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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_teaser', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Final overrides appended. Cache bumped on {bumped} files.")
