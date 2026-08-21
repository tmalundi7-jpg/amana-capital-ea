import re

files_to_fix = ['dse-wrap-2026-08-14.html', 'dse-wrap-2026-08-17.html', 'dse-wrap-2026-08-18.html']

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove H2 for "4. Today's Concept"
    content = re.sub(r'<h2[^>]*>4\.\s+Today.*?</h2>\s*', '', content)
    
    # Renumber 5 -> 4
    content = re.sub(r'(<h2[^>]*>)5\.\s+(.*?)</h2>', r'\g<1>4. \g<2></h2>', content)
    
    # Renumber 6 -> 5
    content = re.sub(r'(<h2[^>]*>)6\.\s+(.*?)</h2>', r'\g<1>5. \g<2></h2>', content)
    
    # Renumber 7 -> 6
    content = re.sub(r'(<h2[^>]*>)7\.\s+(.*?)</h2>', r'\g<1>6. \g<2></h2>', content)
    
    # Renumber 8 -> 7 (It's an h3)
    content = re.sub(r'(<h3[^>]*>)8\.\s+(.*?)</h3>', r'\g<1>7. \g<2></h3>', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Renumbered {file_path}')
