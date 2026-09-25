import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Date substitutions
html = html.replace('24 September 2026', '25 September 2026')
html = html.replace('Thursday, 24th September 2026', 'Friday, 25th September 2026')

# Snapshot figures
html = html.replace('<div class="snapshot-value" id="home-dsei">4,658.16</div>', '<div class="snapshot-value" id="home-dsei">4,682.13</div>')
html = html.replace('<div class="snapshot-value" id="home-tsi">10,362.31</div>', '<div class="snapshot-value" id="home-tsi">10,419.49</div>')
html = html.replace('<div class="snapshot-value" id="home-turnover">TZS 2.73 bn</div>', '<div class="snapshot-value" id="home-turnover">TZS 3.78 bn</div>')

# Teaser figures
html = html.replace('<div class="teaser-prem-stat-value">4,658.16</div>', '<div class="teaser-prem-stat-value">4,682.13</div>')
html = html.replace('<div class="teaser-prem-stat-value">TZS 2.73 bn</div>', '<div class="teaser-prem-stat-value">TZS 3.78 bn</div>')

# Teaser Link
html = re.sub(r'href="/dse-wrap-2026-\d{2}-\d{2}"', 'href="/dse-wrap-2026-09-25"', html)

# Teaser body
old_teaser_body = """The Dar es Salaam Stock Exchange delivered a quieter session on Thursday, with turnover 
contracting across both equity and fixed-income markets. Equity turnover fell 34.1% to TZS 2.73 billion, while bond 
turnover dropped 47.1% to TZS 20.87 billion. Despite the lower liquidity, the indices moved higher: the DSEI gained 
19.98 points to 4,658.16, and the TSI advanced 53.13 points to 10,362.31. The order books continue to show significant 
underlying demand, particularly in banking stocks, even as execution volumes taper off."""

new_teaser_body = """The DSE has entered a new era. Local capital is firmly in control as CRDB hits a post-split high of 2,940, pushing the DSEI to 4,682.13 while bond turnover contracts for the third consecutive session."""

html = html.replace(old_teaser_body, new_teaser_body)

# Top Gainer inside Teaser Stats
# Old: <span>TCCL</span> <span style="color: #22c55e;">+3.7%</span>
old_teaser_gainer = '<span>TCCL</span> <span style="color: #22c55e;">+3.7%</span>'
new_teaser_gainer = '<span>MUCOBA</span> <span style="color: #22c55e;">+11.1%</span>'
html = html.replace(old_teaser_gainer, new_teaser_gainer)

# Top Gainers & Losers
new_gainers = """<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
                              <span>MUCOBA <span style="color:var(--gain)">+11.1%</span></span>
                  <span>MBP <span style="color:var(--gain)">+2.9%</span></span>
                  <span>CRDB <span style="color:var(--gain)">+2.4%</span></span>
  </div>"""

new_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
                              <span>DCB <span style="color:var(--loss)">-4.5%</span></span>
                  <span>NICO <span style="color:var(--loss)">-3.5%</span></span>
                  <span>TCCL <span style="color:var(--loss)">-2.8%</span></span>
  </div>"""

html = re.sub(r'<div class="snapshot-mover" id="home-gainers".*?</div>\s*</div>', new_gainers + '\n  </div>', html, flags=re.DOTALL)
html = re.sub(r'<div class="snapshot-mover" id="home-losers".*?</div>\s*</div>', new_losers + '\n  </div>', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")
