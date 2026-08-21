import re

file_path = 'market-intelligence-archive.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def old_format(date_str, url_date, title, excerpt, is_alt=False):
    bg = ' background: rgba(11,29,58,0.02);' if is_alt else ''
    return f'''                        <div class="arc-row" style="display: grid; grid-template-columns: 110px 1fr auto; align-items: center; gap: 1rem; padding: 0.9rem 1.25rem; border-bottom: 1px solid rgba(11,29,58,0.06);{bg}">
                            <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">{date_str}</div>
                            <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">{title}</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">{excerpt}</div></div>
                            <a href="/dse-wrap-2026-08-{url_date}" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
                        </div>'''

replacements = [
    old_format('21 Aug 2026', '21', 'A Quiet End to the Week as Bonds Surge and Equity Volumes Ease', 'The Dar es Salaam Stock Exchange closed Friday on a subdued note, with the All-Share Index slipping 6.91 points to 4,250.04. Government bond turnover surged to TZS 15.54 billion — the highest in over a week — as institutions rotated into fixed-income assets ahead of the weekend.', is_alt=False),
    old_format('20 Aug 2026', '20', 'Quiet Session, Block Trades, and a Textbook Pullback in DCB', 'The Dar es Salaam Stock Exchange closed Thursday on a calm note, with the All-Share Index edging up by just 1.45 points to 4,256.95. After several days of block-heavy activity, trading volumes reverted to a more normal level, as DCB gave back more than 11% after its earlier speculative surge.', is_alt=True),
    old_format('19 Aug 2026', '19', 'Market Holds Firm as Block Trades Continue and Local Investors Anchor Trading', 'The Dar es Salaam Stock Exchange extended its winning streak on Wednesday, with the All-Share Index climbing to 4,255.50. A series of pre-arranged block trades in CRDB, KCB, and the iTrust ETF lifted overall activity, while local investors absorbed continued foreign selling without flinching.', is_alt=False),
    old_format('18 Aug 2026', '18', 'Block Trades Keep Local Investors Firmly in Control', 'The Dar es Salaam Stock Exchange delivered another session of healthy, locally driven trading on Tuesday, with turnover climbing to TZS 6.84 billion. Large pre-arranged transactions in NICO and continued strong activity in DCB highlighted the depth of institutional interest, while foreign investors remained almost entirely on the sidelines. The All-Share Index eased only slightly, consolidating near its monthly high.', is_alt=True),
    old_format('17 Aug 2026', '17', 'DCB\'s Block Trade and the Power of Local Demand', 'The Dar es Salaam Stock Exchange closed Monday on a strong note, with the All-Share Index rising. A massive 760,000-share DCB block trade boosted overall activity while local investors demonstrated strong conviction at current price levels.', is_alt=False),
    old_format('14 Aug 2026', '14', 'Block Trades Lift Turnover as NMB Reaches a New High and Foreign Selling Fails to Shake the Market', 'The Dar es Salaam Stock Exchange closed the week on a strong note, with the All-Share Index rising for a second consecutive session to 4,232.85. A series of large pre-arranged block trades boosted overall activity, while NMB touched a fresh record high. Crucially, the market advanced even as foreign investors sold into the strength...', is_alt=True),
]

new_content_chunk = '\n'.join(replacements)

# Replace everything from <a class="archive-row" href="/dse-wrap-2026-08-21"> up to just before the 12 Aug entry 
pattern = re.compile(r'<a class="archive-row" href="/dse-wrap-2026-08-21">.*?</a>\s*(?=<div class="arc-row")', re.DOTALL)
content = pattern.sub(new_content_chunk + '\n                        ', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated market-intelligence-archive.html')
