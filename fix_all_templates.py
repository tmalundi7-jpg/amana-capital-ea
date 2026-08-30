import re
import glob

print("=== FIXING TEMPLATE TAGS & NAV LIST IN ALL HTML FILES ===")

def load_include(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            return fh.read().strip()
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return ''

includes_content = {
    'theme-toggle.html': load_include('_includes/theme-toggle.html'),
    'auth-modal.html': load_include('_includes/auth-modal.html'),
    'newsletter.html': load_include('_includes/newsletter.html'),
    'consent-banner.html': load_include('_includes/consent-banner.html'),
}

html_files = glob.glob('*.html')
fixed_files = 0

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
        
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    original = content
    
    # 1. Replace template tags
    for include_name, include_html in includes_content.items():
        if include_html:
            # Match {% include 'filename' %} or {% include "filename" %}
            pattern = r"\{%\s*include\s*['\"]?" + re.escape(include_name) + r"['\"]?\s*%\}"
            content = re.sub(pattern, include_html, content)
            
    # Also handle literal \1\n that might be preceding theme-toggle if missed
    content = re.sub(r'[\\]{1,4}1[\\]{1,4}n\s*', '', content)
    
    # 2. Fix nav-list wrapper missing before <li><a href="/dashboard.html"
    # The original structure was:
    # <button ... id="mobile-toggle">&#9776;</button>
    # <li><a href="/dashboard.html" ...
    # We want:
    # <button ... id="mobile-toggle">&#9776;</button>
    # <ul class="nav-list">
    #   <li><a href="/dashboard.html" ...
    
    if '<ul class="nav-list">' not in content and '<li><a href="/dashboard.html"' in content:
        content = content.replace('<li><a href="/dashboard.html"', '<ul class="nav-list">\n  <li><a href="/dashboard.html"')
        
    # Write back if changed
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_files += 1
        print(f"Fixed template tags / nav list in: {fname}")

print(f"\nTotal files fixed: {fixed_files}")
