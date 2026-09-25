import re
import os
import shutil

REPO = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"

def read_file(filename):
    with open(os.path.join(REPO, filename), "r", encoding="utf-8") as f:
        return f.read()

def write_file(filename, content):
    with open(os.path.join(REPO, filename), "w", encoding="utf-8") as f:
        f.write(content)

# -------------------------------------------------------------------------------------
# 1. market-intelligence.html
# -------------------------------------------------------------------------------------
mi = read_file("market-intelligence.html")

# Dates
mi = mi.replace("<strong>23 Sep 2026</strong>", "<strong>24 Sep 2026</strong>")
mi = mi.replace(">23 September 2026<", ">24 September 2026<")
# Note: we also have archive-date inside this file which will be replaced entirely

# Metrics
mi = re.sub(
    r'(<div class="snapshot-value" id="mi-dsei">)4,638\.18(</div>)',
    r'\g<1>4,658.16\g<2>',
    mi
)
mi = re.sub(
    r'(<div class="snapshot-value" id="mi-tsi">)10,309\.18(</div>)',
    r'\g<1>10,362.31\g<2>',
    mi
)
mi = re.sub(
    r'(<div class="snapshot-value" data-format-type="bn" data-tzs-value="4130000000" id="mi-turnover">)TZS 4\.13 bn(</div>)',
    r'<div class="snapshot-value" data-format-type="bn" data-tzs-value="2730000000" id="mi-turnover">TZS 2.73 bn</div>',
    mi
)

# Gainers
new_gainers = """        <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--gain)">+3.7%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NICO</span> <span style="color:var(--gain)">+3.3%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>CRDB</span> <span style="color:var(--gain)">+1.8%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+1.3%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TTP</span> <span style="color:var(--gain)">+1.2%</span></div>
        </div>"""
mi = re.sub(r'<!-- GAINERS_START -->\s*<div style="display:flex; flex-direction:column; gap:0\.15rem; width:100%;">.*?</div>\s*<!-- GAINERS_END -->', 
            f'<!-- GAINERS_START -->\n{new_gainers}\n        <!-- GAINERS_END -->', mi, flags=re.DOTALL)

# Losers
new_losers = """        <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MUCOBA</span> <span style="color:var(--loss)">-5.8%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>PAL</span> <span style="color:var(--loss)">-3.2%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>AFRIPRISE</span> <span style="color:var(--loss)">-1.9%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-1.9%</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-1.5%</span></div>
        </div>"""
mi = re.sub(r'<!-- LOSERS_START -->\s*<div style="display:flex; flex-direction:column; gap:0\.15rem; width:100%;">.*?</div>\s*<!-- LOSERS_END -->', 
            f'<!-- LOSERS_START -->\n{new_losers}\n        <!-- LOSERS_END -->', mi, flags=re.DOTALL)

# Archive Row Extraction & Replacement
old_archive_row_match = re.search(r'<a class="archive-row" href="/dse-wrap-2026-09-23">.*?</a>', mi, re.DOTALL)
old_archive_row_html = old_archive_row_match.group(0)

new_archive_row = """<a class="archive-row" href="/dse-wrap-2026-09-24">
          <div class="archive-date">24 SEP<br/>2026</div>
          <div>
            <div class="archive-badge badge-equity">Equities</div>
            <div class="archive-content-title">DSE Daily Wrap - Thursday, 24 September 2026</div>
            <div class="archive-content-excerpt">DSEI gained 19.98 pts to 4,658.16. CRDB closed at 2,870 with an extreme 19.2x bid/offer ratio. Equity and bond turnover both contracted sharply as institutions paused.</div>
          </div>
          <span class="archive-cta">Read &rarr;</span>
        </a>"""
mi = mi.replace(old_archive_row_html, new_archive_row)

mi = mi.replace("?v=20260923a", "?v=20260924a")
write_file("market-intelligence.html", mi)
print("Updated market-intelligence.html")

# -------------------------------------------------------------------------------------
# 2. market-intelligence-archive.html
# -------------------------------------------------------------------------------------
arch = read_file("market-intelligence-archive.html")

# Insert old_archive_row into archive list. But first we need to adjust its structure 
# to match the archive page's internal structure (which is slightly different)
# Wait, looking at previous archive inserts, they are often identical or use 'arc-row'.
# Let's check how the previous 23 Sep script did it or just manually craft the 23 Sep archive entry.
arch_entry_23sep = """        <div class="arc-row">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">23 Sep 2026</div>
          <div>
            <div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Wednesday, 23rd September 2026</div>
            <div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">DSEI fell 21.05 pts to 4,638.18. CRDB showed a 4.34x bid/offer ratio as foreign selling collapsed to 5.34%. Bond market absorbed TZS 39.47 billion.</div>
          </div>
          <a href="/dse-wrap-2026-09-23" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
        </div>"""

# Insert right after <div class="archive-list">
if '23 Sep 2026' not in arch and '/dse-wrap-2026-09-23' not in arch:
    arch = arch.replace('<div class="archive-list">', '<div class="archive-list">\n' + arch_entry_23sep)
arch = arch.replace("?v=20260923a", "?v=20260924a")
write_file("market-intelligence-archive.html", arch)
print("Updated market-intelligence-archive.html")

# -------------------------------------------------------------------------------------
# 3. current-prices.html
# -------------------------------------------------------------------------------------
cp = read_file("current-prices.html")
cp = cp.replace("Wednesday 23rd September 2026", "Thursday 24th September 2026")
cp = cp.replace("Pre-Arranged Board (Block Trades): NMB — 429,000 shares", "Pre-Arranged Board (Block Trades): NMB — 140,968 shares")

new_table_rows = """
            <tr><td>AFRIPRISE</td><td>African Pride</td><td>Commercial Services</td><td>775</td><td style="color: var(--red);">-1.9%</td><td>63,851</td><td>49,406,670</td></tr>
            <tr><td>CRDB</td><td>CRDB Bank</td><td>Banks & Finance</td><td>2,870</td><td style="color: var(--green);">+1.8%</td><td>450,310</td><td>1,290,687,950</td></tr>
            <tr><td>DCB</td><td>Dar es Salaam Community Bank</td><td>Banks & Finance</td><td>440</td><td style="color: var(--mist);">0.0%</td><td>28,982</td><td>12,781,730</td></tr>
            <tr><td>DSE</td><td>Dar es Salaam Stock Exchange</td><td>Commercial Services</td><td>6,170</td><td style="color: var(--green);">+1.1%</td><td>1,758</td><td>10,835,080</td></tr>
            <tr><td>KCB</td><td>KCB Group (cross-listed)</td><td>Banks & Finance</td><td>2,200</td><td style="color: var(--green);">+0.5%</td><td>18,409</td><td>40,493,440</td></tr>
            <tr><td>MBP</td><td>Maendeleo Bank</td><td>Banks & Finance</td><td>2,090</td><td style="color: var(--red);">-1.9%</td><td>6,316</td><td>13,201,060</td></tr>
            <tr><td>MCB</td><td>Mwanga Community Bank</td><td>Banks & Finance</td><td>380</td><td style="color: var(--green);">+1.3%</td><td>52,320</td><td>19,909,485</td></tr>
            <tr><td>MKCB</td><td>Mkamba Commercial Bank</td><td>Banks & Finance</td><td>3,610</td><td style="color: var(--red);">-1.4%</td><td>6,477</td><td>23,367,550</td></tr>
            <tr><td>MUCOBA</td><td>Mucoba Bank</td><td>Banks & Finance</td><td>405</td><td style="color: var(--red);">-5.8%</td><td>5,712</td><td>2,326,860</td></tr>
            <tr><td>NICO</td><td>NICO Holdings</td><td>Banks & Finance</td><td>3,740</td><td style="color: var(--green);">+3.3%</td><td>8,960</td><td>33,458,080</td></tr>
            <tr><td>NMB</td><td>NMB Bank</td><td>Banks & Finance</td><td>2,130</td><td style="color: var(--green);">+0.5%</td><td>507,230</td><td>1,076,767,410</td></tr>
            <tr><td>PAL</td><td>Pal Holdings</td><td>Industrials</td><td>305</td><td style="color: var(--red);">-3.2%</td><td>15,308</td><td>4,666,070</td></tr>
            <tr><td>SWIS</td><td>Swissport Tanzania</td><td>Commercial Services</td><td>2,530</td><td style="color: var(--red);">-1.2%</td><td>3,411</td><td>8,633,940</td></tr>
            <tr><td>TBL</td><td>Tanzania Breweries</td><td>Industrials</td><td>9,800</td><td style="color: var(--red);">-0.4%</td><td>1,583</td><td>15,538,130</td></tr>
            <tr><td>TCC</td><td>Tanga Cement</td><td>Industrials</td><td>13,170</td><td style="color: var(--mist);">0.0%</td><td>63</td><td>843,570</td></tr>
            <tr><td>TCCL</td><td>Tanzania Cigarette Company</td><td>Industrials</td><td>3,920</td><td style="color: var(--green);">+3.7%</td><td>4,166</td><td>16,328,400</td></tr>
            <tr><td>TOL</td><td>TOL Gases</td><td>Industrials</td><td>1,790</td><td style="color: var(--mist);">0.0%</td><td>9,710</td><td>17,393,540</td></tr>
            <tr><td>TPCC</td><td>Tanga Portland Cement</td><td>Industrials</td><td>5,600</td><td style="color: var(--red);">-0.9%</td><td>6,205</td><td>34,779,020</td></tr>
            <tr><td>TTP</td><td>Tatepa Public Limited Company</td><td>Commercial Services</td><td>425</td><td style="color: var(--green);">+1.2%</td><td>401</td><td>170,150</td></tr>
            <tr><td>VODA</td><td>Vodacom Tanzania</td><td>Commercial Services</td><td>1,290</td><td style="color: var(--red);">-1.5%</td><td>42,196</td><td>54,554,060</td></tr>
"""

cp = re.sub(r'<tbody>.*?</tbody>', f'<tbody>{new_table_rows}          </tbody>', cp, flags=re.DOTALL)
cp = cp.replace("?v=20260923a", "?v=20260924a")
write_file("current-prices.html", cp)
print("Updated current-prices.html")

# -------------------------------------------------------------------------------------
# 4. script.js & script.min.js (Heatmap)
# -------------------------------------------------------------------------------------
js = read_file("script.js")
jsm = read_file("script.min.js")

NEW_HEATMAP = """[
        { symbol: 'NMB',       marketCap: 2675, change:  0.5 },
        { symbol: 'TBL',       marketCap: 3200, change: -0.4 },
        { symbol: 'CRDB',      marketCap: 1515, change:  1.8 },
        { symbol: 'VODA',      marketCap: 1200, change: -1.5 },
        { symbol: 'TPCC',      marketCap:  900, change: -0.9 },
        { symbol: 'NICO',      marketCap:  700, change:  3.3 },
        { symbol: 'KCB',       marketCap:  380, change:  0.5 },
        { symbol: 'TCC',       marketCap:  340, change:  0.0 },
        { symbol: 'TCCL',      marketCap:  300, change:  3.7 },
        { symbol: 'DCB',       marketCap:  180, change:  0.0 },
        { symbol: 'MKCB',      marketCap:  150, change: -1.4 },
        { symbol: 'TOL',       marketCap:  120, change:  0.0 },
        { symbol: 'SWIS',      marketCap:  100, change: -1.2 },
        { symbol: 'AFRIPRISE', marketCap:   80, change: -1.9 },
        { symbol: 'MCB',       marketCap:   50, change:  1.3 },
        { symbol: 'PAL',       marketCap:   40, change: -3.2 },
        { symbol: 'MUCOBA',    marketCap:   20, change: -5.8 },
        { symbol: 'MBP',       marketCap:   18, change: -1.9 },
        { symbol: 'DSE',       marketCap:   16, change:  1.1 },
        { symbol: 'TTP',       marketCap:   12, change:  1.2 }
    ]"""

NEW_HEATMAP_MIN = "[{symbol:'NMB',marketCap:2675,change:0.5},{symbol:'TBL',marketCap:3200,change:-0.4},{symbol:'CRDB',marketCap:1515,change:1.8},{symbol:'VODA',marketCap:1200,change:-1.5},{symbol:'TPCC',marketCap:900,change:-0.9},{symbol:'NICO',marketCap:700,change:3.3},{symbol:'KCB',marketCap:380,change:0.5},{symbol:'TCC',marketCap:340,change:0.0},{symbol:'TCCL',marketCap:300,change:3.7},{symbol:'DCB',marketCap:180,change:0.0},{symbol:'MKCB',marketCap:150,change:-1.4},{symbol:'TOL',marketCap:120,change:0.0},{symbol:'SWIS',marketCap:100,change:-1.2},{symbol:'AFRIPRISE',marketCap:80,change:-1.9},{symbol:'MCB',marketCap:50,change:1.3},{symbol:'PAL',marketCap:40,change:-3.2},{symbol:'MUCOBA',marketCap:20,change:-5.8},{symbol:'MBP',marketCap:18,change:-1.9},{symbol:'DSE',marketCap:16,change:1.1},{symbol:'TTP',marketCap:12,change:1.2}]"

def replace_heatmap(content, new_data):
    old_start = content.rfind("[", 0, content.find("{ symbol: 'CRDB'"))
    if old_start == -1:
        old_start = content.rfind("[", 0, content.find("{symbol:'CRDB'"))
    old_end = content.find("]", old_start) + 1
    return content[:old_start] + new_data + content[old_end:]

js = replace_heatmap(js, NEW_HEATMAP)
write_file("script.js", js)
print("Updated script.js")

jsm = replace_heatmap(jsm, NEW_HEATMAP_MIN)
write_file("script.min.js", jsm)
print("Updated script.min.js")

# -------------------------------------------------------------------------------------
# 5. Create dse-wrap-2026-09-24.html
# -------------------------------------------------------------------------------------
wrap23 = read_file("dse-wrap-2026-09-23.html")
wrap24 = wrap23.replace("23 September 2026", "24 September 2026")
wrap24 = wrap24.replace("23rd September 2026", "24th September 2026")
wrap24 = wrap24.replace("23 Sep 2026", "24 Sep 2026")
wrap24 = wrap24.replace("Wednesday", "Thursday")
wrap24 = wrap24.replace("dse-wrap-2026-09-23", "dse-wrap-2026-09-24")

# Update titles and excerpt text specifically
wrap24 = re.sub(
    r'<h1 class="wrap-hero-title">.*?</h1>',
    r'<h1 class="wrap-hero-title">Institutions Pause as Equity and Bond Turnover Contract</h1>',
    wrap24
)

new_intro = """<p>The Dar es Salaam Stock Exchange delivered a quieter session on Thursday, with turnover contracting across both equity and fixed-income markets. Equity turnover fell 34.1% to TZS 2.73 billion, while bond turnover dropped 47.1% to TZS 20.87 billion. Despite the lower liquidity, the indices moved higher: the DSEI gained 19.98 points to 4,658.16, and the TSI advanced 53.13 points to 10,362.31. The order books continue to show significant underlying demand, particularly in banking stocks, even as execution volumes taper off.</p>"""
wrap24 = re.sub(r'<p>The Dar es Salaam Stock Exchange delivered a session of stark contrasts.*?</p>', new_intro, wrap24, count=1, flags=re.DOTALL)

# Update Snapshot Table
snapshot_table = """          <thead>
            <tr>
              <th>Metric</th>
              <th>Wednesday 23 Sep</th>
              <th>Thursday 24 Sep</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>DSEI</td><td>4,638.18</td><td>4,658.16</td><td class="gain">+19.98 pts (+0.4%)</td></tr>
            <tr><td>TSI</td><td>10,309.18</td><td>10,362.31</td><td class="gain">+53.13 pts</td></tr>
            <tr><td>Equity Turnover</td><td>TZS 4.13 bn</td><td>TZS 2.73 bn</td><td class="loss">-34.1%</td></tr>
            <tr><td>Shares Traded</td><td>1,918,669</td><td>1,233,368</td><td class="loss">-35.7%</td></tr>
            <tr><td>Deals</td><td>3,301</td><td>3,475</td><td class="gain">+5.3%</td></tr>
            <tr><td>Bond Turnover</td><td>TZS 39.48 bn</td><td>TZS 20.87 bn</td><td class="loss">-47.1%</td></tr>
            <tr><td>ETF Turnover</td><td>TZS 31.95 mn</td><td>TZS 77.72 mn</td><td class="gain">+143.3%</td></tr>
            <tr><td>Foreign Buying</td><td>0.00%</td><td>0.00%</td><td class="neutral">0.00 pts</td></tr>
            <tr><td>Foreign Selling</td><td>5.34%</td><td>7.91%</td><td class="loss">+2.57 pts</td></tr>
          </tbody>"""
wrap24 = re.sub(r'<thead>.*?</tbody>', snapshot_table, wrap24, flags=re.DOTALL)

# Write the file
wrap24 = wrap24.replace("?v=20260923a", "?v=20260924a")
write_file("dse-wrap-2026-09-24.html", wrap24)
print("Created dse-wrap-2026-09-24.html")

