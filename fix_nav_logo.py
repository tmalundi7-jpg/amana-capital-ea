import glob
import re
import os

html_files = glob.glob('*.html')
count = 0

old_logo = '<span class="logo-word-primary">AMANA</span>\n<span class="logo-word-primary">CAPITAL</span>'
new_logo = '<span class="logo-word-primary">AMANA CAPITAL</span>'

nav_item = '<li><a href="/risk-profiler">Risk Profiler</a></li>'

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    original = content
    
    # 1. Fix the logo
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
        
    # 2. Add Risk Profiler to the Navigation Menu if it's missing
    # Find the nav-links ul and see if Risk Profiler is there
    nav_match = re.search(r'<ul\s+[^>]*class="nav-links"[^>]*>', content)
    if nav_match:
        if '/risk-profiler' not in content and 'risk-profiler.html' not in content:
            # Insert it right before the About link
            if '<li><a href="/about"' in content:
                content = content.replace('<li><a href="/about"', nav_item + '\n                <li><a href="/about"')
            elif '<li><a href="about.html"' in content:
                content = content.replace('<li><a href="about.html"', nav_item + '\n                <li><a href="about.html"')
            else:
                # If about is missing, just stick it before the closing </ul>
                # Wait, this regex is safer
                content = re.sub(r'(</ul>)', r'    ' + nav_item + r'\n\1', content, count=1)

    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        
print(f'Updated {count} files with logo and nav fixes.')
