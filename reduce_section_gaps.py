import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

override = """
/* ============================================================
   REDUCE VERTICAL SPACE BETWEEN MAIN HOMEPAGE SECTIONS
   ============================================================ */
/* Reduce padding on the main sections to bring them closer together */
.why-section,
.services-section,
.home-teaser {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Also reduce the huge margin under the section headers (e.g. 'What We Do') */
.why-section-header {
    margin-bottom: 2rem !important; /* Reduced from 3rem/3.5rem */
}

@media (max-width: 768px) {
    .why-section,
    .services-section,
    .home-teaser {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    .why-section-header {
        margin-bottom: 1.5rem !important;
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
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_reduce_section_gaps', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Reduced section vertical gaps. Cache bumped on {bumped} files.")
