import re
with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replacements
content = content.replace('End-of-day &middot; 9 September 2026', 'End-of-day &middot; 11 September 2026')
content = content.replace('<div class="snapshot-value" id="home-dsei">4,581.18</div>', '<div class="snapshot-value" id="home-dsei">4,658.31</div>')
content = content.replace('<div class="snapshot-value" id="home-tsi">10,152.62</div>', '<div class="snapshot-value" id="home-tsi">10,400.36</div>')
content = content.replace('<div class="snapshot-value" id="home-turnover">TZS 6.23 bn</div>', '<div class="snapshot-value" id="home-turnover">TZS 16.64 bn</div>')

gainers_orig = '''          <div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>TCC <span style="color:var(--gain)">+1.2%</span></span>
            <span>KCB <span style="color:var(--gain)">+0.9%</span></span>
            <span>AFRIPRISE <span style="color:var(--gain)">+0.8%</span></span>
          </div>'''
gainers_new = '''          <div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>CRDB <span style="color:var(--gain)">+2.1%</span></span>
            <span>TCC <span style="color:var(--gain)">+1.4%</span></span>
            <span>KCB <span style="color:var(--gain)">+1.0%</span></span>
          </div>'''
content = content.replace(gainers_orig, gainers_new)

losers_orig = '''          <div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>PAL <span style="color:var(--loss)">-10.1%</span></span>
            <span>TOL <span style="color:var(--loss)">-10.0%</span></span>
            <span>MBP <span style="color:var(--loss)">-4.5%</span></span>
          </div>'''
losers_new = '''          <div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>TOL <span style="color:var(--loss)">-3.8%</span></span>
            <span>SWIS <span style="color:var(--loss)">-2.5%</span></span>
            <span>MBP <span style="color:var(--loss)">-1.9%</span></span>
          </div>'''
content = content.replace(losers_orig, losers_new)

content = content.replace('<div class="teaser-prem-date">Wednesday, 9th September 2026</div>', '<div class="teaser-prem-date">Friday, 11th September 2026</div>')
content = content.replace('<h3 class="teaser-prem-title">Daily DSE Wrap | Wednesday, 9th September 2026</h3>', '<h3 class="teaser-prem-title">Daily DSE Wrap | Friday, 11th September 2026</h3>')

teaser_body_orig = '<p class="teaser-prem-body">The Dar es Salaam Stock Exchange delivered a sobering but instructive session on Wednesday. After two days of falling bond turnover that suggested institutional money was rotating into equities, the bond market came roaring back with TZS 35.95 billion in trades — the largest in a week. Equity turnover halved to TZS 6.23 billion as the market paused for breath. The lesson is clear: market transitions are rarely straight lines. They are choppy, unpredictable, and full of false starts. The patient investor who understands this will not be rattled.</p>'
teaser_body_new = '<p class="teaser-prem-body">The Dar es Salaam Stock Exchange closed the week with a session that demonstrated the remarkable depth of local institutional demand. Equity turnover nearly doubled to TZS 16.64 billion, driven by three major block trades — a 4.9-million-share NMB block, a 600,000-share VODA block, and a 114,000-share TCC block. Yet the All-Share Index rose to a new post-split high of 4,658.31, and the Tanzania Share Index crossed 10,400. The message is clear: local capital is not just absorbing supply — it is actively bidding for it. At the same time, the bond market attracted TZS 19.43 billion in institutional money, proving that both asset classes can draw liquidity simultaneously.</p>'
content = content.replace(teaser_body_orig, teaser_body_new)

teaser_dsei_orig = '''<div class="teaser-prem-stat-label">DSEI</div>
                <div class="teaser-prem-stat-value">4,581.18</div>'''
teaser_dsei_new = '''<div class="teaser-prem-stat-label">DSEI</div>
                <div class="teaser-prem-stat-value">4,658.31</div>'''
content = content.replace(teaser_dsei_orig, teaser_dsei_new)

teaser_turnover_orig = '''<div class="teaser-prem-stat-label">Turnover</div>
                <div class="teaser-prem-stat-value">TZS 6.23 bn</div>'''
teaser_turnover_new = '''<div class="teaser-prem-stat-label">Turnover</div>
                <div class="teaser-prem-stat-value">TZS 16.64 bn</div>'''
content = content.replace(teaser_turnover_orig, teaser_turnover_new)

teaser_gainer_orig = '''<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">
                  <span>TCC</span> <span style="color: #22c55e;">+1.2%</span>
                </div>'''
teaser_gainer_new = '''<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">
                  <span>CRDB</span> <span style="color: #22c55e;">+2.1%</span>
                </div>'''
content = content.replace(teaser_gainer_orig, teaser_gainer_new)

content = content.replace('<a class="btn btn-gold-solid" href="/dse-wrap-2026-09-09">Read the Full Wrap →</a>', '<a class="btn btn-gold-solid" href="/dse-wrap-2026-09-11">Read the Full Wrap →</a>')

with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
