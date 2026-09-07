import re

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find Hero / Snapshot date
hero = re.search(r'<strong>(.*?)</strong>', c)
if hero: print('Hero date:', hero.group(1))

# Find DSEI stat
dsei = re.search(r'DSEI</div>\s*<div class="snapshot-value".*?>(.*?)</div>', c, re.DOTALL)
if dsei: print('DSEI:', dsei.group(1).strip())

# Find Top Gainers
gainers = re.search(r'<div class="snapshot-label">Top Gainers</div>\s*<div class="snapshot-mover" id="mi-gainers"[^>]*>(.*?)</div>', c, re.DOTALL)
if gainers: print('Gainers:', gainers.group(1).strip())

# Find Top Losers
losers = re.search(r'<div class="snapshot-label">Top Losers</div>\s*<div class="snapshot-mover" id="mi-losers"[^>]*>(.*?)</div>', c, re.DOTALL)
if losers: print('Losers:', losers.group(1).strip())

# Find Archive featured wrap
archive = re.search(r'<a href="([^"]+)" class="archive-row">\s*<div class="arc-date">(.*?)</div>\s*<div class="arc-title">(.*?)</div>\s*<div class="arc-desc">(.*?)</div>', c, re.DOTALL)
if archive:
    print('Featured Wrap Link:', archive.group(1))
    print('Featured Wrap Date:', archive.group(2))
    print('Featured Wrap Title:', archive.group(3))
    print('Featured Wrap Desc:', archive.group(4).strip()[:100])
