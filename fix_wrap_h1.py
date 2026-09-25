import re

with open('dse-wrap-2026-09-25.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the wrong title strings
html = html.replace('Daily DSE Wrap | Monday, 22nd September 2026', 'Daily DSE Wrap | Friday, 25th September 2026')
html = html.replace('VODA Limits Up, CRDB Absorbs Major Block', 'CRDB Hits Post-Split High as Local Capital Tightens Grip')

with open('dse-wrap-2026-09-25.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated h1 and subtitle")
