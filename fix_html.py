import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Read both files
with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    text14 = f.read()

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    text21 = f.read()

# We need to extract the actual content from text21 to insert it into text14's shell.
# In text21, the content starts after <p class="article-meta">'s closing div, which is probably missing.
# Let's find the lead paragraph in text21.
lead_p_start = text21.find('<p class="lead"')
# The content goes up to the end of section 7, before the disclaimer.
sec7_end = text21.find('market\\'s natural rhythm do the heavy lifting.</p>\n</div>')
if sec7_end != -1:
    sec7_end += len('market\\'s natural rhythm do the heavy lifting.</p>\n</div>')

content21 = text21[lead_p_start:sec7_end]

# Now let's extract the header from 14 Sep.
# The header goes up to </div><p>The Dar es Salaam Stock Exchange opened
header14_end = text14.find('</div><p>The Dar es Salaam Stock Exchange opened')
if header14_end != -1:
    header14_end += len('</div>')

header14 = text14[:header14_end]

# Modify header14 for 21 Sep
header14 = header14.replace('Monday, 14th September 2026', 'Monday, 21st September 2026')
header14 = header14.replace('14 Sep 2026', '21 Sep 2026')
header14 = header14.replace('Indices Hit New Post-Split Highs as Market Consolidates After Record Week', 'VODA Closes With Zero Offers as Local Institutions Tighten Their Grip')
header14 = header14.replace('dse-wrap-2026-09-14.html', 'dse-wrap-2026-09-21.html')
header14 = header14.replace('7th September 2026', '21st September 2026') # description meta

# Now get the footer from 14 Sep
# It starts right after the section 7 div.
sec7_14_end = text14.find('do the heavy lifting.</p></div>')
if sec7_14_end != -1:
    sec7_14_end += len('do the heavy lifting.</p></div>')

footer14 = text14[sec7_14_end:]

# Let's put it all together
final_html = header14 + "\n" + content21 + "\n" + footer14

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Reconstructed dse-wrap-2026-09-21.html using the exact shell of dse-wrap-2026-09-14.html.")
