import os
import sys
import re

work_dir = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
html_file = os.path.join(work_dir, "market-intelligence.html")
js_file = os.path.join(work_dir, "script.min.js")

def update_html():
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements
    content = content.replace(">7 September 2026<", ">14 September 2026<")
    content = content.replace('id="mi-dsei">4,585.52', 'id="mi-dsei">4,689.98')
    content = content.replace('id="mi-tsi">10,101.09', 'id="mi-tsi">10,446.48')
    content = content.replace('data-tzs-value="17310000000"', 'data-tzs-value="6330000000"')
    content = content.replace(">TZS 17.31 bn<", ">TZS 6.33 bn<")

    new_gainers = """<!-- GAINERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--gain)">+5.7%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.8%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MBP</span> <span style="color:var(--gain)">+3.5%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>CRDB</span> <span style="color:var(--gain)">+2.8%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+1.3%</span></div>
      <!-- GAINERS_END -->"""
      
    content = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', new_gainers, content, flags=re.DOTALL)

    new_losers = """<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TTP</span> <span style="color:var(--loss)">-5.6%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MUCOBA</span> <span style="color:var(--loss)">-4.3%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TCCL</span> <span style="color:var(--loss)">-4.3%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NICO</span> <span style="color:var(--loss)">-2.1%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>SWIS</span> <span style="color:var(--loss)">-1.5%</span></div>
      <!-- LOSERS_END -->"""
      
    content = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', new_losers, content, flags=re.DOTALL)

    new_archive = """<a class="archive-row" href="/dse-wrap-2026-09-14">
<div class="archive-date">14 Sep<br/>2026</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | Monday, 14th September 2026</div>
<div class="archive-content-excerpt">Indices hit new post-split highs as market consolidates after record week. Equity turnover fell to TZS 6.33 billion as deals rose 36%. Both DSEI (4,689.98) and TSI (10,446.48) reached new peaks...</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>
<a class="archive-row" href="/dse-wrap-2026-09-07">
<div class="archive-date">07 Sep<br/>2026</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | Monday, 7th September 2026</div>
<div class="archive-content-excerpt">Bond money floods into equities as the rotation signal fires. Equity turnover more than doubled to TZS 17.31 billion while bond turnover collapsed to TZS 7.99 billion. The TSI crossed 10,000...</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>"""
    
    content = re.sub(r'<a class="archive-row" href="/dse-wrap-2026-09-07">.*?<span class="archive-cta">Read &rarr;</span>\n</a>', new_archive, content, flags=re.DOTALL)

    with open(html_file, "w", encoding="utf-8", newline="") as f:
        f.write(content)

if __name__ == "__main__":
    update_html()
    print("Updates applied successfully.")
