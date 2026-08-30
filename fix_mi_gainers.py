with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Manual slicing replacement
# GAINERS
idx_start = html.find('<!-- GAINERS_START -->')
idx_end = html.find('<!-- GAINERS_END -->')
if idx_start != -1 and idx_end != -1:
    new_gainers = '''<!-- GAINERS_START -->
    <div style="display:flex; flex-direction:column; gap:0.25rem; width:100%;">
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
    </div>
    '''
    html = html[:idx_start] + new_gainers + html[idx_end:]

# LOSERS
idx_start = html.find('<!-- LOSERS_START -->')
idx_end = html.find('<!-- LOSERS_END -->')
if idx_start != -1 and idx_end != -1:
    new_losers = '''<!-- LOSERS_START -->
    <div style="display:flex; flex-direction:column; gap:0.25rem; width:100%;">
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
    </div>
    '''
    html = html[:idx_start] + new_losers + html[idx_end:]

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(html)
