with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'<script src="script.min.js\?v=20260914_cache_fix" defer></script>\s*<script defer="" src="script.min.js\?v=20260914_cache_fix"></script>', '<script src="script.min.js?v=20260914_cache_fix" defer></script>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
