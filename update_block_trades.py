import re

def update_block_trades():
    with open('current-prices.html', 'r', encoding='utf-8') as f:
        html = f.read()

    block_trades_new = '''<div style="display: flex; gap: 1rem; flex-wrap: wrap;">
      <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
        <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
        <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">500,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
      </div>
      <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
        <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">IEACLC-ETF</div>
        <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">175,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
      </div>
    </div>'''

    pattern = r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>\s*</div>\s*<div class="table-responsive">'
    
    html = re.sub(pattern, block_trades_new + '\n  </div>\n  \n  <div class="table-responsive">', html, count=1, flags=re.DOTALL)

    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Block trades updated.")

update_block_trades()
