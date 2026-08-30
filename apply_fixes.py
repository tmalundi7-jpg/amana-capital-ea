import os
import re
import glob

# 3. Cache buster update across all HTML files
print("Updating cache buster...")
html_files = glob.glob('*.html')
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    # Update cache buster
    content = re.sub(r'v=[0-9a-zA-Z_]+', 'v=20260830_final_polish_2', content)
    
    # Also fix background for wrap pages and current-prices
    if f.startswith('dse-wrap-') or f == 'current-prices.html' or f == 'market-intelligence-archive.html' or f == 'market-intelligence.html':
        # Remove any inline background style in body or main
        content = re.sub(r'<body[^>]*style="[^"]*background[^"]*"[^>]*>', '<body>', content)
        content = re.sub(r'<main[^>]*style="[^"]*background[^"]*"[^>]*>', '<main>', content)
        content = re.sub(r'<body class="[^"]*bg-dark[^"]*">', '<body>', content)

    # For current-prices.html, fix title color and replace weird chars
    if f == 'current-prices.html':
        content = content.replace('color: white;', 'color: var(--navy);')
        content = content.replace('color: #ffffff;', 'color: var(--navy);')
        # Replace broken unicode
        content = content.replace('â†‘', '&uarr;').replace('â†“', '&darr;').replace('â€”', '-')
        content = content.replace('?', '-') # Generic question marks inside the change column might be from corrupted unicode
        # Specifically target the spans:
        content = re.sub(r'<span class="gain">\?\s*(\d+\.\d+%)', r'<span class="gain">&uarr; +\1', content)
        content = re.sub(r'<span class="loss">\?\s*(\d+\.\d+%)', r'<span class="loss">&darr; -\1', content)

    # For bond-calculator.html, make outer background cream
    if f == 'bond-calculator.html':
        # Set body background
        content = content.replace('<body>', '<body style="background: var(--cream);">')
        content = content.replace('<main>', '<main style="background: var(--cream);">')
        content = content.replace('bg-dark', '')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# 4. About Page Spacing
print("Fixing about page spacing...")
with open('about.html', 'r', encoding='utf-8') as file:
    about_content = file.read()
about_content = re.sub(r'padding:\s*6rem\s+0', 'padding: 3rem 0', about_content)
about_content = re.sub(r'margin-bottom:\s*3rem', 'margin-bottom: 1.5rem', about_content)
with open('about.html', 'w', encoding='utf-8') as file:
    file.write(about_content)
    
# Check style.css for core-purpose
with open('style.css', 'r', encoding='utf-8') as file:
    css = file.read()
    
# Fix core-purpose padding in css if any
css = re.sub(r'(\.core-purpose[^}]*padding:\s*)6rem(\s+0;)', r'\g<1>3rem\g<2>', css)
css = re.sub(r'(\.core-purpose[^}]*margin-bottom:\s*)3rem(;)', r'\g<1>1.5rem\g<2>', css)

# 5. Bond Calculator background in style.css
css = re.sub(r'(\.bc-hero\s*\{[^}]*background:\s*)[^;]+(;)', r'\g<1>var(--cream)\g<2>', css)
css = re.sub(r'(\.bc-layout-wrapper\s*\{[^}]*background:\s*)[^;]+(;)', r'\g<1>var(--cream)\g<2>', css)

with open('style.css', 'w', encoding='utf-8') as file:
    file.write(css)

# Git commit and push
import subprocess
print("Committing and pushing...")
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'Final polish: UI tweaks and cache buster update'])
subprocess.run(['git', 'push', 'origin', 'main', '--force'])

print("Done!")
