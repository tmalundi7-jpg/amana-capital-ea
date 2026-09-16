import re
from bs4 import BeautifulSoup

def main():
    with open('current-prices.html', 'r', encoding='utf-8') as f:
        html = f.read()

    original_soup = BeautifulSoup(html, 'html.parser')
    original_text = original_soup.get_text(separator=' ', strip=True)

    # 1. Fix block trades div
    html = html.replace('  </div>\n</div>\n    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4);',
                        '    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4);')

    # 2. Update styles
    old_style = """<style>
    .gold-grid-table {
        border-collapse: collapse !important;
    }
    .gold-grid-table th, .gold-grid-table td {
        border: 1px solid rgba(200, 150, 46, 0.4) !important;
    }
</style>"""
    
    new_style = """<style>
    /* GUARDRAIL: LOCKED DESIGN FORMAT */
    /* This design format is locked for the Current Prices page. */
    /* Any future content updates must automatically inherit these styles without altering them, */
    /* unless explicitly requested by the site owner. */
    .gold-grid-table {
        border-collapse: collapse !important;
        width: 100%;
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .gold-grid-table th {
        padding: 1.2rem 1rem;
        border-bottom: 2px solid #C8962E !important;
        background-color: rgba(200, 150, 46, 0.08) !important;
        color: #0B1D3A !important;
        text-align: left;
        font-weight: 600;
        white-space: nowrap;
    }
    .gold-grid-table td {
        padding: 1rem;
        border-bottom: 1px solid rgba(200, 150, 46, 0.15) !important;
        color: #0A1628;
        vertical-align: middle;
    }
    .gold-grid-table tbody tr:nth-child(even) {
        background-color: #FBF7F0;
    }
    .gold-grid-table tbody tr:hover {
        background-color: rgba(200, 150, 46, 0.1);
    }
    .table-responsive {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin-bottom: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(11, 29, 58, 0.05);
        border: 1px solid rgba(200, 150, 46, 0.2);
    }
    .text-right {
        text-align: right !important;
    }
    .th-right {
        text-align: right !important;
    }
</style>"""
    html = html.replace(old_style, new_style)

    # 3. Clean inline styles from table and th
    # Replace table inline style
    html = re.sub(r'<table class="data-table gold-grid-table" style="[^"]*">', '<table class="data-table gold-grid-table">', html)
    
    # Replace th inline styles
    html = re.sub(r'<th style="[^"]*">Ticker</th>', '<th>Ticker</th>', html)
    html = re.sub(r'<th style="[^"]*">Company</th>', '<th>Company</th>', html)
    html = re.sub(r'<th style="[^"]*">Sector</th>', '<th>Sector</th>', html)
    # The numeric columns should be right aligned in header too
    html = re.sub(r'<th style="[^"]*">Last Price \(TZS\)</th>', '<th class="th-right">Last Price (TZS)</th>', html)
    html = re.sub(r'<th style="[^"]*">Change \(%\)</th>', '<th class="th-right">Change (%)</th>', html)
    html = re.sub(r'<th style="[^"]*">Volume</th>', '<th class="th-right">Volume</th>', html)
    html = re.sub(r'<th style="[^"]*">Turnover \(TZS\)</th>', '<th class="th-right">Turnover (TZS)</th>', html)

    # 4. Verify no data loss
    new_soup = BeautifulSoup(html, 'html.parser')
    new_text = new_soup.get_text(separator=' ', strip=True)

    if original_text != new_text:
        print("WARNING: Text content changed!")
        print("Original:", len(original_text))
        print("New:", len(new_text))
        import sys
        sys.exit(1)
    
    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Successfully upgraded current-prices.html")

if __name__ == '__main__':
    main()
