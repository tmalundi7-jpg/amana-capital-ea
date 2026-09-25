import re
import os

REPO = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
wrap_file = os.path.join(REPO, "dse-wrap-2026-09-24.html")

with open(wrap_file, "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the narrative sections with the exact ones from the 24 Sep doc
new_narrative = """<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">3. Order Book Analysis</h2>
<p>The headline index gain of 19.98 points (DSEI) obscures the contraction in liquidity beneath the surface. For the first time in weeks, equity turnover fell below TZS 3 billion, closing at TZS 2.73 billion. This was driven by a sharp drop in block trade activity; only one block trade (NMB, 140,968 shares) was recorded on the pre-arranged board, compared to multiple massive blocks in recent sessions.</p>
<p>Despite the lower turnover, the order books for key banking counters remain overwhelmingly bid-heavy:</p>
<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
<li><strong>CRDB</strong> closed at 2,870 with an extreme 19.2x bid/offer ratio (450,310 bids vs. 23,398 offers). The stock has absorbed over 3 million shares in foreign exits over the past two weeks without declining, signaling massive domestic institutional demand.</li>
<li><strong>VODA</strong> pulled back 1.5% to 1,290. After an aggressive limit-up run, the order book has returned to balance (42,196 bids vs. 45,000 offers). The dividend expectation remains the primary catalyst here.</li>
<li><strong>NMB</strong> closed at 2,130 with an offer-heavy book (507,230 offers vs. 195,142 bids). The TZS 61.015 per share dividend is keeping sellers patient, but buyers are refusing to bid higher until the ex-dividend date is finalized.</li>
<li><strong>DCB</strong> remains heavily offered at 440 (28,982 offers, zero bids).</li>
</ul>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">4. The Fixed-Income Perspective</h2>
<p>The bond market also saw a sharp contraction, with turnover falling 47% from Wednesday's TZS 39.48 billion to TZS 20.87 billion. The activity was concentrated entirely in two tenors:</p>
<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
<li><strong>20-Year Bonds:</strong> TZS 18.00 billion traded at yields between 8.26% and 10.45%. The 8.26% print is notably low, suggesting aggressive buying by a specific institution willing to pay a premium for duration.</li>
<li><strong>25-Year Bonds:</strong> TZS 2.87 billion traded at a yield of 11.02%.</li>
</ul>
<p>The contraction in both bond and equity turnover on Thursday suggests that institutions paused across both markets rather than rotating from one to the other. The bond-to-equity rotation signal remains unconfirmed.</p>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">5. Strategic Outlook: What to Anticipate</h2>
<p><strong>Near-Term (Late September):</strong></p>
<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
<li><strong>CRDB</strong> closed at 2,870 with a 19.2x bid/offer ratio &mdash; the most bid-heavy book this quarter. The stock has absorbed multiple block trades without declining. A pullback to 2,830 or below would represent an opportunity for patient buyers.</li>
<li><strong>VODA</strong> pulled back to 1,290 with a balanced order book. The expected FY2025 dividend announcement remains the key catalyst.</li>
<li><strong>NMB</strong> closed at 2,130 with an offer-heavy order book after absorbing a 140,968-share block. The ex-dividend date for the TZS 61.015 per share dividend remains pending. Caution is warranted until the ex-date is announced.</li>
<li><strong>TCC</strong> remains in its pre-dividend window, trading at 13,170. Only 63 shares traded &mdash; the stock is illiquid at current levels.</li>
<li><strong>TBL</strong> fell to 9,800; the net dividend yield is now 7.93% &mdash; the highest in the market.</li>
</ul>
<p><strong>Medium-Term (Q4 2026):</strong></p>
<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
<li>The bond market continues to attract institutional demand, but turnover contracted sharply on Thursday. Watch for a pickup in either market as a signal of institutional activity resuming.</li>
<li>The Bank of Tanzania's monetary policy stance remains supportive. Any change in interest rates would be a major event for both bonds and equities.</li>
</ul>
<p><strong>Long-Term:</strong><br>
The events of the past several weeks &mdash; the NMB share split, the CRDB block trades, the bond yield compression, and the foreign flow reversal &mdash; all point in the same direction: the DSE has entered a new era. Local capital is firmly in control, institutional participation is growing, and the market is demonstrating depth and resilience that would have been unthinkable a year ago. For the patient, long-term investor, this is a market that rewards discipline, education, and the willingness to let compounding work.</p>

<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">6. Professional Approach: How to Use This Intelligence</h2>
<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
<li><strong>Combine the Daily Wrap with our education series.</strong> If the order-book or price-band concepts are new to you, read <a href="https://article-3-2.html/" target="_blank">Stocks, Bonds, and ETFs</a> and <a href="https://article-3-4.html/" target="_blank">Understanding Market Data</a>.</li>
<li><strong>Read the order book, not just the price.</strong> A stock that closes with bids far exceeding offers is very different from one that closes with offers far exceeding bids. The order book tells you what the price alone cannot.</li>
<li><strong>Respect the daily price bands.</strong> They are designed to keep trading orderly and prevent panic-driven moves. Always calculate the allowed range before placing an order.</li>
<li><strong>Watch for turnover patterns.</strong> When both bond and equity turnover fall together, institutions are pausing. When one rises while the other falls, a rotation may be underway.</li>
<li><strong>Don't chase volatile counters.</strong> PAL's 3.2% drop after recent gains is a reminder that sharp moves can reverse quickly.</li>
<li><strong>Think in years, not days.</strong> Daily rallies and pullbacks are part of normal market behaviour. The steady, compounding growth of well-managed companies over many years is what builds real wealth.</li>
<li><strong>Remember that all investments carry risk.</strong> Never invest money you cannot afford to lose, and always do your own research.</li>
</ul>

<div class="" style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">  <h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h3>
  <p>Thursday's session &mdash; with CRDB showing a 19.2x bid/offer ratio, the bond market contracting 47%, and equity turnover falling below TZS 3 billion for the first time in weeks &mdash; is a reminder that markets move in cycles. The extreme bid-heavy order book in CRDB tells us that demand is far stronger than supply. The contraction in bond turnover tells us that institutions paused rather than rotated. For the multi-year investor, the message is clear: this is a market that rewards patience, education, and the willingness to adapt. The opportunities are there &mdash; in CRDB's bid-heavy pause, in VODA's balanced book, in the 8.26% government bond yield that may not last &mdash; but they require discipline to capture. The crowd chases sharp moves; the wise investor reads order books, respects the price bands, and lets the market's natural rhythm do the heavy lifting.</p>
</div>"""

content = re.sub(r'<h2 style="color: var\(--navy\); margin-top: 2\.5rem; margin-bottom: 1\.5rem;">3\. Order Book Analysis</h2>.*</div>', new_narrative, content, flags=re.DOTALL)

with open(wrap_file, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed dse-wrap-2026-09-24.html narrative content")
