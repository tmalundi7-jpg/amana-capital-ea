import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''<div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <div style="background: #ffffff; border: 1px solid rgba(200, 150, 46, 0.4); padding: 1rem 1.5rem; border-radius: 6px; min-width: 200px; flex: 1;">
          <div style="font-size: 0.85rem; color: #6B7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 0.25rem;">NMB</div>
          <div style="font-size: 1.6rem; color: #0A1628; font-weight: 700;">5,451,880 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span></div>
        </div>
      </div>'''

content = re.sub(r'<div style="display: flex; gap: 1rem; flex-wrap: wrap;">.*?</div>\s*</div>\s*</div>', new_block + '\n    </div>\n', content, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(content)
