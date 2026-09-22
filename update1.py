import re

# 1. Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace dates
content = content.replace('18 Sep 2026', '21 Sep 2026')
content = content.replace('18 September 2026', '21 September 2026')
content = content.replace('Friday, 18th September 2026', 'Monday, 21st September 2026')

# Snapshot figures
content = re.sub(r'(id="mi-dsei">)[\d,\.]+', r'\g<1>4,633.82', content)
content = re.sub(r'(id="mi-tsi">)[\d,\.]+', r'\g<1>10,300.66', content)
content = re.sub(r'(data-tzs-value=")\d+(" id="mi-turnover">TZS )[\d\.]+ bn', r'\g<1>11760000000\g<2>11.76 bn', content)

# Top Gainers (VODA, PAL, NMB, MUCOBA, TTP)
gainers_html = """      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--gain)">+3.3%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>PAL</span> <span style="color:var(--gain)">+3.3%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+2.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MUCOBA</span> <span style="color:var(--gain)">+2.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TTP</span> <span style="color:var(--gain)">+2.4%</span></div>
      </div>"""
content = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', f'<!-- GAINERS_START -->\n{gainers_html}\n      <!-- GAINERS_END -->', content, flags=re.DOTALL)

# Top Losers (MCB, DSE, SWIS, TOL, TBL)
losers_html = """      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--loss)">-3.8%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-2.7%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-1.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TBL</span> <span style="color:var(--loss)">-0.7%</span></div>
      </div>"""
content = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', f'<!-- LOSERS_START -->\n{losers_html}\n      <!-- LOSERS_END -->', content, flags=re.DOTALL)


# Update archive list in MI page
# The existing one is 18 Sep. We replace its details with 21 Sep. (The href is a bit tricky, should it be /dse-wrap-2026-09-21 ?)
# "Do not change any page other than the Market Intelligence page... unless strictly required". So maybe I should just update the snippet text.
# The excerpt for 21 Sep: "VODA Closes With Zero Offers as Local Institutions Tighten Their Grip on the Market The Dar es Salaam Stock Exchange opened the new week with a session that confirmed a pattern..."
new_excerpt = "VODA Closes With Zero Offers as Local Institutions Tighten Their Grip on the Market The Dar es Salaam Stock Exchange opened the new week with a session that confirmed a pattern..."
# Actually we truncate at some point. "VODA Closes With Zero Offers as Local Institutions Tighten Their Grip on the Market The Dar es Salaam Stock Exchange opened the new week with a session that confirmed a pattern we have..."
# Let's just use what fits.
content = content.replace('href="/dse-wrap-2026-09-18"', 'href="/dse-wrap-2026-09-21"')
content = content.replace('The Dar es Salaam Stock Exchange closed the week with a session of quiet resilience. Equity turnover fell 72% to TZS 4.30 billion from Thursday\'s block-heavy TZS 15.39 billion, and the All-Share In...', 'VODA Closes With Zero Offers as Local Institutions Tighten Their Grip on the Market The Dar es Salaam Stock Exchange opened the new week with a session that confirmed a pattern...')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("market-intelligence.html updated")
