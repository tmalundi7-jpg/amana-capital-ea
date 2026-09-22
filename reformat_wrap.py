import re

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace h3 styles with h2 styles from 14/09
old_h3_pattern = r'<h3 style="color: var\(--navy\); font-size: 1.4rem; font-family: \'Cormorant Garamond\', serif; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; border-left: 3px solid var\(--gold\); padding-left: 0.75rem;">'
new_h2 = '<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">'

content = re.sub(old_h3_pattern, new_h2, content)
content = content.replace('</h3>', '</h2>')

# Wrap section 7 in the div
sec7_start_pattern = r'<h2 style="color: var\(--navy\); margin-top: 2.5rem; margin-bottom: 1.5rem;">7\. Considerations for a Multi-Year Framework</h2>'

sec7_new = """<div class="" style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">
  <h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h3>"""

content = re.sub(sec7_start_pattern, sec7_new, content)

# Close the div before the disclaimer
# The disclaimer starts with <p style="font-size: 0.85rem; color: #666;
# Actually in 21 Sep I just had <br>\n</div>
# Let's find where to close it.
content = content.replace('<br>\n</div>', '</div>\n</div>')

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Reformatted dse-wrap-2026-09-21.html")
