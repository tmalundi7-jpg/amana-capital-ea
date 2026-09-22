import bs4
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    text14 = f.read()

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    text21 = f.read()

lead_p_start = text21.find('<p class="lead"')
# Let's find the end of the text in a robust way
sec7_end = text21.find("market's natural rhythm do the heavy lifting.</p>\n</div>")
if sec7_end != -1:
    sec7_end += len("market's natural rhythm do the heavy lifting.</p>\n</div>")
else:
    print("Could not find end of section 7 in 21 Sep")

content21 = text21[lead_p_start:sec7_end]

header14_end = text14.find('</div><p>The Dar es Salaam Stock Exchange opened')
if header14_end != -1:
    header14_end += len('</div>')

header14 = text14[:header14_end]

header14 = header14.replace('Monday, 14th September 2026', 'Monday, 21st September 2026')
header14 = header14.replace('14 Sep 2026', '21 Sep 2026')
header14 = header14.replace('Indices Hit New Post-Split Highs as Market Consolidates After Record Week', 'VODA Closes With Zero Offers as Local Institutions Tighten Their Grip')
header14 = header14.replace('dse-wrap-2026-09-14.html', 'dse-wrap-2026-09-21.html')
header14 = header14.replace('7th September 2026', '21st September 2026')

sec7_14_end = text14.find("do the heavy lifting.</p></div>")
if sec7_14_end != -1:
    sec7_14_end += len("do the heavy lifting.</p></div>")
else:
    print("Could not find end of section 7 in 14 Sep")

footer14 = text14[sec7_14_end:]

final_html = header14 + "\n" + content21 + "\n" + footer14

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Reconstructed dse-wrap-2026-09-21.html using the exact shell of dse-wrap-2026-09-14.html.")
