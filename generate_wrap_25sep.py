import re
import shutil

source_html = 'dse-wrap-2026-09-24.html'
target_html = 'dse-wrap-2026-09-25.html'
shutil.copy(source_html, target_html)

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title and Dates
html = re.sub(r'Thursday, 24th September 2026', 'Friday, 25th September 2026', html)
html = re.sub(r'24 Sep 2026', '25 Sep 2026', html)
html = html.replace('dse-wrap-2026-09-24', 'dse-wrap-2026-09-25')

# 2. Update Subtitle and Teaser
subtitle = "Local Capital in Control as CRDB Hits Post-Split High"
teaser = "The DSE has entered a new era. Local capital is firmly in control as CRDB hits a post-split high of 2,940, pushing the DSEI to 4,682.13 while bond turnover contracts for the third consecutive session."

html = re.sub(r'<h2 class="wrap-subtitle">.*?</h2>', f'<h2 class="wrap-subtitle">{subtitle}</h2>', html, flags=re.DOTALL)
html = re.sub(r'<p class="wrap-teaser">.*?</p>', f'<p class="wrap-teaser">{teaser}</p>', html, flags=re.DOTALL)

# 3. Update Snapshot Table Header
html = html.replace('<th>Wednesday 23 Sep</th>', '<th>Thursday 24 Sep</th>')
html = html.replace('<th>Thursday 24 Sep</th>', '<th>Friday 25 Sep</th>')

# 4. Update Snapshot Table Values
# We need to replace the specific row data
def replace_row(html, label, old_prev, old_curr, old_chg, new_prev, new_curr, new_chg, chg_class):
    # This is a bit tricky due to regex, so we'll do literal replacements if possible,
    # or just regex on the TD contents.
    pattern = rf'<td><strong>{label}</strong></td>\s*<td>{re.escape(old_prev)}</td>\s*<td>{re.escape(old_curr)}</td>\s*<td class="[^"]*">{re.escape(old_chg)}</td>'
    replacement = f'<td><strong>{label}</strong></td>\n                <td>{new_prev}</td>\n                <td>{new_curr}</td>\n                <td class="{chg_class}">{new_chg}</td>'
    return re.sub(pattern, replacement, html, flags=re.DOTALL)

html = replace_row(html, 'DSEI', '4,638.18', '4,658.16', '+19.98 pts (+0.4%)', '4,658.16', '4,682.13', '+23.97 pts (+0.5%)', 'text-gain')
html = replace_row(html, 'TSI', '10,309.18', '10,362.31', '+53.13 pts', '10,362.31', '10,419.49', '+57.18 pts', 'text-gain')
html = replace_row(html, 'Equity Turnover', 'TZS 4.13 bn', 'TZS 2.73 bn', '−34.1%', 'TZS 2.73 bn', 'TZS 3.78 bn', '+38.7%', 'text-gain')
html = replace_row(html, 'Shares Traded', '1,918,879', '1,233,368', '−35.7%', '1,233,368', '1,808,516', '+46.6%', 'text-gain')
html = replace_row(html, 'Deals', '3,300', '3,475', '+5.3%', '3,475', '3,719', '+7.0%', 'text-gain')
html = replace_row(html, 'Bond Turnover', 'TZS 39.48 bn', 'TZS 20.87 bn', '−47.1%', 'TZS 20.87 bn', 'TZS 18.91 bn', '−9.4%', 'text-loss')
html = replace_row(html, 'ETF Turnover', 'TZS 100.50 mn', 'TZS 77.72 mn', '−22.6%', 'TZS 77.72 mn', 'TZS 55.97 mn', '−28.0%', 'text-loss')
html = replace_row(html, 'Foreign Buying', '0.00%', '0.00%', '0.00 pts', '0.00%', '0.00%', '0.00 pts', 'text-neutral')
html = replace_row(html, 'Foreign Selling', '5.34%', '7.91%', '+2.57 pts', '7.91%', '11.31%', '+3.40 pts', 'text-loss')

# 5. Update Top Movers
gainers_html = """
        <div class="movers-col">
            <h4 class="movers-title">Gainers</h4>
            <ul class="movers-list">
                <li><span class="ticker">MUCOBA</span> <span class="price">450</span> <span class="change text-gain">+11.1%</span> <span class="volume">356</span></li>
                <li><span class="ticker">MBP</span> <span class="price">2,150</span> <span class="change text-gain">+2.9%</span> <span class="volume">5,467</span></li>
                <li><span class="ticker">CRDB</span> <span class="price">2,940</span> <span class="change text-gain">+2.4%</span> <span class="volume">431,081</span></li>
            </ul>
        </div>
"""
losers_html = """
        <div class="movers-col">
            <h4 class="movers-title">Losers</h4>
            <ul class="movers-list">
                <li><span class="ticker">DCB</span> <span class="price">420</span> <span class="change text-loss">-4.5%</span> <span class="volume">106,635</span></li>
                <li><span class="ticker">NICO</span> <span class="price">3,610</span> <span class="change text-loss">-3.5%</span> <span class="volume">31,545</span></li>
                <li><span class="ticker">TCCL</span> <span class="price">3,810</span> <span class="change text-loss">-2.8%</span> <span class="volume">5,670</span></li>
            </ul>
        </div>
"""
# Replace the columns
html = re.sub(r'<div class="movers-col">\s*<h4 class="movers-title">Gainers</h4>.*?</div>', gainers_html.strip(), html, flags=re.DOTALL, count=1)
html = re.sub(r'<div class="movers-col">\s*<h4 class="movers-title">Losers</h4>.*?</div>', losers_html.strip(), html, flags=re.DOTALL, count=1)

# Heatmap changes
# We just need to update VODA, CRDB, NMB, TBL, TCC to the new ones mentioned or just general
others_html = """
        <div class="movers-col">
            <h4 class="movers-title">Heatmap</h4>
            <ul class="movers-list">
                <li><span class="ticker">NMB</span> <span class="price">2,130</span> <span class="change text-neutral">0.0%</span> <span class="volume">859,775</span></li>
                <li><span class="ticker">VODA</span> <span class="price">1,280</span> <span class="change text-loss">-0.8%</span> <span class="volume">189,462</span></li>
                <li><span class="ticker">AFRIPRISE</span> <span class="price">780</span> <span class="change text-gain">+0.6%</span> <span class="volume">90,355</span></li>
                <li><span class="ticker">TPCC</span> <span class="price">5,700</span> <span class="change text-gain">+1.8%</span> <span class="volume">1,253</span></li>
            </ul>
        </div>
"""
html = re.sub(r'<div class="movers-col">\s*<h4 class="movers-title">Heatmap</h4>.*?</div>', others_html.strip(), html, flags=re.DOTALL, count=1)

# 6. Replace Narrative Content
narrative_html = """
    <div class="wrap-section">
        <h3>Equity Market: The Institutional Pulse</h3>
        <p>The narrative that the market is "cooling" is factually incorrect. While headline turnover appears lower than the TZS 15 billion peaks seen earlier this month, the underlying dynamics point to an extremely tight market where supply has evaporated.</p>
        <p>Equity turnover rose 38.7% to TZS 3.78 billion. Deal counts rose 7.0% to 3,719. Retail participation remains robust, but institutional selling has vanished. Domestic investors accounted for 100% of all buying and 88.69% of all selling. Foreign participation remains negative but small (11.31% of selling, zero buying).</p>
        <p>The most important signal in the market right now is the bid/offer ratio on the major banking counters. When buyers outnumber sellers 19 to 1 (as seen in CRDB earlier this week) or when stocks rally with zero foreign help, the market is demonstrating severe accumulation behavior.</p>
    </div>

    <div class="wrap-section">
        <h3>Fixed Income: The Rotation Signal</h3>
        <p>Bond turnover contracted again, falling 9.4% to TZS 18.91 billion. This marks the third consecutive session of declining fixed-income volume (from TZS 39.48 bn to TZS 20.87 bn to TZS 18.91 bn).</p>
        <p>This sequence &mdash; bond volume contracting while equity volume begins to recover &mdash; is the classic signature of an institutional pause preceding a rotation.</p>
        <p>In the 10-year maturity (11.44% coupon), TZS 18.15 billion changed hands. However, we noted a distressed sale at a 19.00% yield, alongside standard trades at 10.60%. The 25-year bond (12.56% coupon) saw a tiny TZS 0.05 billion trade at 15.65%. Yields are volatile, but the trend of lower overall volume is the key metric to watch.</p>
    </div>

    <div class="wrap-section">
        <h3>Order Book Analysis: The Story Behind the Price</h3>
        <ul>
            <li><strong>CRDB:</strong> Rose 2.4% to close at a new post-split high of 2,940. Volume was 431,081 shares. The extreme 19.2x bid-to-offer imbalance seen on Thursday has normalized, but the fact that the price broke out to a new high on purely local demand is a massive signal of domestic strength.</li>
            <li><strong>VODA:</strong> Fell 0.8% to 1,280. Volume was 189,462 shares. The order book is balanced. The stock is currently undergoing pre-dividend accumulation ahead of its impending ex-dividend date.</li>
            <li><strong>NMB:</strong> Closed flat at 2,130 after absorbing a 429,000-share block trade. The ex-dividend date for the TZS 61.015 per share dividend remains pending. Caution is warranted until the ex-date is announced.</li>
            <li><strong>TCC:</strong> Closed at 13,200, remaining in its pre-dividend window. The net dividend yield remains attractive at over 7.5%.</li>
            <li><strong>TBL:</strong> Closed at 9,800; the net dividend yield is 7.93% &mdash; the highest in the market.</li>
            <li><strong>DCB:</strong> Fell 4.5% with an extremely offer-heavy book. The stock is in a downtrend; avoid.</li>
        </ul>
    </div>

    <div class="wrap-section">
        <h3>Strategic Outlook</h3>
        <p><strong>Medium-Term (Q4 2026):</strong> The bond-to-equity rotation signal is building. Watch for bond turnover to remain below TZS 10 billion for two more sessions while equity turnover stays above TZS 5 billion &mdash; that would confirm the rotation. The Bank of Tanzania's monetary policy stance remains supportive. Any change in interest rates would be a major event for both bonds and equities.</p>
        <p><strong>Long-Term:</strong> The events of the past several weeks &mdash; the NMB share split, the CRDB block trades, the bond yield compression, and the foreign flow reversal &mdash; all point in the same direction: the DSE has entered a new era. Local capital is firmly in control, institutional participation is growing, and the market is demonstrating depth and resilience that would have been unthinkable a year ago. For the patient, long-term investor, this is a market that rewards discipline, education, and the willingness to let compounding work.</p>
    </div>
"""

# Replace everything inside <div class="wrap-content">...</div> except the snapshot and movers which we already replaced manually above!
# Actually, wait, the snapshot and movers are inside <div class="wrap-content">. Let's find the sections using regex.
# <div class="wrap-section">...</div>
html = re.sub(r'<div class="wrap-section">.*?</div>\s*<div class="wrap-section">.*?</div>\s*<div class="wrap-section">.*?</div>\s*<div class="wrap-section">.*?</div>', narrative_html.strip(), html, flags=re.DOTALL, count=1)

# Write to file
with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Created {target_html}")
