import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the DSEI inside teaser-prem-stats
old_teaser_dsei = '<div class="teaser-prem-stat-value">4,395.95</div>'
new_teaser_dsei = '<div class="teaser-prem-stat-value">4,415.49</div>'
c = c.replace(old_teaser_dsei, new_teaser_dsei)

# Fix the Top Gainer inside teaser-prem-stats
old_teaser_gainer = '''<span>DCB</span> <span style="color: #22c55e;">+3.2%</span>'''
new_teaser_gainer = '''<span>SWIS</span> <span style="color: #22c55e;">+5.1%</span>'''
c = c.replace(old_teaser_gainer, new_teaser_gainer)

# Verify button link
# We already did `c.replace('href="/dse-wrap-2026-09-01"', 'href="/dse-wrap-2026-09-02"')` globally, but let's be absolutely sure.
# Find the button
match = re.search(r'<a[^>]*href="(/dse-wrap-2026-09-\d\d(?:\.html)?)"[^>]*>.*?Read the Full Wrap.*?</a>', c, re.DOTALL | re.IGNORECASE)
if match:
    href = match.group(1)
    if href != '/dse-wrap-2026-09-02':
        print(f"Button had wrong href: {href}, fixing...")
        c = c.replace(href, '/dse-wrap-2026-09-02')

# There might also be a 'dse-wrap-2026-08-31' or something. Let's globally replace the specific button.
# The button class is likely `btn` or something, but let's just regex the exact text.
c = re.sub(r'<a href="[^"]*?"( class="btn btn-primary"[^>]*)>\s*Read the Full Wrap', 
           r'<a href="/dse-wrap-2026-09-02"\g<1>>Read the Full Wrap', c, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed teaser stats and button!")
