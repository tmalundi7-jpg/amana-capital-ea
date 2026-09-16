def update_archive():
    with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
        arch = f.read()

    arc_row_7sep = '''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">7 Sep 2026</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Monday, 7th September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">Bond money floods into equities as the rotation signal fires. Equity turnover more than doubled to TZS 17.31 billion while bond turnover collapsed to TZS 7.99 billion. The TSI crossed 10,000...</div></div>
<a href="/dse-wrap-2026-09-07" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>
'''
    
    if '<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">7 Sep 2026</div>' not in arch:
        first_arc_row_index = arch.find('<div class="arc-row">')
        if first_arc_row_index != -1:
            arch = arch[:first_arc_row_index] + arc_row_7sep + arch[first_arc_row_index:]
            with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
                f.write(arch)
            print("market-intelligence-archive.html updated.")
        else:
            print("FAIL: could not find first arc-row in archive")
    else:
        print("Archive already has 7 Sep row")

update_archive()
