import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Terminal feed
c = re.sub(
    r'(<div class="terminal-title">DSE TERMINAL FEED // )[^<]*(</div>)',
    r'\g<1>04 SEP 2026\g<2>',
    c
)

# Gainers
gainers_repl = '''<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>KCB <span style="color:var(--gain)">+3.7%</span></span>
            <span>NMB <span style="color:var(--gain)">+3.6%</span></span>
            <span>MCB <span style="color:var(--gain)">+2.6%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-gainers"[^>]*>.*?</div>', gainers_repl, c, flags=re.DOTALL)

# Losers
losers_repl = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>VODA <span style="color:var(--loss)">-1.9%</span></span>
            <span>DSE <span style="color:var(--loss)">-1.4%</span></span>
            <span>TOL <span style="color:var(--loss)">-0.5%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-losers"[^>]*>.*?</div>', losers_repl, c, flags=re.DOTALL)

# Teaser URL
c = re.sub(
    r'(<a href=")/dse-wrap-[0-9\-]+(" class="teaser-prem-btn">)',
    r'\g<1>/dse-wrap-2026-09-04\g<2>',
    c
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed index.html")
