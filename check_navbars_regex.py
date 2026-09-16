import glob
import re

html_files = glob.glob('*.html')
issues = []
expected_links = [
    'href="/"',
    'href="/market-intelligence"',
    'href="/education"',
    'href="/bond-calculator"',
    'href="/risk-profiler"',
    'href="/about"',
    'href="/contact"'
]

for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test'):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    nav_match = re.search(r'<nav class="navbar".*?</nav>', content, re.DOTALL)
    if not nav_match:
        issues.append(f"{file}: Missing <nav class=\"navbar\"> completely.")
        continue
        
    nav_content = nav_match.group(0)
    
    # 1. Check brand block
    if not re.search(r'<a[^>]+class="brand-link"[^>]*>', nav_content) and not re.search(r'<a[^>]+href="/"[^>]*class="brand-link"[^>]*>', nav_content):
        # some might have href first, some class first
        if not re.search(r'class="brand-link"', nav_content):
            issues.append(f"{file}: Missing brand-link anchor")
    
    if '<span class="logo-word-primary">AMANA CAPITAL</span>' not in nav_content:
        issues.append(f"{file}: Missing AMANA CAPITAL text")
        
    if '<span class="logo-word-secondary">East Africa Limited</span>' not in nav_content:
        issues.append(f"{file}: Missing East Africa Limited text")
        
    if not re.search(r'<svg[^>]+class="brand-icon"[^>]*>', nav_content):
        issues.append(f"{file}: Missing SVG brand icon")
        
    # 2. Check mobile toggle
    if 'class="mobile-toggle"' not in nav_content:
        issues.append(f"{file}: Missing mobile toggle button")
        
    # 3. Check nav links container
    if not re.search(r'<ul[^>]+class="nav-links"', nav_content):
        issues.append(f"{file}: Missing <ul class=\"nav-links\">")
        
    # 4. Check links
    for link in expected_links:
        if link not in nav_content:
            issues.append(f"{file}: Missing link {link}")

if not issues:
    print("All scanned HTML files have the exact required navigation structure.")
else:
    for issue in issues[:30]:
        print(issue)
    if len(issues) > 30:
        print(f"...and {len(issues) - 30} more issues.")

