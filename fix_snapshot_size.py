import re
import glob

# =======================================================
# 1. FIX INDEX.HTML TOP LOSERS FORMATTING
# =======================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the poorly formatted home-losers div
old_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>TOL 
<span style="color:var(--loss)">—6.6%</span></span><span>MBP <span 
style="color:var(--loss)">—4.8%</span></span><span>SWIS <span style="color:var(--loss)">—1.6%</span></span></div>"""

old_losers_regex = r'<div class="snapshot-mover" id="home-losers"[^>]*>.*?</div>'

new_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem; width:100%;">
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
  </div>"""

html = re.sub(old_losers_regex, new_losers, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# =======================================================
# 2. REDUCE DSE SNAPSHOT CARD SIZE
# =======================================================
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

snapshot_override = """
/* ============================================================
   REDUCE MAIN DSE SNAPSHOT SQUARE SIZE
   ============================================================ */

/* Reduce padding on the main snapshot card to shrink its square size */
.snapshot-card {
    padding: 2rem 2.5rem !important;
}

@media (max-width: 768px) {
    .snapshot-card {
        padding: 1.5rem !important;
    }
}
@media (max-width: 480px) {
    .snapshot-card {
        padding: 1rem !important;
    }
}
/* ============================================================ */
"""

css += snapshot_override

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# =======================================================
# 3. BUMP CACHE
# =======================================================
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_shrink2', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Fixed losers layout and shrunk snapshot card. Cache bumped on {bumped} files.")
