import os
import re

files = [
    'dse-wrap-2026-07-23.html',
    'dse-wrap-2026-07-22.html',
    'dse-wrap-2026-07-21.html',
    'dse-wrap-2026-07-20.html',
    'dse-wrap-2026-07-17.html'
]

dir_path = r'C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main'

for filename in files:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure all <h2> tags have exactly the inline style
    content = re.sub(r'<h2\b[^>]*>', r'<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">', content)

    # 2. Add class="gold-link" to links in text.
    main_match = re.search(r'(<main[^>]*>)(.*?)(</main>)', content, flags=re.DOTALL)
    if main_match:
        main_start, main_content, main_end = main_match.groups()
        
        def process_link(m):
            tag = m.group(0)
            if "Back to Market Intelligence" in tag:
                return tag
            if "gold-link" in tag:
                return tag
            # Add class="gold-link"
            if 'class="' in tag:
                return re.sub(r'class="([^"]*)"', r'class="\1 gold-link"', tag)
            else:
                return tag.replace('<a ', '<a class="gold-link" ')
                
        new_main_content = re.sub(r'<a\b[^>]*>.*?</a>', process_link, main_content, flags=re.DOTALL)
        content = content.replace(main_content, new_main_content)
        
    # 3. Locate the "Considerations for a Multi-Year Framework" section
    heading_pattern = r'<h[23][^>]*>(?:\d+\.\s*)?Considerations for a Multi-Year Framework</h[23]>'
    section_pattern = re.compile(rf'({heading_pattern}.*?)(?=\s*<div class="article-disclaimer"|\s*</div>\s*</div>)', re.DOTALL)
    
    def section_replacer(m):
        sec_content = m.group(1)
        
        sec_content = re.sub(
            r'<h[23][^>]*>((?:\d+\.\s*)?Considerations for a Multi-Year Framework)</h[23]>', 
            r'<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem;">\1</h3>', 
            sec_content
        )
        
        wrapped = f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{sec_content.strip()}\n</div>'
        return wrapped

    if re.search(heading_pattern, content):
        content = section_pattern.sub(section_replacer, content)
    else:
        print(f"Heading not found in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Formatting complete.")
