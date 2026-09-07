import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- INDEX.HTML ---
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 4. Losers
losers_repl = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>VODA <span style="color:var(--loss)">-1.9%</span></span>
            <span>DSE <span style="color:var(--loss)">-1.4%</span></span>
            <span>TOL <span style="color:var(--loss)">-0.5%</span></span>
          </div>'''
old_losers = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>TCCL <span style="color:var(--loss)">-4.0%</span></span>
            <span>TTP <span style="color:var(--loss)">-2.1%</span></span>
            <span>DSE <span style="color:var(--loss)">-1.8%</span></span>
          </div>'''
c = c.replace(old_losers, losers_repl)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)


# --- MARKET INTELLIGENCE ---
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Losers
losers_repl_mi = '''<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-1.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.4%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-0.5%</span></div>
      </div>
      <!-- LOSERS_END -->'''
old_losers_mi = '''<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--loss)">-4.0%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TTP</span> <span style="color:var(--loss)">-2.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.8%</span></div>
      </div>
      <!-- LOSERS_END -->'''
c = c.replace(old_losers_mi, losers_repl_mi)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated losers.")
