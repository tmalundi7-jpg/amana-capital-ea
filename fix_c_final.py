import re

with open('_includes/theme-toggle.html', 'r', encoding='utf-8') as f:
    toggle_html = f.read().strip()

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Use broad regex to remove any line containing backslash garbage + a template include
# This matches: \1\n  {% include 'theme-toggle.html' %}  (in any encoding variant)
before = content.count('{%')
content = re.sub(r'[\\]+1[\\]+n\s*\{%\s*include\s*[\'"]?theme-toggle\.html[\'"]?\s*%\}', toggle_html, content)
after = content.count('{%')
print(f'Template tags removed: {before - after} (before={before}, after={after})')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Saved. Remaining {%:', after)
