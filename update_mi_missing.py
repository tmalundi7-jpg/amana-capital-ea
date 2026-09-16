import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the data-tzs-value
c = re.sub(r'(id="mi-turnover".*?data-tzs-value=")\d+(")', r'\g<1>6230000000\g<2>', c)
# Or if it's data-format-type="bn" data-tzs-value="..."
c = re.sub(r'(data-tzs-value=")\d+(" id="mi-turnover")', r'\g<1>6230000000\g<2>', c)

# Fix gainers
gainers = '''<!-- GAINERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCC</span> <span style="color:var(--gain)">+1.2%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+0.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>AFRIPRISE</span> <span style="color:var(--gain)">+0.8%</span></div>
      </div>
      <!-- GAINERS_END -->'''

c = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', gainers, c, flags=re.DOTALL)

# Fix losers
losers = '''<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>PAL</span> <span style="color:var(--loss)">-10.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-10.0%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.5%</span></div>
      </div>
      <!-- LOSERS_END -->'''

c = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', losers, c, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated missing MI items')
