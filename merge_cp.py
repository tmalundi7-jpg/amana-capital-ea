import re

with open('old_cp.html', 'r', encoding='utf-8') as f:
    old_content = f.read()

with open('current-prices.html', 'r', encoding='utf-8') as f:
    new_content = f.read()

# Extract old table body
old_tbody_match = re.search(r'<tbody>(.*?)</tbody>', old_content, re.DOTALL)
if not old_tbody_match:
    print("Could not find tbody in old file!")
    exit(1)
old_tbody = old_tbody_match.group(1)

# Extract old date text
# Looking for "End-of-day, ... 2026" or similar
old_date_match = re.search(r'(Monday, 7th September 2026|7 September 2026|07 September 2026)', old_content)
old_date = old_date_match.group(1) if old_date_match else "Monday, 7th September 2026"

# Replace tbody in new file
# First, let's make sure we only replace the first tbody which is the main prices table
# Wait, in the new layout, there might be multiple tbodys if there's a block trades table.
# We should replace the tbody of the table with class "gold-grid-table" or similar
new_content_updated = re.sub(r'(<table[^>]*>.*?<tbody>)(.*?)(</tbody>)', r'\g<1>' + old_tbody.replace('\\', '\\\\') + r'\3', new_content, count=1, flags=re.DOTALL)

# Replace date
new_content_updated = re.sub(r'Friday, 11th September 2026', old_date, new_content_updated)
new_content_updated = re.sub(r'11 September 2026', '7 September 2026', new_content_updated)
new_content_updated = re.sub(r'11th September 2026', '7th September 2026', new_content_updated)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(new_content_updated)

print("Merged old prices into new layout.")
