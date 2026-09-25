import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Snapshot Dates
html = html.replace("End-of-day &middot; 23 September 2026", "End-of-day &middot; 24 September 2026")
html = html.replace("Terminal Feed | End-of-day &middot; 23 September 2026", "Terminal Feed | End-of-day &middot; 24 September 2026")

# 2. Update Daily Wrap Dates & Title
html = html.replace("Wednesday, 23rd September 2026", "Thursday, 24th September 2026")

# 3. Update Snapshot Values
# DSEI
html = re.sub(
    r'(<div class="snapshot-value" id="home-dsei">)4,638\.18(</div>)',
    r'\g<1>4,658.16\g<2>',
    html
)
# TSI
html = re.sub(
    r'(<div class="snapshot-value" id="home-tsi">)10,309\.18(</div>)',
    r'\g<1>10,362.31\g<2>',
    html
)
# Turnover
html = re.sub(
    r'(<div class="snapshot-value" id="home-turnover">)TZS 4\.13 bn(</div>)',
    r'\g<1>TZS 2.73 bn\g<2>',
    html
)

# 4. Update Top Gainers
new_gainers = """                            <span>TCCL <span style="color:var(--gain)">+3.7%</span></span>
                <span>NICO <span style="color:var(--gain)">+3.3%</span></span>
                <span>CRDB <span style="color:var(--gain)">+1.8%</span></span>"""
old_gainers = """                            <span>MUCOBA <span style="color:var(--gain)">+3.6%</span></span>
                <span>PAL <span style="color:var(--gain)">+3.3%</span></span>
                <span>MBP <span style="color:var(--gain)">+2.9%</span></span>"""
if old_gainers in html:
    html = html.replace(old_gainers, new_gainers)
else:
    print("WARNING: Could not find old gainers. Trying regex...")
    html = re.sub(r'(id="home-gainers"[^>]*>)\s*<span>.*?</span>\s*</div>', r'\g<1>\n' + new_gainers + '\n  </div>', html, flags=re.DOTALL)

# 5. Update Top Losers
new_losers = """                            <span>MUCOBA <span style="color:var(--loss)">-5.8%</span></span>
                <span>PAL <span style="color:var(--loss)">-3.2%</span></span>
                <span>AFRIPRISE <span style="color:var(--loss)">-1.9%</span></span>"""
old_losers = """                            <span>TTP <span style="color:var(--loss)">-2.3%</span></span>
                <span>TCC <span style="color:var(--loss)">-1.6%</span></span>
                <span>SWIS <span style="color:var(--loss)">-1.5%</span></span>"""
if old_losers in html:
    html = html.replace(old_losers, new_losers)
else:
    print("WARNING: Could not find old losers. Trying regex...")
    html = re.sub(r'(id="home-losers"[^>]*>)\s*<span>.*?</span>\s*</div>', r'\g<1>\n' + new_losers + '\n  </div>', html, flags=re.DOTALL)


# 6. Update Bottom Daily Wrap Section Stats
html = re.sub(
    r'(<div class="teaser-prem-stat-value">)4,638\.18(</div>)',
    r'\g<1>4,658.16\g<2>',
    html
)
html = re.sub(
    r'(<div class="teaser-prem-stat-value">)TZS 4\.13 bn(</div>)',
    r'\g<1>TZS 2.73 bn\g<2>',
    html
)
old_wrap_gainer = """<span>MUCOBA</span> <span style="color: #22c55e;">+3.6%</span>"""
new_wrap_gainer = """<span>TCCL</span> <span style="color: #22c55e;">+3.7%</span>"""
html = html.replace(old_wrap_gainer, new_wrap_gainer)

# 7. Update Wrap Body
old_wrap_body = """The Dar es Salaam Stock Exchange delivered a session of quiet consolidation on Wednesday. Equity turnover moderated to TZS 4.13 billion, and both indices pulled back modestly from recent highs. Yet beneath these headline numbers, one stock stood out: CRDB closed with a bid-to-offer ratio of 4.34 to 1 &mdash; the most bid-heavy order book seen this week. Meanwhile, the bond market continued to attract massive institutional demand, absorbing TZS 39.47 billion in long-dated government paper."""
new_wrap_body = """The Dar es Salaam Stock Exchange delivered a quieter session on Thursday, with turnover contracting across both equity and fixed-income markets. Equity turnover fell 34.1% to TZS 2.73 billion, while bond turnover dropped 47.1% to TZS 20.87 billion. Despite the lower liquidity, the indices moved higher: the DSEI gained 19.98 points to 4,658.16, and the TSI advanced 53.13 points to 10,362.31. The order books continue to show significant underlying demand, particularly in banking stocks, even as execution volumes taper off."""
html = html.replace(old_wrap_body, new_wrap_body)

# Write back
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html")
