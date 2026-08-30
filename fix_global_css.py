import os, glob, re, shutil

print("=== GLOBAL CSS FIX: Update style.min.css refs to style.css ===")

html_files = glob.glob('*.html')
fixed_count = 0
total_files = 0

for fname in html_files:
    # Skip test and backup files
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original = content
    
    # Replace style.min.css with style.css
    content = re.sub(r'style\.min\.css(\?[^\'"]*)?', 'style.css?v=20260830', content)
    
    # Fix garbled hamburger unicode - any multi-byte garbled near mobile-toggle
    content = re.sub(r'(<button[^>]*class="mobile-toggle"[^>]*>)[^<]{0,20}(</button>)',
                     r'\1&#9776;\2', content)
    
    # Fix garbled dropdown arrows
    content = re.sub(r'<span class="dropdown-arrow">[^<]{0,10}</span>',
                     '<span class="dropdown-arrow">&#9660;</span>', content)
    
    # Remove \1\n garbage sequences
    content = re.sub(r'[\\]{1,4}1[\\]{1,4}n\s*', '', content)
    
    total_files += 1
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"  Fixed: {fname}")

print(f"\nTotal files processed: {total_files}")
print(f"Files updated: {fixed_count}")

# Final validation
remaining_min = 0
for fname in html_files:
    if 'test_pdf' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    if 'style.min.css' in c:
        remaining_min += 1

print(f"Files still with style.min.css: {remaining_min}")
