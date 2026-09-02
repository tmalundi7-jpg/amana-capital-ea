import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix Turnover
c = c.replace('TZS 16.39 bn', 'TZS 4.01 bn')

# Fix Gainers
old_gainers = '''<span>DCB <span style="color:var(--gain)">+3.2%</span></span>
            <span>TOL <span style="color:var(--gain)">+2.2%</span></span>
            <span>DSE <span style="color:var(--gain)">+1.2%</span></span>'''
new_gainers = '''<span>SWIS <span style="color:var(--gain)">+5.1%</span></span>
            <span>NICO <span style="color:var(--gain)">+3.6%</span></span>
            <span>KCB <span style="color:var(--gain)">+3.5%</span></span>'''
c = c.replace(old_gainers, new_gainers)

# Fix Losers
old_losers = '''<span>NMB <span style="color:var(--loss)">-3.7%</span></span>
            <span>TICL <span style="color:var(--loss)">-2.6%</span></span>
            <span>CRDB <span style="color:var(--loss)">-1.8%</span></span>'''
new_losers = '''<span>NMB <span style="color:var(--loss)">-2.5%</span></span>
            <span>MBP <span style="color:var(--loss)">-2.1%</span></span>
            <span>PAL <span style="color:var(--loss)">-1.6%</span></span>'''
c = c.replace(old_losers, new_losers)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed index.html!")
