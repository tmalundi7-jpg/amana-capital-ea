import re
import glob

# 1. Update Gainers/Losers layout on market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

# Top Gainers Replacement
mi_gainers_old = '''<div style="display:flex; flex-direction:column; gap:0.25rem;">
      <div style="font-size:0.85rem; font-weight:700; color:var(--white);">NMG <span 
style="color:var(--gain)">+5.8%</span></div>
      <div style="font-size:0.85rem; font-weight:700; color:var(--white);">NMB <span 
style="color:var(--gain)">+4.9%</span></div>
      <div style="font-size:0.85rem; font-weight:700; color:var(--white);">VODA <span 
style="color:var(--gain)">+1.9%</span></div>
    </div>'''
mi_gainers_new = '''<div style="display:flex; flex-direction:column; gap:0.25rem; width:100%;">
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
    </div>'''
# Replace linebreaks to ensure it matches
mi_gainers_old_regex = r'<div style="display:flex; flex-direction:column; gap:0.25rem;">\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">NMG <span\s*style="color:var\(--gain\)">\+5.8%</span></div>\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">NMB <span\s*style="color:var\(--gain\)">\+4.9%</span></div>\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">VODA <span\s*style="color:var\(--gain\)">\+1.9%</span></div>\s*</div>'
mi = re.sub(mi_gainers_old_regex, mi_gainers_new, mi)

# Top Losers Replacement
mi_losers_old_regex = r'<div style="display:flex; flex-direction:column; gap:0.25rem;">\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">TOL <span\s*style="color:var\(--loss\)">-6.6%</span></div>\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">MBP <span\s*style="color:var\(--loss\)">-4.8%</span></div>\s*<div style="font-size:0.85rem; font-weight:700; color:var(--white);">SWIS <span\s*style="color:var\(--loss\)">-1.6%</span></div>\s*</div>'
mi_losers_new = '''<div style="display:flex; flex-direction:column; gap:0.25rem; width:100%;">
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
      <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
    </div>'''
mi = re.sub(mi_losers_old_regex, mi_losers_new, mi)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi)

# 2. Update Gainers/Losers layout on index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx_gainers_regex = r'<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>NMG\s*<span style="color:var\(--gain\)">\+5.8%</span></span><span>NMB <span\s*style="color:var\(--gain\)">\+4.9%</span></span><span>VODA <span style="color:var\(--gain\)">\+1.9%</span></span></div>'
idx_gainers_new = '''<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem; width:100%;">
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+5.8%</span></div>
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+4.9%</span></div>
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+1.9%</span></div>
</div>'''
idx = re.sub(idx_gainers_regex, idx_gainers_new, idx)

idx_losers_regex = r'<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;"><span>TOL\s*<span style="color:var\(--loss\)">[\-]*"?6.6%</span></span><span>MBP <span\s*style="color:var\(--loss\)">[\-]*"?4.8%</span></span><span>SWIS <span style="color:var\(--loss\)">[\-]*"?1.6%</span></span></div>'
idx_losers_new = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem; width:100%;">
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-6.6%</span></div>
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-4.8%</span></div>
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.6%</span></div>
</div>'''
idx = re.sub(idx_losers_regex, idx_losers_new, idx)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# 3. Update style.css to make mini-snapshot identical to main snapshot
css_updates = """
/* --- DAILY DSE WRAP MINI-SNAPSHOT EXACT MATCH --- */
.teaser-prem-stat, .teaser-prem-stats > div {
    background-color: var(--navy) !important; /* Made identical to main snapshot */
    border: 1px solid rgba(200,150,46,0.3) !important;
    border-top: 3px solid var(--gold) !important;
    padding: 1.25rem !important; /* Matched padding */
    border-radius: 4px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}
.teaser-prem-stat-label {
    min-height: 24px !important; /* Forces alignment */
    display: flex !important;
    align-items: flex-end !important;
    color: var(--gold) !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-weight: 700 !important;
}
.teaser-prem-stat-value {
    font-size: 1.4rem !important;
    color: var(--cream) !important;
}
/* Ensure the +5.8% gain tag looks like a two-column row inside the mini-snapshot */
.teaser-prem-stat-value.gain {
    width: 100% !important;
    display: flex !important;
    justify-content: space-between !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: var(--cream) !important;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_updates)

# 4. Bump Cache
html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_21', c2)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c2)

print("Upgrades complete")
