import re
import glob

# 1. Restore the exact HTML of home-losers in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will find the current home-losers div and replace it with the original messy one
old_losers_regex = r'<div class="snapshot-mover" id="home-losers".*?</div>\s*</div>'
original_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>TOL <span style="color:var(--loss)">-6.6%</span></span><span>MBP <span style="color:var(--loss)">-4.8%</span></span><span>SWIS <span style="color:var(--loss)">-1.6%</span></span></div>
  </div>"""

html = re.sub(old_losers_regex, original_losers, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Revert all the DSE Snapshot CSS overrides I appended to style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I appended several blocks at the end of style.css:
# REDUCE MAIN DSE SNAPSHOT SQUARE SIZE
# PLACE GAINERS AND LOSERS NEXT TO EACH OTHER ON MOBILE (or PLACE LOSERS AFTER GAINERS ON MOBILE)
# LAPTOP/DESKTOP SNAPSHOT GRID REDESIGN
# REVERT DESKTOP SNAPSHOT GRID (BACK TO 5 COLUMNS)

# I will just strip all of these out using regex.

css = re.sub(r'/\* ============================================================\n   REDUCE MAIN DSE SNAPSHOT SQUARE SIZE\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)

css = re.sub(r'/\* ============================================================\n   PLACE LOSERS AFTER GAINERS ON MOBILE\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)

css = re.sub(r'/\* ============================================================\n   PLACE GAINERS AND LOSERS NEXT TO EACH OTHER ON MOBILE\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)

css = re.sub(r'/\* ============================================================\n   LAPTOP/DESKTOP SNAPSHOT GRID REDESIGN\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)

css = re.sub(r'/\* ============================================================\n   REVERT DESKTOP SNAPSHOT GRID \(BACK TO 5 COLUMNS\)\n   ============================================================ \*/.*?/\* ============================================================ \*/', '', css, flags=re.DOTALL)


# Also restore the original nth-child span logic that was there before I started messing with it.
# Wait, my scripts used re.sub to change the nth-child logic directly sometimes.
# Before I touched mobile, the mobile CSS was:
# .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
#     grid-column: span 2 !important;
# }
# Let's just make sure this is what is in the main max-width: 768px block.
# Actually, I had a script `fix_mobile_stack.py` which did:
# .snapshot-grid > :nth-child(3) { grid-column: span 2 !important; }
# .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) { grid-column: span 2 !important; }

# Let's just rewrite the exact mobile grid to what it was originally:
mobile_grid_fix = r"""/\* Stack Gainers and Losers sequentially \(one after another\) to prevent squishing \*/
    \.snapshot-grid > :nth-child\(3\) \{
        grid-column: span 2 !important; /\* Turnover full width \*/
    \}
    \.snapshot-grid > :nth-child\(4\), \.snapshot-grid > :nth-child\(5\) \{
        grid-column: span 2 !important; /\* Gainers and Losers each get their own full row \*/
    \}"""

original_mobile_grid = """/* Let the Top Gainers / Losers span 2 columns so they aren't squished */
    .snapshot-grid > :nth-child(4), .snapshot-grid > :nth-child(5) {
        grid-column: span 2 !important;
    }"""

css = re.sub(mobile_grid_fix, original_mobile_grid, css, flags=re.DOTALL)


with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 3. Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_full_revert', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Completely reverted all snapshot changes. Cache bumped on {bumped} files.")
