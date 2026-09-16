import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace date
c = re.sub(r'Monday, 7th September 2026', 'Wednesday, 9th September 2026', c)

old_blocks = '''<div style="display: flex; gap: 1rem; flex-wrap: wrap;">
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">CRDB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">3,193,022 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">KCB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">500,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">1,051,811 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
    <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
      <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">IEACLC-ETF</div>
      <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">809,952 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
    </div>
  </div>'''

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

c = c.replace(old_blocks, new_blocks)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Replaced block safely')
