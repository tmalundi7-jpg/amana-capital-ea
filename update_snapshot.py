import re

# File paths
index_path = 'index.html'
mi_path = 'market-intelligence.html'

# Data
dsei = '4,112.64'
tsi = '9,005.34'
turnover_home = 'TZS 5.57 bn'
turnover_mi = '5.57 bn'
timestamp = '23rd July 2026'

home_gainers = 'MBP <span style="color:var(--gain)">+4.3%</span><br>VODA <span style="color:var(--gain)">+2.5%</span><br>TBL <span style="color:var(--gain)">+1.9%</span>'
home_losers = 'MCB <span style="color:var(--loss)">-14.4%</span><br>PAL <span style="color:var(--loss)">-5.3%</span><br>MUCOBA <span style="color:var(--loss)">-3.0%</span>'

mi_gainers_html = """<div class="snapshot-mover" id="mi-gainer">MBP <span style="color:#16A34A">+4.3%</span></div>
                        <div class="snapshot-mover" id="mi-gainer">VODA <span style="color:#16A34A">+2.5%</span></div>
                        <div class="snapshot-mover" id="mi-gainer">TBL <span style="color:#16A34A">+1.9%</span></div>"""
mi_losers_html = """<div class="snapshot-mover" id="mi-loser">MCB <span style="color:#DC2626">-14.4%</span></div>
                        <div class="snapshot-mover" id="mi-loser">PAL <span style="color:#DC2626">-5.3%</span></div>
                        <div class="snapshot-mover" id="mi-loser">MUCOBA <span style="color:#DC2626">-3.0%</span></div>"""

with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

index_content = re.sub(r'(id="home-dsei">).*?(</div>)', r'\g<1>' + dsei + r'\2', index_content)
index_content = re.sub(r'(id="home-tsi">).*?(</div>)', r'\g<1>' + tsi + r'\2', index_content)
index_content = re.sub(r'(id="home-turnover">).*?(</div>)', r'\g<1>' + turnover_home + r'\2', index_content)
index_content = re.sub(r'(id="home-gainers">).*?(</div>)', r'\g<1>' + home_gainers + r'\2', index_content)
index_content = re.sub(r'(id="home-losers">).*?(</div>)', r'\g<1>' + home_losers + r'\2', index_content)
index_content = re.sub(r'(id="home-snapshot-date">).*?(</div>)', r'\g<1>End-of-day, ' + timestamp + r'. For educational purposes only.\2', index_content)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

with open(mi_path, 'r', encoding='utf-8') as f:
    mi_content = f.read()

mi_content = re.sub(r'(id="mi-dsei">).*?(</div>)', r'\g<1>' + dsei + r'\2', mi_content)
mi_content = re.sub(r'(id="mi-tsi">).*?(</div>)', r'\g<1>' + tsi + r'\2', mi_content)
mi_content = re.sub(r'(id="mi-turnover">).*?(</div>)', r'\g<1>' + turnover_mi + r'\2', mi_content)
mi_content = re.sub(r'(class="snapshot-timestamp".*?>).*?(</div>)', r'\g<1>' + timestamp + r'\2', mi_content)
mi_content = re.sub(r'(<!-- GAINERS_START -->).*?(<!-- GAINERS_END -->)', r'\1\n' + mi_gainers_html + '\n' + r'\2', mi_content, flags=re.DOTALL)
mi_content = re.sub(r'(<!-- LOSERS_START -->).*?(<!-- LOSERS_END -->)', r'\1\n' + mi_losers_html + '\n' + r'\2', mi_content, flags=re.DOTALL)

with open(mi_path, 'w', encoding='utf-8') as f:
    f.write(mi_content)

print("Files updated successfully.")
