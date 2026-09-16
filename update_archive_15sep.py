import os

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_row = '''<div class="arc-row">
<div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">14 Sep 2026</div>
<div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Monday, 14th September 2026</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">Indices hit new post-split highs as market consolidates after record week. Equity turnover fell to TZS 6.33 billion as deals rose 36%. Both DSEI (4,689.98) and TSI (10,446.48) reached new peaks...</div></div>
<a href="/dse-wrap-2026-09-14" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>\n'''

archive_start = text.find('<div id="archiveList" style="border: 1px solid rgba(11,29,58,0.09); border-radius: 8px; overflow: hidden; background: #fff;">')
if archive_start != -1:
    insert_idx = text.find('>', archive_start) + 1
    # Check if 14 Sep is already there to avoid duplicates
    if text[insert_idx:insert_idx+1000].find('14 Sep 2026') == -1:
        text = text[:insert_idx] + '\n' + new_row + text[insert_idx:]

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated archive')
