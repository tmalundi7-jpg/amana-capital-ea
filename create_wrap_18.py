import re

file_path = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\dse-wrap-2026-09-17.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update title and meta
content = content.replace('17th September 2026', '18th September 2026')
content = content.replace('Thursday, 18th', 'Friday, 18th') 
content = content.replace('Thursday, 17th', 'Friday, 18th')
content = content.replace('17 Sep 2026', '18 Sep 2026')
content = content.replace('dse-wrap-2026-09-17.html', 'dse-wrap-2026-09-18.html')
content = content.replace('Amana-DSE-Wrap-17-Sept.pdf', 'Amana-DSE-Wrap-18-Sept.pdf')

start_marker = '<div class="article-body"'
end_marker = '<div class="article-disclaimer"'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_article_body = '''<div class="article-body" style="font-size: 1.05rem; line-height: 1.8; color: var(--navy);">
<p><strong>Turnover Cools but CRDB Absorbs a 380,000-Share Block Without Flinching &mdash; Order Books Tell the Real Story</strong></p>

<p>The Dar es Salaam Stock Exchange closed the week with a session of quiet resilience. Equity turnover fell 72% to TZS 4.30 billion from Thursday's block-heavy TZS 15.39 billion, and the All-Share Index slipped 30 points. Yet beneath these headline numbers, CRDB absorbed a 380,000-share block trade and closed just 30 shillings lower. Meanwhile, VODA closed with a bid-to-offer ratio of nearly 11 to 1, and AFRIPRISE surged 8.8%. The market is not retreating &mdash; it is consolidating, and the order books are revealing where the real demand lies.</p>

<h3 style="color: var(--navy); font-family: var(--heading-font); font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem;">1. Market Snapshot</h3>
<p>The session remained in the <strong>HIGH</strong> turnover regime at TZS 4.30 billion, above the TZS 3 billion threshold. While this represents a 72% decline from Thursday, it is important to remember that Thursday's figure was inflated by a single 5.45-million-share block in NMB. Friday's session was more balanced, with normal-board activity led by NMB (660,141 shares), CRDB (466,459 shares), VODA (182,415 shares), and AFRIPRISE (119,813 shares).</p>
<p>Foreign selling surged to 51.16% of turnover (TZS 2.20 billion), concentrated almost entirely in the CRDB block trade. Yet local investors absorbed the supply with ease &mdash; local buying was 99.90% of turnover. This is the pattern we have seen repeatedly: foreign institutions exit via block trades, and local capital steps forward to absorb the supply without demanding a discount.</p>
<p>The DSEI slipped 30 points to 4,602.26, while the TSI fell 54 points to 10,166.24. The decline was led by Banks, Finance & Investment (&minus;0.92%), while Commercial Services (+1.44%) outperformed on AFRIPRISE's strong gain.</p>
<p>Bond market turnover collapsed 98.5% to TZS 0.63 billion from Thursday's TZS 41.51 billion. This sharp contraction, coming alongside lower equity turnover, suggests institutions paused rather than rotated. The bond-to-equity rotation signal is not confirmed.</p>

<h3 style="color: var(--navy); font-family: var(--heading-font); font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem;">2. Top Movers</h3>
<p><strong>Gainers:</strong> AFRIPRISE (+8.8%), VODA (+1.6%), KCB (+0.5%).<br>
<strong>Losers:</strong> PAL (&minus;7.7%), DSE (&minus;1.7%), CRDB (&minus;1.1%), TOL (&minus;1.1%), NMB (&minus;1.0%).</p>
<p><strong>AFRIPRISE</strong> was the standout performer for the second consecutive session, surging 8.8% to 740. The stock closed with 52,873 bids against 24,143 offers &mdash; a ratio of 2.2 to 1 in favour of buyers. The company's shares have now risen 22% in two sessions.</p>
<p><strong>VODA</strong> rose 1.6% to 1,220, closing with an order book showing 22,282 bids against just 2,044 offers &mdash; a ratio of 10.9 to 1. Supply has virtually evaporated. The stock has absorbed significant block trades in recent sessions and continues to attract strong demand.</p>
<p><strong>CRDB</strong> fell 1.1% to 2,810 after absorbing a 380,000-share block trade. The order book remains offer-heavy: 142,621 offers versus 103,095 bids. However, the ratio has improved from Thursday's extreme 7-to-1 to 1.4-to-1, suggesting the selling pressure is easing.</p>
<p><strong>NMB</strong> fell 1.0% to 2,070 on volume of 660,141 shares. The order book is balanced: 96,400 bids versus 123,017 offers. The ex-dividend date for the TZS 61.015 per share dividend remains pending.</p>
<p><strong>PAL</strong> was the session's worst performer, falling 7.7% to 300 on light volume.</p>

<h3 style="color: var(--navy); font-family: var(--heading-font); font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem;">3. In Focus: Reading Order Books &mdash; A Key Skill for Investors</h3>
<p>Friday's session provided another valuable lesson in reading order books &mdash; the lists of outstanding buy and sell orders that sit beneath every stock's price. Three stocks told very different stories through their order books at the close:</p>
<p><strong>What does this mean for everyday investors?</strong></p>
<p>When a stock closes with bids far exceeding offers &mdash; as VODA did &mdash; it means there are many more people wanting to buy than to sell. This is a strong signal of demand. The price is likely to find support and may continue to rise until supply increases.</p>
<p>When a stock closes with offers far exceeding bids &mdash; as DCB did &mdash; it means there is more supply than demand. Sellers are competing to exit, and buyers can afford to be patient. This suggests the stock may continue to drift lower until the excess supply is absorbed.</p>
<p>The lesson is simple: <strong>pay attention to the order book, not just the price.</strong> A stock that falls on heavy volume with a balanced book may be near a bottom. A stock that falls with an offer-heavy book may have further to go. A stock that rises with a bid-heavy book may have further to run.</p>
<p>For the daily price band, Friday's closing prices determine Monday's limits. Because CRDB closed at 2,810, it cannot trade on Monday, 21 September, outside a band of &plusmn;5% around that level:</p>
<ul>
<li><strong>Upper limit:</strong> 2,810 &times; 1.05 = 2,950.50</li>
<li><strong>Lower limit:</strong> 2,810 &times; 0.95 = 2,669.50</li>
</ul>
<p>Based on Friday's closing prices, here are the allowed trading ranges for Monday, 21 September 2026:</p>
<p><em>&lowast; DCB and MCB trade under wider 15% bands due to their sub-TZS 1,000 price levels.</em></p>
<p>Before placing any order, checking the previous day's close and calculating the allowed band takes only a moment. It ensures your order is executable from the second you place it, and it prevents the frustration of setting a price the market simply cannot reach that day.</p>
</div>
'''

    new_content = content[:start_idx] + new_article_body + content[end_idx:]
    
    with open(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\dse-wrap-2026-09-18.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Created dse-wrap-2026-09-18.html")
else:
    print(f"Failed to find markers: start={start_idx}, end={end_idx}")
