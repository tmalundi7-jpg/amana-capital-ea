import re

# Fix index.html teaser
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = re.sub(
    r'<div class="teaser-date">.*?</div>',
    '<div class="teaser-date">20 July 2026</div>',
    idx_html
)
idx_html = re.sub(
    r'<h3 class="teaser-title">.*?</h3>',
    '<h3 class="teaser-title">CRDB Block Wave Subsides as VODA Block Surprises and NMB Hits a New Peak</h3>',
    idx_html
)
idx_html = re.sub(
    r'<p class="teaser-body">.*?</p>',
    r'<p class="teaser-body">The Dar es Salaam Stock Exchange opened the new week with a change of pace. After two weeks dominated by massive CRDB block trades, Monday delivered a more varied session. A large 600,000-share VODA block took centre stage, while CRDB\'s block activity shrank dramatically to just 200,000 shares - the smallest in July. The number of individual deals jumped to 3,701, the highest in over a week, showing that everyday investors and local institutions are increasingly driving the market. Meanwhile, NMB briefly surged to a new high of 17,050 before settling back.</p>',
    idx_html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)


# Fix market-intelligence.html snapshot
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi_html = f.read()

# Replace exact strings based on the 17th
mi_html = mi_html.replace('4,111.98', '4,102.83')
mi_html = mi_html.replace('8,969.32', '8,952.33')
mi_html = mi_html.replace('TZS 38.44 bn', 'TZS 4.61 bn')

mi_html = mi_html.replace(
    'MUCOBA <span style="color:var(--gain)">+7.7%</span><br>DSE <span style="color:var(--gain)">+2.8%</span><br>TCCL <span style="color:var(--gain)">+2.4%</span>',
    'DSE <span style="color:var(--gain)">+2.4%</span><br>TCCL <span style="color:var(--gain)">+0.9%</span><br>PAL <span style="color:var(--gain)">+5.4%</span>'
)

mi_html = mi_html.replace(
    'TTP <span style="color:var(--loss)">-11.1%</span><br>DCB <span style=\"color:var(--loss)\">-6.3%</span><br>MCB <span style="color:var(--loss)">-5.1%</span>',
    'TTP <span style="color:var(--loss)">-2.2%</span><br>DCB <span style="color:var(--loss)">-5.0%</span><br>MCB <span style="color:var(--loss)">-3.5%</span><br>MBP <span style="color:var(--loss)">-9.8%</span>'
)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi_html)

print("Fixed missing HTML files successfully")
