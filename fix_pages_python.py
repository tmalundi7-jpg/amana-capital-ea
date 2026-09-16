import re

def fix_index():
    path = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 1. Update DSE Snapshot Note
    html = re.sub(r'End&#8209;of&#8209;day, Friday, 3rd July 2026', r'End&#8209;of&#8209;day, Friday, 11th September 2026', html)
    
    # 2. Update DSEI
    html = re.sub(r'(<div class="snapshot-value" id="home-dsei">).*?(</div>)', r'\g<1>4,658.31\g<2>', html)
    
    # 3. Update TSI
    html = re.sub(r'(<div class="snapshot-value" id="home-tsi">).*?(</div>)', r'\g<1>10,400.36\g<2>', html)
    
    # 4. Update Turnover
    html = re.sub(r'(<div class="snapshot-value" id="home-turnover">).*?(</div>)', r'\g<1>16.64\g<2>', html)
    
    # 5. Update Gainers
    gainers_html = 'CRDB <span style="color:var(--gain)">+2.1%</span><br>TCC <span style="color:var(--gain)">+1.4%</span><br>KCB <span style="color:var(--gain)">+1.0%</span>'
    html = re.sub(r'(<div class="snapshot-mover" id="home-gainers">).*?(</div>)', r'\1' + gainers_html + r'\2', html)
    
    # 6. Update Losers
    losers_html = 'TOL <span style="color:var(--loss)">-3.8%</span><br>SWIS <span style="color:var(--loss)">-2.5%</span><br>MBP <span style="color:var(--loss)">-1.9%</span>'
    html = re.sub(r'(<div class="snapshot-mover" id="home-losers">).*?(</div>)', r'\1' + losers_html + r'\2', html)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixed index.html")

def fix_mi():
    path = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\market-intelligence.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 1. Update DSEI
    html = re.sub(r'(<div class="snapshot-value" id="mi-dsei">).*?(</div>)', r'\g<1>4,658.31\g<2>', html)
    
    # 2. Update TSI
    html = re.sub(r'(<div class="snapshot-value" id="mi-tsi">).*?(</div>)', r'\g<1>10,400.36\g<2>', html)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixed market-intelligence.html")

try:
    fix_index()
    fix_mi()
except Exception as e:
    print(e)
