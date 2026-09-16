import re
import os

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Snapshot Date
text = text.replace('End-of-day &middot; 14 September 2026', 'End-of-day &middot; 15 September 2026')

# 2. Update Snapshot Values
text = re.sub(r'(<div class="snapshot-value" id="home-dsei">)[\d,\.]+</div>', r'\g<1>4,696.11</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="home-tsi">)[\d,\.]+</div>', r'\g<1>10,438.46</div>', text)
text = re.sub(r'(<div class="snapshot-value" id="home-turnover">)TZS [\d\.]+ bn</div>', r'\g<1>TZS 16.86 bn</div>', text)

# 3. Update Snapshot Gainers
gainers_html = '''<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
              <span>VODA <span style="color:var(--gain)">+3.6%</span></span>
              <span>TCCL <span style="color:var(--gain)">+2.6%</span></span>
              <span>TOL <span style="color:var(--gain)">+2.2%</span></span>
              <span>KCB <span style="color:var(--gain)">+0.9%</span></span>
            </div>'''
text = re.sub(r'<div class="snapshot-mover" id="home-gainers".*?</div>\s*</div>', gainers_html + '\n  </div>', text, flags=re.DOTALL)

# 4. Update Snapshot Losers
losers_html = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
              <span>DCB <span style="color:var(--loss)">-3.3%</span></span>
              <span>MCB <span style="color:var(--loss)">-2.5%</span></span>
              <span>CRDB <span style="color:var(--loss)">-1.4%</span></span>
              <span>SWIS <span style="color:var(--loss)">-1.1%</span></span>
              <span>TCC <span style="color:var(--loss)">-1.0%</span></span>
            </div>'''
text = re.sub(r'<div class="snapshot-mover" id="home-losers".*?</div>\s*</div>', losers_html + '\n  </div>', text, flags=re.DOTALL)

# 5. Update Bottom Wrap Section
text = text.replace('Monday, 14th September 2026', 'Tuesday, 15th September 2026')
body_new = "The Dar es Salaam Stock Exchange delivered a session of stark contrasts on Tuesday. Equity turnover surged 166.5% to TZS 16.86 billion, driven by four major block trades. The All-Share Index closed at a new post-split high of 4,696.11. Yet beneath these headline numbers lies a more nuanced picture: foreign buyers returned in their largest numbers in weeks, VODA closed with zero offers on the order book after absorbing a 1.4-million-share block, while NMB and CRDB both turned offer-heavy."
text = re.sub(r'(<p class="teaser-prem-body">).*?(</p>)', r'\g<1>' + body_new + r'\g<2>', text, count=1, flags=re.DOTALL)

text = re.sub(r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[\d,\.]+(</div>)', r'\g<1>4,696.11\g<2>', text)
text = re.sub(r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)TZS [\d\.]+ bn(</div>)', r'\g<1>TZS 16.86 bn\g<2>', text)

top_gainer_bottom = '''<div class="teaser-prem-stat-value gain" style="display:flex; justify-content:space-between; width:100%; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; letter-spacing: 0;">
            <span>VODA</span> <span style="color: #22c55e;">+3.6%</span>
          </div>'''
text = re.sub(r'<div class="teaser-prem-stat-value gain".*?</div>\s*</div>', top_gainer_bottom + '\n          </div>', text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully updated index.html')
