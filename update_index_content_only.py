import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Update dates globally where applicable on the homepage
c = re.sub(r'7 September 2026', '9 September 2026', c)
c = re.sub(r'Monday, 7th September 2026', 'Wednesday, 9th September 2026', c)

# Snapshot Grid replacements (Live DSE Snapshot)
c = re.sub(r'(id="home-dsei">).*?(</div>)', r'\g<1>4,581.18\g<2>', c)
c = re.sub(r'(id="home-tsi">).*?(</div>)', r'\g<1>10,152.62\g<2>', c)
c = re.sub(r'(id="home-turnover">).*?(</div>)', r'\g<1>TZS 6.23 bn\g<2>', c)

# Fix gainers keeping the exact native format
gainers = '''<div class="snapshot-mover" id="home-gainers">
          <div style="display:flex; flex-direction:column; gap:0.25rem;">
            <span>TCC <span style="color:var(--profit)">+1.2%</span></span>
            <span>KCB <span style="color:var(--profit)">+0.9%</span></span>
            <span>AFRIPRISE <span style="color:var(--profit)">+0.8%</span></span>
          </div>
        </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-gainers"[^>]*>.*?</div>\s*</div>', gainers, c, flags=re.DOTALL)

# Fix losers keeping the exact native format
losers = '''<div class="snapshot-mover" id="home-losers">
          <div style="display:flex; flex-direction:column; gap:0.25rem;">
            <span>PAL <span style="color:var(--loss)">-10.1%</span></span>
            <span>TOL <span style="color:var(--loss)">-10.0%</span></span>
            <span>MBP <span style="color:var(--loss)">-4.5%</span></span>
          </div>
        </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-losers"[^>]*>.*?</div>\s*</div>', losers, c, flags=re.DOTALL)

# Teaser bottom widget updates
c = re.sub(r'href="/dse-wrap-2026-[0-9]{2}-[0-9]{2}"', 'href="/dse-wrap-2026-09-09"', c)

# Excerpt text
old_excerpt = 'The Dar es Salaam Stock Exchange opened the new week with a session confirming the long-anticipated rotation from bonds into equities. Equity turnover more than doubled to TZS 17.31 billion, while bond turnover collapsed to TZS 7.99 billion. The Tanzania Share Index crossed 10,000 for the first time since the NMB share split recalibrated the market.'
new_excerpt = 'The Dar es Salaam Stock Exchange delivered a sobering but instructive session on Wednesday. After two days of falling bond turnover that suggested institutional money was rotating into equities, the bond market came roaring back with TZS 35.95 billion in trades — the largest in a week. Equity turnover halved to TZS 6.23 billion as the market paused for breath. The lesson is clear: market transitions are rarely straight lines. They are choppy, unpredictable, and full of false starts. The patient investor who understands this will not be rattled.'
c = c.replace(old_excerpt, new_excerpt)

# Teaser stats replacements
c = re.sub(r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">).*?(</div>)', r'\g<1>4,581.18\g<2>', c)
c = re.sub(r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">).*?(</div>)', r'\g<1>TZS 6.23 bn\g<2>', c)

# Teaser gainer update
# The previous gainer was TOL +10.4%
old_gainer_pattern = r'<span>TOL</span> <span style="color: #22c55e;">\+10\.4%</span>'
new_gainer = r'<span>TCC</span> <span style="color: #22c55e;">+1.2%</span>'
c = re.sub(old_gainer_pattern, new_gainer, c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html updated.")
