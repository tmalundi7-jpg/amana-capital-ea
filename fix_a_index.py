import re, os, shutil

print("=== FIX A: index.html Template Tags & Unicode & CSS Ref ===")

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

# Backup
shutil.copy('index.html', 'index.html.bak')

# --- LOAD INCLUDES ---
def load_include(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            return fh.read().strip()
    except:
        return ''

theme_toggle   = load_include('_includes/theme-toggle.html')
auth_modal     = load_include('_includes/auth-modal.html')
newsletter     = load_include('_includes/newsletter.html')
consent_banner = load_include('_includes/consent-banner.html')

# --- FIX 1: Garbled line 57 with broken escape + include ---
# Replace the broken line (\\1\\n  {% include 'theme-toggle.html' %}) with actual include content
html = re.sub(
    r"\\1\\n\s*\{%\s*include\s*['\"]?theme-toggle\.html['\"]?\s*%\}",
    theme_toggle,
    html
)

# --- FIX 2: Replace {% include 'auth-modal.html' %} ---
html = re.sub(
    r"\{%\s*include\s*['\"]?auth-modal\.html['\"]?\s*%\}",
    auth_modal,
    html
)

# --- FIX 3: Replace {% include 'newsletter.html' %} ---
html = re.sub(
    r"\{%\s*include\s*['\"]?newsletter\.html['\"]?\s*%\}",
    newsletter,
    html
)

# --- FIX 4: Replace {% include 'consent-banner.html' %} ---
html = re.sub(
    r"\{%\s*include\s*['\"]?consent-banner\.html['\"]?\s*%\}",
    consent_banner,
    html
)

# --- FIX 5: Fix style.min.css -> style.css ---
html = html.replace('style.min.css?v=20260810k', 'style.css?v=20260830')
html = html.replace('style.min.css', 'style.css')

# --- FIX 6: Fix garbled mobile hamburger Unicode ---
# The broken hamburger ≡ / ☰ character
html = re.sub(r'<button[^>]*class="mobile-toggle"[^>]*>.*?</button>',
    '<button aria-label="Open menu" class="mobile-toggle" id="mobile-toggle">&#9776;</button>',
    html, flags=re.DOTALL)

# --- FIX 7: Fix dropdown arrow garbled char ---
html = re.sub(
    r'<span class="dropdown-arrow">[^<]{0,10}</span>',
    '<span class="dropdown-arrow">&#9660;</span>',
    html
)

# --- FIX 8: Fix any replacement character artifacts ---
html = html.replace('\ufffd', '')

# --- FIX 9: Add script.js and Phase JS if not present ---
phase_scripts = [
    'assets/js/personalisation.js',
    'assets/js/engagement.js',
    'assets/js/analytics.js',
    'assets/js/consent.js',
    'assets/js/auth.js',
    'assets/js/newsletter.js',
]

scripts_block = '\n'.join([f'<script defer src="{s}"></script>' for s in phase_scripts])

# Insert before </body> if not already present
if 'personalisation.js' not in html:
    html = html.replace('</body>', scripts_block + '\n</body>')

# Write fixed HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html fixed and saved.")

# Verify remaining template tags
remaining = re.findall(r'\{%.*?%\}', html)
print(f"Remaining template tags: {len(remaining)}")
remaining_esc = html.count('\\1\\')
print(f"Remaining escape garbage: {remaining_esc}")
print("CSS ref:", "style.css" in html and "style.min.css" not in html)
