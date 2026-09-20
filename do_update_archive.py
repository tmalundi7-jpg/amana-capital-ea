import re

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The archive list starts after <div class="archive-list">
# We need to insert the 18th Sept item at the top.
# We'll take the first item, copy it, update it to 18th, and insert it before the 17th item.

start_idx = content.find('<div class="archive-item">')
end_idx = content.find('<div class="archive-item">', start_idx + 1)
first_item = content[start_idx:end_idx]

# Modify first_item for 18th
new_item = first_item.replace('17 September 2026', '18 September 2026')
new_item = new_item.replace('17 Sep 2026', '18 Sep 2026')
new_item = new_item.replace('17th September 2026', '18th September 2026')
new_item = new_item.replace('4,632.03', '4,602.26')
new_item = new_item.replace('TZS 15.39 bn', 'TZS 4.30 bn')
new_item = new_item.replace('PAL (+3.3%)', 'AFRIPRISE (+8.8%)')
new_item = new_item.replace('Banks Under Pressure as a Massive NMB Block Trade Drives a 51% Turnover Surge', 'Turnover Cools but CRDB Absorbs a 380,000-Share Block Without Flinching')
new_item = new_item.replace('dse-wrap-2026-09-17', 'dse-wrap-2026-09-18')

# Insert the new item
new_content = content[:start_idx] + new_item + content[start_idx:]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated market-intelligence-archive.html")
