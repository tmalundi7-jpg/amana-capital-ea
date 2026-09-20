import re

# Read 17th
with open('17_main_full.txt', 'r', encoding='utf-8') as f:
    main_17 = f.read()

# We need to extract the parts before and after the content body from 17th
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    content_17 = f.read()

# The prefix goes up to <div class="dse-header-box"
prefix_match = re.search(r'(.*?)<div class="dse-header-box"', content_17, re.DOTALL)
prefix = prefix_match.group(1)

# The suffix starts at <div class="article-disclaimer"
suffix_match = re.search(r'(<div class="article-disclaimer".*)', content_17, re.DOTALL)
suffix = suffix_match.group(1)

# Now build the new body
new_body = '''<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">Daily DSE Wrap | Friday, 18th September 2026</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">Turnover Cools but CRDB Absorbs a 380,000-Share Block Without Flinching</p>
</div>

<p>The Dar es Salaam Stock Exchange closed the week with a session of quiet resilience. Equity turnover fell 72% to TZS 4.30 billion from Thursday's block-heavy TZS 15.39 billion, and the All-Share Index slipped 30 points. Yet beneath these headline numbers, CRDB absorbed a 380,000-share block trade and closed just 30 shillings lower. Meanwhile, VODA closed with a bid-to-offer ratio of nearly 11 to 1, and AFRIPRISE surged 8.8%. The market is not retreating &mdash; it is consolidating, and the order books are revealing where the real demand lies.</p>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">1. Market Snapshot</h2>

<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">
<table class="data-table" style="width: 100%; border-collapse: collapse;">
<thead>
<tr style="background-color: var(--navy); color: var(--white); text-align: left;">
<th style="padding: 1rem;">Metric</th>
<th style="padding: 1rem;">Thursday 17 Sep</th>
<th style="padding: 1rem;">Friday 18 Sep</th>
<th style="padding: 1rem;">Change</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">DSEI</strong></td>
<td style="padding: 1rem;">4,632.03</td>
<td style="padding: 1rem;">4,602.26</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-29.77 pts (-0.6%)</td>
</tr>
<tr style="background-color: var(--cream);">
<td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">TSI</strong></td>
<td style="padding: 1rem;">10,220.27</td>
<td style="padding: 1rem;">10,166.24</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-54.03 pts</td>
</tr>
<tr>
<td style="padding: 1rem;">Equity Turnover</td>
<td style="padding: 1rem;">TZS 15.39 bn</td>
<td style="padding: 1rem;">TZS 4.30 bn</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-72.1%</td>
</tr>
<tr style="background-color: var(--cream);">
<td style="padding: 1rem;">Shares Traded</td>
<td style="padding: 1rem;">7,269,330</td>
<td style="padding: 1rem;">1,948,432</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-73.2%</td>
</tr>
<tr>
<td style="padding: 1rem;">Deals</td>
<td style="padding: 1rem;">3,871</td>
<td style="padding: 1rem;">3,307</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-14.6%</td>
</tr>
<tr style="background-color: var(--cream);">
<td style="padding: 1rem;">Bond Turnover</td>
<td style="padding: 1rem;">TZS 41.51 bn</td>
<td style="padding: 1rem;">TZS 0.63 bn</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-98.5%</td>
</tr>
<tr>
<td style="padding: 1rem;">ETF Turnover</td>
<td style="padding: 1rem;">TZS 113.85 mn</td>
<td style="padding: 1rem;">TZS 183.24 mn</td>
<td style="padding: 1rem; color: var(--gain); font-weight: 600;">+60.9%</td>
</tr>
<tr style="background-color: var(--cream);">
<td style="padding: 1rem;">Foreign Buying</td>
<td style="padding: 1rem;">0.60%</td>
<td style="padding: 1rem;">0.10%</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">-0.50 pts</td>
</tr>
<tr>
<td style="padding: 1rem;">Foreign Selling</td>
<td style="padding: 1rem;">5.99%</td>
<td style="padding: 1rem;">51.16%</td>
<td style="padding: 1rem; color: var(--loss); font-weight: 600;">+45.17 pts</td>
</tr>
</tbody>
</table>
</div>

<p>The session remained in the <strong>HIGH</strong> turnover regime at TZS 4.30 billion, above the TZS 3 billion threshold. While this represents a 72% decline from Thursday, it is important to remember that Thursday's figure was inflated by a single 5.45-million-share block in NMB. Friday's session was more balanced, with normal-board activity led by NMB (660,141 shares), CRDB (466,459 shares), VODA (182,415 shares), and AFRIPRISE (119,813 shares).</p>

<p>Foreign selling surged to 51.16% of turnover (TZS 2.20 billion), concentrated almost entirely in the CRDB block trade. Yet local investors absorbed the supply with ease &mdash; local buying was 99.90% of turnover. This is the pattern we have seen repeatedly: foreign institutions exit via block trades, and local capital steps forward to absorb the supply without demanding a discount.</p>

<p>The DSEI slipped 30 points to 4,602.26, while the TSI fell 54 points to 10,166.24. The decline was led by Banks, Finance & Investment (&minus;0.92%), while Commercial Services (+1.44%) outperformed on AFRIPRISE's strong gain.</p>

<p>Bond market turnover collapsed 98.5% to TZS 0.63 billion from Thursday's TZS 41.51 billion. This sharp contraction, coming alongside lower equity turnover, suggests institutions paused rather than rotated. The bond-to-equity rotation signal is not confirmed.</p>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">2. Top Movers</h2>

<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">
<table class="data-table" style="width: 100%; border-collapse: collapse;">
<thead>
<tr style="background-color: var(--navy); color: var(--white); text-align: left;">
<th style="padding: 1rem;">Ticker</th>
<th style="padding: 1rem;">Closing Price (TZS)</th>
<th style="padding: 1rem;">Change</th>
<th style="padding: 1rem;">Volume</th>
</tr>
</thead>
<tbody>
<tr><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">AFRIPRISE</strong></td><td style="padding: 1rem;">740</td><td style="padding: 1rem; color: var(--gain); font-weight: 600;">+8.8%</td><td style="padding: 1rem;">119,813</td></tr>
<tr style="background-color: var(--cream);"><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">VODA</strong></td><td style="padding: 1rem;">1,220</td><td style="padding: 1rem; color: var(--gain); font-weight: 600;">+1.6%</td><td style="padding: 1rem;">182,415</td></tr>
<tr><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">KCB</strong></td><td style="padding: 1rem;">2,190</td><td style="padding: 1rem; color: var(--gain); font-weight: 600;">+0.5%</td><td style="padding: 1rem;">17,592</td></tr>
<tr style="background-color: var(--cream);"><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">NMB</strong></td><td style="padding: 1rem;">2,070</td><td style="padding: 1rem; color: var(--loss); font-weight: 600;">-1.0%</td><td style="padding: 1rem;">660,141</td></tr>
<tr><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">CRDB</strong></td><td style="padding: 1rem;">2,810</td><td style="padding: 1rem; color: var(--loss); font-weight: 600;">-1.1%</td><td style="padding: 1rem;">846,459</td></tr>
<tr style="background-color: var(--cream);"><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">TOL</strong></td><td style="padding: 1rem;">1,790</td><td style="padding: 1rem; color: var(--loss); font-weight: 600;">-1.1%</td><td style="padding: 1rem;">4,715</td></tr>
<tr><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">DSE</strong></td><td style="padding: 1rem;">6,240</td><td style="padding: 1rem; color: var(--loss); font-weight: 600;">-1.7%</td><td style="padding: 1rem;">2,019</td></tr>
<tr style="background-color: var(--cream);"><td style="padding: 1rem; font-weight: 600;"><strong style="color: #000;">PAL</strong></td><td style="padding: 1rem;">300</td><td style="padding: 1rem; color: var(--loss); font-weight: 600;">-7.7%</td><td style="padding: 1rem;">6,520</td></tr>
</tbody>
</table>
</div>

<p><strong>AFRIPRISE</strong> was the standout performer for the second consecutive session, surging 8.8% to 740. The stock closed with 52,873 bids against 24,143 offers &mdash; a ratio of 2.2 to 1 in favour of buyers. The company's shares have now risen 22% in two sessions.</p>

<p><strong>VODA</strong> rose 1.6% to 1,220, closing with an order book showing 22,282 bids against just 2,044 offers &mdash; a ratio of 10.9 to 1. Supply has virtually evaporated. The stock has absorbed significant block trades in recent sessions and continues to attract strong demand.</p>

<p><strong>CRDB</strong> fell 1.1% to 2,810 after absorbing a 380,000-share block trade. The order book remains offer-heavy: 142,621 offers versus 103,095 bids. However, the ratio has improved from Thursday's extreme 7-to-1 to 1.4-to-1, suggesting the selling pressure is easing.</p>

<p><strong>NMB</strong> fell 1.0% to 2,070 on volume of 660,141 shares. The order book is balanced: 96,400 bids versus 123,017 offers. The ex-dividend date for the TZS 61.015 per share dividend remains pending.</p>

<p><strong>PAL</strong> was the session's worst performer, falling 7.7% to 300 on light volume.</p>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">3. In Focus: Reading Order Books &mdash; A Key Skill for Investors</h2>
<p>Friday's session provided another valuable lesson in reading order books &mdash; the lists of outstanding buy and sell orders that sit beneath every stock's price. Three stocks told very different stories through their order books at the close:</p>
<p><strong>What does this mean for everyday investors?</strong></p>
<p>When a stock closes with bids far exceeding offers &mdash; as VODA did &mdash; it means there are many more people wanting to buy than to sell. This is a strong signal of demand. The price is likely to find support and may continue to rise until supply increases.</p>
<p>When a stock closes with offers far exceeding bids &mdash; as DCB did &mdash; it means there is more supply than demand. Sellers are competing to exit, and buyers can afford to be patient. This suggests the stock may continue to drift lower until the excess supply is absorbed.</p>
<p>The lesson is simple: <strong>pay attention to the order book, not just the price.</strong> A stock that falls on heavy volume with a balanced book may be near a bottom. A stock that falls with an offer-heavy book may have further to go. A stock that rises with a bid-heavy book may have further to run.</p>

<div style="background-color: rgba(200, 150, 46, 0.05); border-left: 4px solid var(--gold); padding: 1.5rem; margin: 2rem 0; border-radius: 0 8px 8px 0;">
    <h3 style="color: var(--navy); margin-top: 0; font-family: var(--heading-font); margin-bottom: 1rem;">Understanding Price Bands</h3>
    <p style="margin-bottom: 1rem;">For the daily price band, Friday's closing prices determine Monday's limits. Because CRDB closed at 2,810, it cannot trade on Monday, 21 September, outside a band of &plusmn;5% around that level:</p>
    <ul style="margin-bottom: 1rem; color: var(--navy);">
        <li><strong>Upper limit:</strong> 2,810 &times; 1.05 = 2,950.50</li>
        <li><strong>Lower limit:</strong> 2,810 &times; 0.95 = 2,669.50</li>
    </ul>
    <p style="margin-bottom: 0;">Before placing any order, checking the previous day's close and calculating the allowed band takes only a moment. It ensures your order is executable from the second you place it, and it prevents the frustration of setting a price the market simply cannot reach that day.</p>
</div>

'''

full_html = prefix + new_body + suffix

# Fix titles and dates in prefix
full_html = full_html.replace('17th September 2026', '18th September 2026')
full_html = full_html.replace('Thursday, 18th', 'Friday, 18th') 
full_html = full_html.replace('Thursday, 17th', 'Friday, 18th')
full_html = full_html.replace('17 Sep 2026', '18 Sep 2026')
full_html = full_html.replace('dse-wrap-2026-09-17.html', 'dse-wrap-2026-09-18.html')
full_html = full_html.replace('Amana-DSE-Wrap-17-Sept.pdf', 'Amana-DSE-Wrap-18-Sept.pdf')

with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
print("Recreated dse-wrap-2026-09-18.html with proper formatting!")
