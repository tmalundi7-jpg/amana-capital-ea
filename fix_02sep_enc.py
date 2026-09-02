import re
with open('dse-wrap-2026-09-02.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Occurrences of A<:', len(re.findall(r'Â', c)) if 'Â' in c else c.count('Â'))
# I should check for literal non-breaking space issues
print('Occurrences of Â:', c.count('Â'))

print('Occurrences of ?" (dash):', c.count('?"'))
print('Occurrences of ?T (apostrophe):', c.count('?T'))

# Let's just fix them.
c = c.replace('Â', ' ')
c = c.replace('?"', '&mdash;')
c = c.replace('?T', '&rsquo;')
c = c.replace('"?', '&#9642;')

with open('dse-wrap-2026-09-02.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Cleaned up HTML encoding artifacts.')
