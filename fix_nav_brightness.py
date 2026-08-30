#!/usr/bin/env python3
import os, re, glob

BASE_DIR = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea'

# 1. Append override block to style.css
CSS_PATH = os.path.join(BASE_DIR, 'style.css')

OVERRIDE_BLOCK = '''
/* ====== NAV BRIGHTNESS LOCK v2 ====== */
.logo-word-primary {
    color: #FFFFFF !important;
    text-shadow: 0 0 20px rgba(229,177,59,0.12) !important;
}
.logo-word-secondary {
    color: #e5b13b !important;
    opacity: 1 !important;
}
.nav-links a {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
.nav-links a:hover,
.nav-links a.active {
    color: #FFFFFF !important;
    text-shadow: 0 0 12px rgba(229,177,59,0.5) !important;
}
/* ======================================= */
'''

with open(CSS_PATH, 'a', encoding='utf-8') as f:
    f.write(OVERRIDE_BLOCK)

print(f'[OK] Appended NAV BRIGHTNESS LOCK v2 to {CSS_PATH}')

# 2. Bump cache buster in all HTML files
NEW_VERSION = 'v=20260830_final_polish_27'
VERSION_PATTERN = re.compile(r'([?&])v=[^\s"\'&]+')

html_files = glob.glob(os.path.join(BASE_DIR, '**', '*.html'), recursive=True)
total_replaced = 0

for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, count = VERSION_PATTERN.subn(lambda m: f"{m.group(1)}{NEW_VERSION}", content)
    if count > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[OK] {os.path.relpath(html_path, BASE_DIR)} — {count} cache buster(s) updated')
        total_replaced += count
    else:
        print(f'[--] {os.path.relpath(html_path, BASE_DIR)} — no version strings found')

print(f'\nDone. {len(html_files)} HTML file(s) processed, {total_replaced} replacement(s) total.')
