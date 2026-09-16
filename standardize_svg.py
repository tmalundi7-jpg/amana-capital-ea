import glob
import re

html_files = glob.glob('*.html')

standard_svg = '<svg aria-hidden="true" class="brand-icon" viewBox="0 0 32 44" height="36" width="26"><path d="M0,44 L13,0 L19,0 L6,44Z" fill="currentColor"></path><rect fill="currentColor" height="44" width="8" x="21" y="0"></rect><rect fill="currentColor" height="4" width="21" x="0" y="19"></rect></svg>'

updated_count = 0

for file in html_files:
    if file.startswith('mammoth') or file.startswith('scratch') or file.startswith('preview') or file.startswith('test') or file in ['dashboard.html', 'footer.html', 'monitoring.html', 'linkedin-banner.html', 'linkedin-profile-pic.html', 'temp_new_14_wrap.html']:
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match the <svg> block that has class="brand-icon"
    # This regex is robust to attribute ordering.
    new_content = re.sub(r'<svg[^>]*class=["\']brand-icon["\'][^>]*>.*?</svg>', standard_svg, content, flags=re.DOTALL)
    
    # Just in case some have class="brand-icon" AFTER viewbox, we need an even more robust regex for the opening tag, or match any SVG inside brand-link
    # Better yet, find <a ... class="brand-link"> and replace the SVG inside it
    new_content = re.sub(r'(<a[^>]*class=["\']brand-link["\'][^>]*>\s*)<svg[^>]*>.*?</svg>', r'\1' + standard_svg, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1

print(f"Standardized SVG in {updated_count} files.")
