import re

def deduplicate_header(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find all header boxes
    pattern = r'<div class="dse-header-box".*?</div>'
    matches = list(re.finditer(pattern, c, re.DOTALL))
    
    if len(matches) >= 2:
        # Remove the SECOND header box (which is the one that Mammoth added, or the first one?
        # Let's check which one is inside the <main> block, both are.
        # Wait, the template has one, and mammoth prepended one to the content.
        # We can just remove the second occurrence.
        
        # Actually it's safer to remove the first occurrence if they are identical or just adjacent.
        # Let's just remove the first one.
        c = c[:matches[0].start()] + c[matches[0].end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Deduplicated header in {filepath}")
    else:
        print(f"No duplicate header found in {filepath}")

deduplicate_header('dse-wrap-2026-09-01.html')
deduplicate_header('dse-wrap-2026-09-02.html')
