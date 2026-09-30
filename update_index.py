import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Top dates
html = html.replace('End-of-day &middot; 28 September 2026', 'End-of-day &middot; 29 September 2026')

# 2. DSEI value
html = html.replace('<div class="snapshot-value" id="home-dsei">4,658.84</div>', '<div class="snapshot-value" id="home-dsei">4,650.62</div>')
html = html.replace('<div class="teaser-prem-stat-value">4,658.84</div>', '<div class="teaser-prem-stat-value">4,650.62</div>')

# 3. TSI value
html = html.replace('<div class="snapshot-value" id="home-tsi">10,335.05</div>', '<div class="snapshot-value" id="home-tsi">10,310.90</div>')

# 4. Turnover
html = html.replace('<div class="snapshot-value" id="home-turnover">TZS 4.63 bn</div>', '<div class="snapshot-value" id="home-turnover">TZS 6.01 bn</div>')
html = html.replace('<div class="teaser-prem-stat-value">TZS 4.63 bn</div>', '<div class="teaser-prem-stat-value">TZS 6.01 bn</div>')

# 5. Top Gainers
old_gainers = """<span>NICO <span style="color:var(--gain)">+4.2%</span></span>
                  <span>PAL <span style="color:var(--gain)">+3.3%</span></span>
                  <span>MCB <span style="color:var(--gain)">+2.7%</span></span>"""
new_gainers = """<span>MCB <span style="color:var(--gain)">+2.6%</span></span>
                  <span>TCC <span style="color:var(--gain)">+0.9%</span></span>
                  <span>TPCC <span style="color:var(--gain)">+0.5%</span></span>"""
html = html.replace(old_gainers, new_gainers)

# 6. Top Losers
old_losers = """<span>SWIS <span style="color:var(--loss)">-2.3%</span></span>
                  <span>VODA <span style="color:var(--loss)">-1.6%</span></span>
                  <span>NMB <span style="color:var(--loss)">-1.4%</span></span>"""
new_losers = """<span>DCB <span style="color:var(--loss)">-3.5%</span></span>
                  <span>AFRIPRISE <span style="color:var(--loss)">-1.3%</span></span>
                  <span>NICO <span style="color:var(--loss)">-1.1%</span></span>"""
html = html.replace(old_losers, new_losers)

# 7. Bottom Daily DSE Wrap section Date
html = html.replace('Monday, 28th September 2026', 'Tuesday, 29th September 2026')
html = html.replace('Daily DSE Wrap | Monday, 28th September 2026', 'Daily DSE Wrap | Tuesday, 29th September 2026')

# 8. Bottom Daily DSE Wrap section Body
old_body = """<p class="teaser-prem-body">The Dar es Salaam Stock Exchange opened the new week with a session that told two very different stories. On the surface, equity turnover rose 22% to TZS 4.63 billion, and the number of individual deals surged 38% to 5,120 &mdash; the highest in weeks. Yet both indices pulled back from recent highs, and the large-cap order books turned offer-heavy. Meanwhile, in the bond market, turnover contracted for the fourth consecutive session. This is the pattern that experienced investors watch for: institutional money quietly stepping away from fixed income while equities attract fresh capital. For everyday investors, understanding this dynamic is essential.</p>"""
new_body = """<p class="teaser-prem-body">Tuesday's session delivered the clearest signal yet that institutional money is rotating from bonds into equities. Government bond turnover collapsed 87.3% to TZS 1.45 billion &mdash; the lowest reading in weeks &mdash; while equity turnover rose 30% to TZS 6.01 billion. This is the pattern that experienced investors watch for. When institutions buy government bonds, they are parking cash in a safe, predictable asset. When they sell bonds or stop buying, that cash has to go somewhere. Often, it moves into equities &mdash; particularly high-quality, dividend-paying stocks.</p>"""
html = html.replace(old_body, new_body)

# 9. Top Gainer in teaser
old_teaser_gainer = """<span>NICO</span> <span style="color: #22c55e;">+4.2%</span>"""
new_teaser_gainer = """<span>MCB</span> <span style="color: #22c55e;">+2.6%</span>"""
html = html.replace(old_teaser_gainer, new_teaser_gainer)

# 10. Link
html = html.replace('/dse-wrap-2026-09-28', '/dse-wrap-2026-09-29')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
