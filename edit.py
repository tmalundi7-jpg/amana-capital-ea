import re
import os

os.chdir(r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea")

# 1. Header Navigation Polish (style.css)
with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()

css = css.replace("gap: 2rem;", "gap: 1rem;") # in .nav-links
with open("style.css", "w", encoding="utf-8") as f:
    f.write(css)

# 2. Core Services Cards (index.html)
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace service card background
html = html.replace(
    ".service-card {\n        background: #ffffff;",
    ".service-card {\n        background: var(--navy);"
)
# Replace service card h3 text color
html = html.replace(
    ".service-card h3 {\n        font-family: 'Cormorant Garamond', serif;\n        font-size: 2rem;\n        font-weight: 600;\n        color: var(--navy);",
    ".service-card h3 {\n        font-family: 'Cormorant Garamond', serif;\n        font-size: 2rem;\n        font-weight: 600;\n        color: var(--cream);"
)
# Replace service card p text color
html = html.replace(
    ".service-card p {\n        font-size: 1rem;\n        color: rgba(11,29,58,0.7);",
    ".service-card p {\n        font-size: 1rem;\n        color: rgba(251,247,240,0.8);"
)

# Remove swup
html = html.replace('<main id="swup">', '<main>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 3. Market Intelligence (market-intelligence.html)
with open("market-intelligence.html", "r", encoding="utf-8") as f:
    mi = f.read()

mi = mi.replace("Latest Report<br/>issued today", "Latest Report")
mi = mi.replace('<span class="live-badge">Live Feed</span>', '')
mi = mi.replace('grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));', 'grid-template-columns: repeat(5, 1fr);')
mi = mi.replace('<main id="swup">', '<main>')

with open("market-intelligence.html", "w", encoding="utf-8") as f:
    f.write(mi)

# 4. Education (education.html)
with open("education.html", "r", encoding="utf-8") as f:
    edu = f.read()

edu = edu.replace('<main id="swup">', '<main>')
with open("education.html", "w", encoding="utf-8") as f:
    f.write(edu)

print("Edits complete.")
