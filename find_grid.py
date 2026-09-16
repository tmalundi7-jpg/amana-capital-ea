import re

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc = f.read()

# Let's find where the cards start. Usually it's after <div class="mi-snapshot-hdr"> or similar.
# Let's just find the first "archive-card" or "archive-row"
idx = arc.find('<div class="archive-card">')
if idx == -1:
    idx = arc.find('<a class="archive-row"')

print("Found at:", idx)
if idx != -1:
    print(arc[idx-200:idx])
