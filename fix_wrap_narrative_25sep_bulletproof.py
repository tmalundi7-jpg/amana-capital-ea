import re

with open('dse-wrap-2026-09-25.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_narrative = """
  <h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">3. Equity Market: The Institutional Pulse</h2>
  <p>The narrative that the market is "cooling" is factually incorrect. While headline turnover appears lower than the TZS 15 billion peaks seen earlier this month, the underlying dynamics point to an extremely tight market where supply has evaporated.</p>
  <p>Equity turnover rose 38.7% to TZS 3.78 billion. Deal counts rose 7.0% to 3,719. Retail participation remains robust, but institutional selling has vanished. Domestic investors accounted for 100% of all buying and 88.69% of all selling. Foreign participation remains negative but small (11.31% of selling, zero buying).</p>
  <p>The most important signal in the market right now is the bid/offer ratio on the major banking counters. When buyers outnumber sellers 19 to 1 (as seen in CRDB earlier this week) or when stocks rally with zero foreign help, the market is demonstrating severe accumulation behavior.</p>

  <h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">4. Fixed Income: The Rotation Signal</h2>
  <p>Bond turnover contracted again, falling 9.4% to TZS 18.91 billion. This marks the third consecutive session of declining fixed-income volume (from TZS 39.48 bn to TZS 20.87 bn to TZS 18.91 bn).</p>
  <p>This sequence &mdash; bond volume contracting while equity volume begins to recover &mdash; is the classic signature of an institutional pause preceding a rotation.</p>
  <p>In the 10-year maturity (11.44% coupon), TZS 18.15 billion changed hands. However, we noted a distressed sale at a 19.00% yield, alongside standard trades at 10.60%. The 25-year bond (12.56% coupon) saw a tiny TZS 0.05 billion trade at 15.65%. Yields are volatile, but the trend of lower overall volume is the key metric to watch.</p>

  <h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">5. Order Book Analysis: The Story Behind the Price</h2>
  <p><strong>CRDB:</strong> Rose 2.4% to close at a new post-split high of 2,940. Volume was 431,081 shares. The extreme 19.2x bid-to-offer imbalance seen on Thursday has normalized, but the fact that the price broke out to a new high on purely local demand is a massive signal of domestic strength.</p>
  <p><strong>VODA:</strong> Fell 0.8% to 1,280. Volume was 189,462 shares. The order book is balanced. The stock is currently undergoing pre-dividend accumulation ahead of its impending ex-dividend date.</p>
  <p><strong>NMB:</strong> Closed flat at 2,130 after absorbing a 429,000-share block trade. The ex-dividend date for the TZS 61.015 per share dividend remains pending. Caution is warranted until the ex-date is announced.</p>
  <p><strong>TCC:</strong> Closed at 13,200, remaining in its pre-dividend window. The net dividend yield remains attractive at over 7.5%.</p>
  <p><strong>TBL:</strong> Closed at 9,800; the net dividend yield is 7.93% &mdash; the highest in the market.</p>
  <p><strong>DCB:</strong> Fell 4.5% with an extremely offer-heavy book. The stock is in a downtrend; avoid.</p>

  <h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">6. Strategic Outlook</h2>
  <p><strong>Medium-Term (Q4 2026):</strong> The bond-to-equity rotation signal is building. Watch for bond turnover to remain below TZS 10 billion for two more sessions while equity turnover stays above TZS 5 billion &mdash; that would confirm the rotation. The Bank of Tanzania's monetary policy stance remains supportive. Any change in interest rates would be a major event for both bonds and equities.</p>
  <p><strong>Long-Term:</strong> The events of the past several weeks &mdash; the NMB share split, the CRDB block trades, the bond yield compression, and the foreign flow reversal &mdash; all point in the same direction: the DSE has entered a new era. Local capital is firmly in control, institutional participation is growing, and the market is demonstrating depth and resilience that would have been unthinkable a year ago. For the patient, long-term investor, this is a market that rewards discipline, education, and the willingness to let compounding work.</p>
"""

# Find start and end indices
start_idx = html.find('<p><strong>Daily DSE Wrap | ')
end_idx = html.find('<p style="font-size: 0.85rem; color: var(--mist);')

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + new_narrative + html[end_idx:]
    with open('dse-wrap-2026-09-25.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully spliced new narrative!")
else:
    print(f"Could not find indices: start={start_idx}, end={end_idx}")

