import re
import glob

# =========================================================
# 1. FIX TEASER DESIGN inline <style> in index.html
# =========================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the current .teaser-prem-title rule in the inline style block and patch it
# Use regex to find and replace each rule individually within the <style> block

def patch_inline_style(html, old_pattern, new_rule):
    """Replace a CSS rule within the inline <style> block."""
    match = re.search(old_pattern, html, re.DOTALL)
    if match:
        html = html[:match.start()] + new_rule + html[match.end():]
        return html, True
    return html, False

# Patch .teaser-prem-title
html, ok = patch_inline_style(
    html,
    r'\.teaser-prem-title \{[^}]+\}',
    """.teaser-prem-title {
          font-family: 'Cormorant Garamond', serif;
          font-size: 2.1rem;
          font-weight: 600;
          color: var(--cream);
          line-height: 1.2;
          margin-bottom: 1.5rem;
          letter-spacing: -0.5px;
      }"""
)
print("teaser-prem-title patched:", ok)

# Patch .teaser-prem-body
html, ok = patch_inline_style(
    html,
    r'\.teaser-prem-body \{[^}]+\}',
    """.teaser-prem-body {
          font-size: 0.92rem;
          color: rgba(251,247,240,0.72);
          line-height: 1.75;
          margin-bottom: 2rem;
          border-left: 3px solid var(--gold);
          padding-left: 1.25rem;
      }"""
)
print("teaser-prem-body patched:", ok)

# Patch .teaser-prem-date
html, ok = patch_inline_style(
    html,
    r'\.teaser-prem-date \{[^}]+\}',
    """.teaser-prem-date {
          font-size: 0.78rem;
          color: rgba(251,247,240,0.5);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 1rem;
          font-weight: 600;
      }"""
)
print("teaser-prem-date patched:", ok)

# Patch .teaser-right-label
html, ok = patch_inline_style(
    html,
    r'\.teaser-right-label \{[^}]+\}',
    """.teaser-right-label {
          font-family: 'Cormorant Garamond', serif;
          font-size: 1.6rem;
          font-weight: 700;
          color: var(--gold);
          margin-bottom: 0;
          letter-spacing: 0.3px;
      }"""
)
print("teaser-right-label patched:", ok)

# Patch .teaser-right-cta-text
html, ok = patch_inline_style(
    html,
    r'\.teaser-right-cta-text \{[^}]+\}',
    """.teaser-right-cta-text {
          font-size: 0.95rem;
          color: rgba(251,247,240,0.75);
          line-height: 1.7;
          font-style: italic;
      }"""
)
print("teaser-right-cta-text patched:", ok)

# Patch .teaser-right-divider
html, ok = patch_inline_style(
    html,
    r'\.teaser-right-divider \{[^}]+\}',
    """.teaser-right-divider {
          width: 50px;
          height: 2px;
          background: var(--gold);
          margin-bottom: 1.5rem;
      }"""
)
print("teaser-right-divider patched:", ok)

# Bump cache
html = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v2', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# =========================================================
# 2. NAV BRIGHTNESS LOCK in style.css
# =========================================================
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Append authoritative nav brightness override at the very end
nav_lock = """
/* ====== NAV BRIGHTNESS LOCK v3 (FINAL) ====== */
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
/* ============================================= */
"""
css += nav_lock

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# =========================================================
# 3. BUMP CACHE on all remaining HTML files
# =========================================================
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if fname == 'index.html' or 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v2', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Nav brightness locked. Cache bumped on {bumped} additional files.")
print("Done.")
