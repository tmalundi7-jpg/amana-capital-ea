
import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
start_idx = content.find(start_str)
end_idx = content.find('</div>\n  </div>\n\n  <div class="table-container">', start_idx)

if start_idx != -1 and end_idx != -1:
    print('Found section:')
    print(content[start_idx:end_idx + 14])
else:
    print('Not found')
