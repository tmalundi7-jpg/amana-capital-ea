import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    # Date in snapshot
    c = re.sub(r'(<span style="font-size:0.78rem;color:rgba\(251,247,240,0.7\);font-weight:600;">).*?(</span>)', r'\g<1>2 September 2026\g<2>', c)
    c = re.sub(r'(End-of-day &middot; ).*?(</span>)', r'\g<1>2 September 2026\g<2>', c)

    # Values
    c = re.sub(r'(<div class="snapshot-value" id="home-dsei">).*?(</div>)', r'\g<1>4,415.49\g<2>', c)
    c = re.sub(r'(<div class="snapshot-value" id="home-tsi">).*?(</div>)', r'\g<1>9,699.66\g<2>', c)
    c = re.sub(r'(<div class="snapshot-value" data-format-type="bn" data-tzs-value=").*?(" id="home-turnover">).*?(</div>)', r'\g<1>4010000000\g<2>TZS 4.01 bn\g<3>', c)

    c = re.sub(r'(<div class="snapshot-value" id="mi-dsei">).*?(</div>)', r'\g<1>4,415.49\g<2>', c)
    c = re.sub(r'(<div class="snapshot-value" id="mi-tsi">).*?(</div>)', r'\g<1>9,699.66\g<2>', c)
    c = re.sub(r'(<div class="snapshot-value" data-format-type="bn" data-tzs-value=").*?(" id="mi-turnover">).*?(</div>)', r'\g<1>4010000000\g<2>TZS 4.01 bn\g<3>', c)

    # Gainers & Losers
    gainers_html = '''<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--gain)">+5.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NICO</span> <span style="color:var(--gain)">+3.6%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.5%</span></div>'''
    
    losers_html = '''<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--loss)">-2.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--loss)">-2.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>PAL</span> <span style="color:var(--loss)">-1.6%</span></div>'''

    c = re.sub(r'(<!-- GAINERS_START -->\s*<div.*?>).*?(</div>\s*<!-- GAINERS_END -->)', r'\g<1>\n        ' + gainers_html + r'\n      \g<2>', c, flags=re.DOTALL)
    c = re.sub(r'(<!-- LOSERS_START -->\s*<div.*?>).*?(</div>\s*<!-- LOSERS_END -->)', r'\g<1>\n        ' + losers_html + r'\n      \g<2>', c, flags=re.DOTALL)

    if filename == 'index.html':
        c = re.sub(r'(<div class="mi-hero-meta">\s*<strong>).*?(</strong>)', r'\g<1>02 Sep 2026\g<2>', c)
        c = re.sub(r'(<div class="archive-date">).*?(<br/>2026</div>)', r'\g<1>02 Sep\g<2>', c)
        c = re.sub(r'(<div class="archive-content-title">)Daily DSE Wrap.*?</div>', r'\g<1>Daily DSE Wrap | Wednesday, 2nd September 2026</div>', c)
        c = re.sub(r'(<div class="archive-content-excerpt">).*?</div>', r'\g<1>The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion...</div>', c)
        c = re.sub(r'href="/dse-wrap-2026-09-01"', 'href="/dse-wrap-2026-09-02"', c)

    if filename == 'market-intelligence.html':
        c = re.sub(r'(<div class="mi-hero-meta">\s*<strong>).*?(</strong>)', r'\g<1>02 Sep 2026\g<2>', c)
        
        # We need to PREPEND the new wrap to the archive-list and REMOVE the 01 Sep one, because we only keep ONE there according to user's last request!
        # Actually wait, the user said "remove 31 Aug from below 01 Sep". 
        # So I will replace the 01 Sep entry entirely with 02 Sep.
        c = re.sub(r'(<div class="archive-date">).*?(<br/>2026</div>)', r'\g<1>02 Sep\g<2>', c)
        c = re.sub(r'(<div class="archive-content-title">)Daily DSE Wrap.*?</div>', r'\g<1>Daily DSE Wrap | Wednesday, 2nd September 2026</div>', c)
        c = re.sub(r'(<div class="archive-content-excerpt">).*?</div>', r'\g<1>The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion...</div>', c)
        c = re.sub(r'href="/dse-wrap-2026-09-01"', 'href="/dse-wrap-2026-09-02"', c)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(c)

update_file('index.html')
update_file('market-intelligence.html')
print("Updated index.html and market-intelligence.html")
