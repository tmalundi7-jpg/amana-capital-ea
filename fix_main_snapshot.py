import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the main snapshot gainers
new_gainers = '''<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>SWIS <span style="color:var(--gain)">+5.1%</span></span>
            <span>NICO <span style="color:var(--gain)">+3.6%</span></span>
            <span>KCB <span style="color:var(--gain)">+3.5%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-gainers".*?</div>', new_gainers, c, flags=re.DOTALL)

# Fix the main snapshot losers
new_losers = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>NMB <span style="color:var(--loss)">-2.5%</span></span>
            <span>MBP <span style="color:var(--loss)">-2.1%</span></span>
            <span>PAL <span style="color:var(--loss)">-1.6%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-losers".*?</div>', new_losers, c, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed main snapshot gainers and losers!")
