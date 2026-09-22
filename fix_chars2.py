import re

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to match the weird characters
content = re.sub(r'Dar es Salaam .*? Tanzania .*? Registration', 'Dar es Salaam &middot; Tanzania &middot; Registration', content)
content = re.sub(r'A\xc2\xa9 2026', '&copy; 2026', content)
content = re.sub(r'A[^\x00-\x7F] 2026', '&copy; 2026', content)

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(content)
