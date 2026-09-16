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
    
    nav_match = re.search(r'<nav class="navbar">.*?</nav>', content, re.DOTALL)
    if not nav_match:
        issues.append(f"{file}: Missing <nav class=\"navbar\"> completely.")
        continue
        
    nav_content = nav_match.group(0)
    
    # 1. Check brand block
    if '<a class="brand-link" href="/">' not in nav_content:
        issues.append(f"{file}: Missing <a class=\"brand-link\" href=\"/\">")
    
    if '<span class="logo-word-primary">AMANA CAPITAL</span>' not in nav_content:
        issues.append(f"{file}: Missing AMANA CAPITAL text")
        
    if '<span class="logo-word-secondary">East Africa Limited</span>' not in nav_content:
        issues.append(f"{file}: Missing East Africa Limited text")
        
    if '<svg aria-hidden="true" class="brand-icon"' not in nav_content:
        issues.append(f"{file}: Missing SVG brand icon")
        
    # 2. Check mobile toggle
    if 'class="mobile-toggle"' not in nav_content or 'id="mobile-toggle"' not in nav_content:
        issues.append(f"{file}: Missing mobile toggle button")
        
    # 3. Check nav links container
    if '<ul class="nav-links"' not in nav_content:
        issues.append(f"{file}: Missing <ul class=\"nav-links\">")
        
    # 4. Check links in order
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

