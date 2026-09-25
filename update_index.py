import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Snapshot Dates
html = html.replace("End-of-day &middot; 22 September 2026", "End-of-day &middot; 23 September 2026")
html = html.replace("Terminal Feed | End-of-day &middot; 22 September 2026", "Terminal Feed | End-of-day &middot; 23 September 2026")

# 2. Update Daily Wrap Dates & Title
html = html.replace("Tuesday, 22nd September 2026", "Wednesday, 23rd September 2026")

# 3. Update Snapshot Values
# DSEI
html = re.sub(
    r'(<div class="snapshot-value" id="home-dsei">)4,659\.23(</div>)',
    r'\g<1>4,638.18\g<2>',
    html
)
# TSI
html = re.sub(
    r'(<div class="snapshot-value" id="home-tsi">)10,359\.92(</div>)',
    r'\g<1>10,309.18\g<2>',
    html
)
# Turnover
html = re.sub(
    r'(<div class="snapshot-value" id="home-turnover">)TZS 5\.07 bn(</div>)',
    r'\g<1>TZS 4.13 bn\g<2>',
    html
)

# 4. Update Top Gainers
new_gainers = """                            <span>MUCOBA <span style="color:var(--gain)">+3.6%</span></span>
                <span>PAL <span style="color:var(--gain)">+3.3%</span></span>
                <span>MBP <span style="color:var(--gain)">+2.9%</span></span>"""
html = re.sub(
    r'(id="home-gainers"[^>]*>)\s*<span>AFRIPRISE.*?</span >\s*</span>\s*</div>',
    r'\g<1>\n' + new_gainers + '\n  </div>',
    html, flags=re.DOTALL
)
# The above regex might be tricky, let's just do a direct string replace if it doesn't match perfectly.
# Wait, safer direct replace:
old_gainers = """<span>AFRIPRISE <span style="color:var(--gain)">+5.4%</span></span>
                <span>VODA <span style="color:var(--gain)">+4.8%</span></span>
                <span>MCB <span style="color:var(--gain)">+1.3%</span></span>"""
html = html.replace(old_gainers, new_gainers)

# 5. Update Top Losers
old_losers = """<span>TCCL <span style="color:var(--loss)">-5.1%</span></span>
                <span>PAL <span style="color:var(--loss)">-1.6%</span></span>
                <span>NICO <span style="color:var(--loss)">-1.4%</span></span>"""
new_losers = """<span>TTP <span style="color:var(--loss)">-2.3%</span></span>
                <span>TCC <span style="color:var(--loss)">-1.6%</span></span>
                <span>SWIS <span style="color:var(--loss)">-1.5%</span></span>"""
html = html.replace(old_losers, new_losers)

# 6. Update Bottom Daily Wrap Section Stats
html = re.sub(
    r'(<div class="teaser-prem-stat-value">)4,659\.23(</div>)',
    r'\g<1>4,638.18\g<2>',
    html
)
html = re.sub(
    r'(<div class="teaser-prem-stat-value">)TZS 5\.07 bn(</div>)',
    r'\g<1>TZS 4.13 bn\g<2>',
    html
)
old_wrap_gainer = """<span>AFRIPRISE</span> <span style="color: #22c55e;">+5.4%</span>"""
new_wrap_gainer = """<span>MUCOBA</span> <span style="color: #22c55e;">+3.6%</span>"""
html = html.replace(old_wrap_gainer, new_wrap_gainer)

# 7. Update Wrap Body
old_wrap_body = """The Dar es Salaam Stock Exchange delivered a session of remarkable contrasts on Tuesday. Equity turnover moderated to TZS 5.07 billion, yet both indices closed at new post-split highs. VODA surged to its 5% upper limit after absorbing a 1-million-share block on Monday, while CRDB digested an 868,000-share block without moving. Foreign selling surged to 57.58% of turnover &mdash; but every share was absorbed by local institutions."""
new_wrap_body = """The Dar es Salaam Stock Exchange delivered a session of quiet consolidation on Wednesday. Equity turnover moderated to TZS 4.13 billion, and both indices pulled back modestly from recent highs. Yet beneath these headline numbers, one stock stood out: CRDB closed with a bid-to-offer ratio of 4.34 to 1 &mdash; the most bid-heavy order book seen this week. Meanwhile, the bond market continued to attract massive institutional demand, absorbing TZS 39.47 billion in long-dated government paper."""
html = html.replace(old_wrap_body, new_wrap_body)

# Write back
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html")
