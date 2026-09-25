import re

# 1. market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<strong>24 Sep 2026</strong>', r'<strong>25 Sep 2026</strong>', html)
html = re.sub(r'24 September 2026</span>', r'25 September 2026</span>', html)
html = re.sub(r'<div class="snapshot-value" id="mi-dsei">4,658.16</div>', r'<div class="snapshot-value" id="mi-dsei">4,682.13</div>', html)
html = re.sub(r'<div class="snapshot-value" id="mi-tsi">10,362.31</div>', r'<div class="snapshot-value" id="mi-tsi">10,419.49</div>', html)
html = re.sub(r'data-tzs-value="2730000000" id="mi-turnover">TZS 2.73 bn</div>', r'data-tzs-value="3780000000" id="mi-turnover">TZS 3.78 bn</div>', html)

# Gainers
gainers_html = """
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MUCOBA</span> <span style="color:var(--gain)">+11.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--gain)">+2.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>CRDB</span> <span style="color:var(--gain)">+2.4%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TPCC</span> <span style="color:var(--gain)">+1.8%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MKCB</span> <span style="color:var(--gain)">+1.4%</span></div>
      </div>
"""
html = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', f'<!-- GAINERS_START -->\n{gainers_html.strip()}\n      <!-- GAINERS_END -->', html, flags=re.DOTALL)

# Losers
losers_html = """
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DCB</span> <span style="color:var(--loss)">-4.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NICO</span> <span style="color:var(--loss)">-3.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--loss)">-2.8%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--loss)">-1.3%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-0.8%</span></div>
      </div>
"""
html = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', f'<!-- LOSERS_START -->\n{losers_html.strip()}\n      <!-- LOSERS_END -->', html, flags=re.DOTALL)

# Archive Row
archive_row = """
<a class="archive-row" href="/dse-wrap-2026-09-25">
<div class="archive-date">25 Sep<br/>2026</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | Friday, 25th September 2026</div>
<div class="archive-content-excerpt">The DSE has entered a new era. Local capital is firmly in control as CRDB hits a post-split high of 2,940, pushing the DSEI to 4,682.13 while bond turnover contracts for the third consecutive session...</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>
"""
html = re.sub(r'<a class="archive-row" href="/dse-wrap-2026-09-24">.*?</a>', archive_row.strip(), html, flags=re.DOTALL)

# Script cache buster
html = re.sub(r'script\.min\.js\?v=20260924a', 'script.min.js?v=20260925a', html)
html = re.sub(r'script\.js\?v=20260924a', 'script.js?v=20260925a', html)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated market-intelligence.html")
