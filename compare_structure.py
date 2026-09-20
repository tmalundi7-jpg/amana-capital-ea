import re

def get_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only HTML tags
    tags = re.findall(r'<\w[^>]*>|<\/\w+>', content)
    return tags

tags_17 = get_structure('dse-wrap-2026-09-17.html')
tags_18 = get_structure('dse-wrap-2026-09-18.html')

# Find the start of the main swup block
start_17 = tags_17.index('<main id="swup">')
start_18 = tags_18.index('<main id="swup">')

print("17th Tags (first 25 after main):")
for t in tags_17[start_17:start_17+25]: print(t)

print("\n18th Tags (first 25 after main):")
for t in tags_18[start_18:start_18+25]: print(t)

