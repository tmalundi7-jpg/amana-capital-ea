import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()

# We want to find the first arc-row and insert the 03 Sep entry right before it.
first_arc_row_idx = c.find('<div class="arc-row">')

if first_arc_row_idx != -1:
    new_entry = """<div class="arc-row">
  <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">03 Sep 2026</div>
  <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Thursday, 3rd September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day figure in months...</div></div>
  <a href="/dse-wrap-2026-09-03" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
  </div>
"""

    c = c[:first_arc_row_idx] + new_entry + c[first_arc_row_idx:]
    
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Inserted 03 Sep into market-intelligence-archive.html")
else:
    print("Could not find the first arc-row.")
