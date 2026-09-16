import re

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

mobile_guardrail = """
**CURRENT PRICES PAGE MOBILE DISPLAY GUARDRAIL:**
The mobile display layout for `current-prices.html` (including edge-to-edge table scrolling, responsive font scaling for headers/tables, and the 'Swipe to scroll' indicator) is LOCKED.
It must NOT be changed unless explicitly requested by the site owner. Future content updates must reuse this same responsive structure and classes automatically without altering the desktop layout.
"""

if "**CURRENT PRICES PAGE MOBILE DISPLAY GUARDRAIL:**" not in readme:
    readme += "\n" + mobile_guardrail

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
    
print("Added mobile guardrail to README.md")
