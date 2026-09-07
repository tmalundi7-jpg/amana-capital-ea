import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Hero Date
c = re.sub(
    r'(<div class="mi-hero-meta">\s*<strong>)[^<]*(</strong>)',
    r'\g<1>04 Sep 2026\g<2>',
    c
)

# Metrics
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

# Gainers
gainers_repl = '''<!-- GAINERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.7%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+3.6%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+2.6%</span></div>
      </div>
      <!-- GAINERS_END -->'''
c = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', gainers_repl, c, flags=re.DOTALL)

# Losers
losers_repl = '''<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-1.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.4%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-0.5%</span></div>
      </div>
      <!-- LOSERS_END -->'''
c = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', losers_repl, c, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed MI html")
