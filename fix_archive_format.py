import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()

# I need to completely replace whatever arc-row for 03 Sep and 02 Sep exists, with just the 02 Sep properly formatted.
# The 01 Sep one should remain. Let's find the 01 Sep entry.

idx_01 = c.find('01 Sep 2026')
if idx_01 == -1:
    print("Could not find 01 Sep")
    sys.exit(1)

# Find the start of the arc-row for 01 Sep
idx_01_start = c.rfind('<div class="arc-row">', 0, idx_01)

if idx_01_start == -1:
    print("Could not find start of 01 Sep")
    sys.exit(1)

# Let's find the very first arc-row in the file, which should be where the archive list begins.
# Wait, I need to find the start of the archive list container.
first_arc_row_idx = c.find('<div class="arc-row">')

# Everything from first_arc_row_idx up to idx_01_start is the 03 Sep and 02 Sep entries I previously added.
# I will replace that whole chunk with just the properly formatted 02 Sep entry.

new_entry = """<div class="arc-row">
  <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">02 Sep 2026</div>
  <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Wednesday, 2nd September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion, a 75% drop from Tuesday's NMB-driven surge...</div></div>
  <a href="/dse-wrap-2026-09-02" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
  </div>
"""

# Wait, does 01 Sep have `background: rgba(11,29,58,0.02)` or something?
# In the original CSS, odd items have background: rgba(11,29,58,0.02);
# .arc-row:nth-child(even) { background: transparent; }
# .arc-row:nth-child(odd) { background: rgba(11,29,58,0.02); }
# So I don't need to manually add inline style backgrounds! The CSS handles it.

c_new = c[:first_arc_row_idx] + new_entry + c[idx_01_start:]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

print("Fixed market-intelligence-archive.html")
