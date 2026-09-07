with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replacements for market-intelligence.html
c = c.replace(
    '<strong>03 Sep 2026</strong>',
    '<strong>04 Sep 2026</strong>'
)

c = c.replace(
    '<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">3 September 2026</span>',
    '<span style="font-size:0.78rem;color:rgba(251,247,240,0.7);font-weight:600;">4 September 2026</span>'
)

c = c.replace(
    '<div class="snapshot-value" id="mi-dsei">4,442.62</div>',
    '<div class="snapshot-value" id="mi-dsei">4,523.81</div>'
)

c = c.replace(
    '<div class="snapshot-value" id="mi-tsi">9,653.89</div>',
    '<div class="snapshot-value" id="mi-tsi">9,826.80</div>'
)

c = c.replace(
    '<div class="snapshot-value" data-format-type="bn" data-tzs-value="4010000000" id="mi-turnover">TZS 42.93 bn</div>',
    '<div class="snapshot-value" data-format-type="bn" data-tzs-value="8180000000" id="mi-turnover">TZS 8.18 bn</div>'
)

c = c.replace(
    '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--gain)">+8.2%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMG</span> <span style="color:var(--gain)">+7.9%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.9%</span></div>',
    '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.7%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+3.6%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+2.6%</span></div>'
)

c = c.replace(
    '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--loss)">-4.0%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TTP</span> <span style="color:var(--loss)">-2.1%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.8%</span></div>',
    '<div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-1.9%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.4%</span></div>\n        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-0.5%</span></div>'
)

c = c.replace(
    '<a class="archive-row" href="/dse-wrap-2026-09-03">\n<div class="archive-date">03 Sep<br/>2026</div>\n<div>\n<div class="archive-badge badge-equity">Equities</div>\n<div class="archive-content-title">Daily DSE Wrap | Thursday, 3rd September 2026</div>\n<div class="archive-content-excerpt">The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day figure...</div>\n</div>\n<span class="archive-cta">Read &rarr;</span>\n</a>',
    '<a class="archive-row" href="/dse-wrap-2026-09-04">\n<div class="archive-date">04 Sep<br/>2026</div>\n<div>\n<div class="archive-badge badge-equity">Equities</div>\n<div class="archive-content-title">Daily DSE Wrap | Friday, 4th September 2026</div>\n<div class="archive-content-excerpt">The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion...</div>\n</div>\n<span class="archive-cta">Read &rarr;</span>\n</a>'
)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("market-intelligence.html updated")

# Now update market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc = f.read()

new_row = """<div class="arc-row">
  <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">03 Sep 2026</div>
  <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Thursday, 3rd September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day figure...</div></div>
  <a href="/dse-wrap-2026-09-03" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
  </div>
"""

arc = arc.replace(
    '<div id="archiveList" style="border: 1px solid rgba(11,29,58,0.09); border-radius: 8px; overflow: hidden; background: #fff;">\n',
    '<div id="archiveList" style="border: 1px solid rgba(11,29,58,0.09); border-radius: 8px; overflow: hidden; background: #fff;">\n' + new_row
)

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arc)

print("market-intelligence-archive.html updated")
