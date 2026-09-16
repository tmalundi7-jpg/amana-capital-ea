import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Invisible Figures (Cream/Black Contrast Bug)
html = html.replace('color: #0A1628;', 'color: #0A1628 !important;')

# 3. Sector Column Contrast Failure
html = html.replace('color: #9A9490;', 'color: #5C544D;')
html = html.replace('color: #9A9490 !important;', 'color: #5C544D !important;')

# 4. Missing Table Semantics
html = html.replace('<th>Ticker</th>', '<th scope="col">Ticker</th>')
html = html.replace('<th>Company</th>', '<th scope="col">Company</th>')
html = html.replace('<th>Sector</th>', '<th scope="col">Sector</th>')
html = html.replace('<th class="th-right">Last Price (TZS)</th>', '<th scope="col" class="th-right">Last Price (TZS)</th>')
html = html.replace('<th class="th-right">Change (%)</th>', '<th scope="col" class="th-right">Change (%)</th>')
html = html.replace('<th class="th-right">Volume</th>', '<th scope="col" class="th-right">Volume</th>')
html = html.replace('<th class="th-right">Turnover (TZS)</th>', '<th scope="col" class="th-right">Turnover (TZS)</th>')

if '<caption>' not in html:
    html = html.replace('<table class="data-table gold-grid-table">',
                        '<table class="data-table gold-grid-table">\n<caption style="position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0;">DSE End of Day Current Prices</caption>')

# 5 & 6. Broken Google Fonts URL & Missing Cormorant Garamond
old_font = '<link href="https://fonts.googleapis.com/css2-family=Inter:wght@400;600&amp;family=Merriweather:wght@400;700&amp;display=swap" rel="stylesheet"/>'
new_font = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;family=Cormorant+Garamond:wght@400;600;700&amp;display=swap" rel="stylesheet"/>'
html = html.replace(old_font, new_font)

# 7. Typographical Hyphens
html = re.sub(r'>-(?=\d)', '>\u2013', html)

# 8. Corrupted Characters on Mobile
html = html.replace("content: '+? Swipe to scroll +'';", "content: '\\\\2194  Swipe to scroll  \\\\2194';")

# 9. No Sticky Ticker Column
sticky_css = '''
    /* Sticky Ticker Column */
    .gold-grid-table th:first-child,
    .gold-grid-table td:first-child {
        position: sticky !important;
        left: 0;
        background-color: inherit !important;
        z-index: 2;
        border-right: 2px solid rgba(11, 29, 58, 0.1) !important;
    }
    .gold-grid-table th:first-child {
        z-index: 3;
        background-color: #F8F1E5 !important;
    }
'''
if '/* Sticky Ticker Column */' not in html:
    html = html.replace('/* Lock structural formatting */', sticky_css + '\n    /* Lock structural formatting */')

# 10. Inline Styles on Block Trades
block_css = '''
    /* Block Trades Styling */
    .block-trades-container {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .block-trade-card {
        flex: 1;
        min-width: 200px;
        background: #ffffff;
        border: 1px solid rgba(200, 150, 46, 0.3);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(11, 29, 58, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .block-trade-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(11, 29, 58, 0.08);
        border-color: rgba(200, 150, 46, 0.6);
    }
    .block-trade-ticker {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #5C544D;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }
    .block-trade-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #0A1628 !important;
    }
    .block-trade-shares {
        font-size: 0.95rem;
        font-weight: 400;
        color: #6B7280;
    }
    .block-trade-price {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #16A34A;
        font-weight: 600;
        margin-top: 0.25rem;
    }
'''
if '/* Block Trades Styling */' not in html:
    html = html.replace('/* GUARDRAIL: LOCKED MOBILE DISPLAY */', block_css + '\n    /* GUARDRAIL: LOCKED MOBILE DISPLAY */')

# Use regex to find and replace the inline block trades
container_regex = re.compile(r'<div class="block-trades-container" style=".*?">')
html = container_regex.sub('<div class="block-trades-container">', html)

card_regex = re.compile(r'<div style="background: #ffffff; border: 1px solid rgba\(200, 150, 46, 0\.4\); padding: 1rem 1\.5rem; border-radius: 6px; min-width: 200px; flex: 1;">\s*<div style="font-size: 0\.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0\.5px; margin-bottom: 0\.25rem;">(.*?)</div>\s*<div style="font-size: 1\.6rem; color: #0A1628; font-weight: 700;">(.*?) <span style="font-size: 0\.95rem; font-weight: 400; color: #6B7280;">shares</span></div>\s*</div>', re.DOTALL)

def replace_card(match):
    ticker = match.group(1)
    shares = match.group(2)
    return f'<div class="block-trade-card">\\n<div class="block-trade-ticker">{ticker}</div>\\n<div class="block-trade-value">{shares} <span class="block-trade-shares">shares</span></div>\\n</div>'

html = card_regex.sub(replace_card, html)

# 11. Misleading Navbar State
html = html.replace('<li><a class="active" href="/market-intelligence">Market Intelligence</a></li>', '<li><a href="/market-intelligence">Market Intelligence</a></li>')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("current-prices.html updated successfully")
