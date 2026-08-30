import re
import glob

new_footer = '''<footer class="footer" style="background-color: var(--navy); padding: 3rem 0 2rem; border-top: 1px solid rgba(255,255,255,0.05);">
  <div class="container" style="display: flex; flex-direction: column; align-items: center; gap: 1.5rem; text-align: center;">
    <div>
      <div style="font-family: 'Cormorant Garamond', serif; color: var(--gold); font-weight: 600; letter-spacing: 2px; font-size: 1.15rem; margin-bottom: 0.4rem; text-transform: uppercase;">AMANA CAPITAL EAST AFRICA</div>
      <div style="color: rgba(251,247,240,0.5); font-size: 0.8rem; letter-spacing: 0.5px;">Dar es Salaam &middot; Tanzania &middot; Registration Pending CMSA</div>
    </div>
    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: center; margin: 0.5rem 0;">
      <a href="/market-intelligence" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Research</a>
      <a href="/bond-calculator" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Bond Calc</a>
      <a href="/compound-wealth" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Wealth Modeler</a>
      <a href="/education" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Education</a>
      <a href="/about" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Governance</a>
      <a href="/contact" style="color: var(--mist); text-decoration: none; font-size:0.85rem; transition: color 0.2s;">Contact</a>
    </div>
    <div style="color: var(--mist); opacity: 0.45; font-size:0.75rem;">&copy; 2026 Amana Capital East Africa Limited</div>
  </div>
</footer>'''

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace footer
    content = re.sub(r'<footer class="footer".*?</footer>', new_footer, content, flags=re.DOTALL)

    # Bump cache
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_11', content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated footer successfully')
