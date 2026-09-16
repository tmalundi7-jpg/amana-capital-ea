import re

html_path = 'C:\\Users\\tmalu\\.gemini\\antigravity\\scratch\\Amana-capital-ea\\current-prices.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sticky Ticker Column & 3. Table Header Border & 2. Accessible Sector Color in styles
style_mod = '''    .gold-grid-table th:nth-child(n+4), .gold-grid-table td:nth-child(n+4) {
        text-align: right !important;
    }
    .gold-grid-table td:nth-child(3) {
        color: #736B66 !important;
    }
    .gold-grid-table td:nth-child(1) {
        font-weight: 700 !important;
    }
    .gold-grid-table th:nth-child(1), .gold-grid-table td:nth-child(1) {
        position: sticky;
        left: 0;
        z-index: 10;
        background-color: #ffffff;
    }
    .gold-grid-table tbody tr:nth-child(even) td:nth-child(1) {
        background-color: #FBF7F0;
    }
    .gold-grid-table thead {
        border-bottom: 2px solid #C8962E !important;
    }'''

content = re.sub(
    r'    \.gold-grid-table th:nth-child\(n\+4\), \.gold-grid-table td:nth-child\(n\+4\) \{.*?font-weight: 700 !important;\n    \}',
    style_mod, content, flags=re.DOTALL
)

# Replace inline style for sector column
content = content.replace('<td style=\"color: #9A9490;\">', '<td style=\"color: #736B66;\">')

# 4. Accessibility tags
header_orig = '<thead><tr><th>Ticker</th><th>Company</th><th>Sector</th><th class=\"th-right\">Last Price (TZS)</th><th class=\"th-right\">Change (%)</th><th class=\"th-right\">Volume</th><th class=\"th-right\">Turnover (TZS)</th></tr></thead>'
header_new = '<thead><tr><th scope=\"col\">Ticker</th><th scope=\"col\">Company</th><th scope=\"col\">Sector</th><th scope=\"col\" class=\"th-right\">Last Price (TZS)</th><th scope=\"col\" class=\"th-right\">Change (%)</th><th scope=\"col\" class=\"th-right\">Volume</th><th scope=\"col\" class=\"th-right\">Turnover (TZS)</th></tr></thead>'
content = content.replace(header_orig, header_new)

caption_str = '<caption style=\"position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0, 0, 0, 0);\">Current DSE Prices Data</caption>'
content = content.replace('<table class=\"data-table gold-grid-table\">\n', f'<table class=\"data-table gold-grid-table\">\n{caption_str}\n')

# 5. Block Trades Refactor
block_orig = '''<div class=\"block-trades-container\" style=\"display: flex; gap: 1rem; flex-wrap: wrap;\">
    <div style=\"background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;\">
      <div style=\"font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;\">NMB</div>
      <div style=\"font-size: 1.6rem; color: #0A1628; font-weight: 700;\">4,904,282 <span style=\"font-size: 0.95rem; font-weight: 400; color: #6B7280;\">shares</span></div>
    </div>
    <div style=\"background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;\">
      <div style=\"font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;\">TCC</div>
      <div style=\"font-size: 1.6rem; color: #0A1628; font-weight: 700;\">114,000 <span style=\"font-size: 0.95rem; font-weight: 400; color: #6B7280;\">shares</span></div>
    </div>
    <div style=\"background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;\">
      <div style=\"font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;\">VODA</div>
      <div style=\"font-size: 1.6rem; color: #0A1628; font-weight: 700;\">600,000 <span style=\"font-size: 0.95rem; font-weight: 400; color: #6B7280;\">shares</span></div>
    </div>
  </div>'''

block_new = '''<div class=\"block-trades-container\">
    <div class=\"block-trade-card\">
      <div class=\"block-trade-ticker\">NMB</div>
      <div class=\"block-trade-volume\">4,904,282 <span class=\"block-trade-shares\">shares</span></div>
    </div>
    <div class=\"block-trade-card\">
      <div class=\"block-trade-ticker\">TCC</div>
      <div class=\"block-trade-volume\">114,000 <span class=\"block-trade-shares\">shares</span></div>
    </div>
    <div class=\"block-trade-card\">
      <div class=\"block-trade-ticker\">VODA</div>
      <div class=\"block-trade-volume\">600,000 <span class=\"block-trade-shares\">shares</span></div>
    </div>
  </div>'''

content = content.replace(block_orig, block_new)

# 7. Typography Cleanup
content = content.replace('<link href=\"https://fonts.googleapis.com/css2-family=Inter:wght@400;600&amp;family=Merriweather:wght@400;700&amp;display=swap\" rel=\"stylesheet\"/>', '<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;display=swap\" rel=\"stylesheet\"/>')

# 8. En-dash Correction
content = re.sub(r'change-negative\"><strong>-([0-9]+\.[0-9]+%)', r'change-negative\"><strong>–\1', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

style_path = 'C:\\Users\\tmalu\\.gemini\\antigravity\\scratch\\Amana-capital-ea\\style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    style_content = f.read()

# Append Block Trades classes to style.css
css_append = '''

/* --- Block Trades --- */
.block-trades-container {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.block-trade-card {
    background: #ffffff;
    border: 1px solid rgba(200, 150, 46, 0.4);
    padding: 1rem 1.5rem;
    border-radius: 6px;
    min-width: 200px;
    flex: 1;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.block-trade-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(200, 150, 46, 0.15);
}

.block-trade-ticker {
    font-size: 0.85rem;
    color: #6B7280;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 0.25rem;
}

.block-trade-volume {
    font-size: 1.6rem;
    color: #0A1628;
    font-weight: 700;
}

.block-trade-shares {
    font-size: 0.95rem;
    font-weight: 400;
    color: #6B7280;
}
'''
if '.block-trade-card' not in style_content:
    with open(style_path, 'a', encoding='utf-8') as f:
        f.write(css_append)
