import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- INDEX.HTML ---
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('End-of-day &middot; 3 September 2026', 'End-of-day &middot; 4 September 2026')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

# --- MARKET INTELLIGENCE.HTML ---
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">3 September 2026</span>', '<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">4 September 2026</span>')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Dates updated.")
