import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the CSS for change-positive / change-negative classes
css_matches = re.findall(r'\.change-(?:positive|negative)[^}]+}', c)
print("=== CSS Classes Found ===")
for m in css_matches:
    print(m)

print("\n=== Sample Table Rows ===")
rows = re.findall(r'<td class="change-(?:positive|negative)">[^<]+</td>', c)
for r in rows[:5]:
    print(r)
