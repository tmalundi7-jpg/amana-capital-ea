import glob
import re

html_files = glob.glob('*.html')
count = 0

nav_item = '<li><a href="/risk-profiler">Risk Profiler</a></li>'

for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    original = content
    
    if nav_item not in content:
        if '<li><a href="/about">About</a></li>' in content:
            content = content.replace('<li><a href="/about">About</a></li>', nav_item + '\n                <li><a href="/about">About</a></li>')
        elif '<li><a href="about.html">About</a></li>' in content:
            content = content.replace('<li><a href="about.html">About</a></li>', nav_item + '\n                <li><a href="about.html">About</a></li>')
        elif '<li><a href="/about"' in content:
             content = content.replace('<li><a href="/about"', nav_item + '\n                <li><a href="/about"')

    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        
print(f'Updated {count} files nav fixes.')
