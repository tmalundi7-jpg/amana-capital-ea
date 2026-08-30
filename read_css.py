import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

print('--- teaser-prem-left ---')
for match in re.finditer(r'\.teaser-prem-left[^}]*\}', css):
    print(match.group(0))

print('--- archive-row ---')
for match in re.finditer(r'\.archive-row[^}]*\}', css):
    print(match.group(0))

print('--- core-purpose ---')
for match in re.finditer(r'\.core-purpose[^}]*\}', css):
    print(match.group(0))

print('--- bc-hero ---')
for match in re.finditer(r'\.bc-hero[^}]*\}', css):
    print(match.group(0))
