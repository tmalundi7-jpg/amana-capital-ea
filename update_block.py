import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Define the new block trades HTML
new_blocks = '''<div style="display: flex; gap: 1rem; flex-wrap: wrap;">
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">KCB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">500,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">639,435 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">TCCL</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">127,058 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">IEACLC-ETF</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">351,927 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
  </div>'''

c = re.sub(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>\s*</div>', new_blocks + '\n</div>\n', c, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)
