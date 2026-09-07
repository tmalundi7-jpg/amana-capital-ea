with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

colour_css = """
/* ─── Current Prices — Change % column colours ─── */
.change-positive { color: #16a34a; font-weight: 700; }
.change-negative { color: #dc2626; font-weight: 700; }
.change-neutral  { color: #64748b; font-weight: 600; }
"""

c = c + colour_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
with open('style.css', 'r', encoding='utf-8') as f:
    v = f.read()
print("Green present:", '#16a34a' in v)
print("Red present:", '#dc2626' in v)
