from bs4 import BeautifulSoup
import re
import json

with open('extracted_31aug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc_html = f.read()

# I will use string replacement because BeautifulSoup sometimes messes up formatting.
# First, remove my bad injection
arc_html = re.sub(r'\s*<div class="arc-row">\s*<div class="arc-date">31 Aug<br>2026</div>.*?</p>\s*</div>\s*<a href="/dse-wrap-2026-08-31" class="arc-read">Read Report &rarr;</a>\s*</div>', '', arc_html, flags=re.DOTALL)

# Find where the list starts
list_start = arc_html.find('<div class="arc-list">')
if list_start != -1:
    insert_pos = list_start + len('<div class="arc-list">')
    
    new_entry = """
<div class="arc-row">
  <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">31 Aug 2026</div>
  <div><div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">The Market Matures: Record Volumes, Block Trades, and the Fall of Bond Yields</div><div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">The era of 15% risk-free yields is ending. In 2025, government bonds were issued with coupons of 15-16%. In 2026, the new issues carry coupons of 12-...</div></div>
  <a href="/dse-wrap-2026-08-31" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
</div>"""
    
    if "31 Aug 2026" not in arc_html:
        arc_html = arc_html[:insert_pos] + new_entry + arc_html[insert_pos:]

# Now fix the alternating backgrounds!
# Find all `<div class="arc-row" ...>` and replace with alternating styles
def replacer(match):
    replacer.count += 1
    # Check if last item (we can't easily, but let's assume we can just apply border-bottom to all except the last if we could, but the original HTML just has it on all except the last one manually... wait, I'll just use CSS in the style block!)
    return match.group(0)

# Instead of inline styles, why don't I just add a <style> block to the head of this file for `.arc-row`?
# Much safer and cleaner!
style_block = """
<style>
.arc-row {
    display: grid; 
    grid-template-columns: 110px 1fr auto; 
    align-items: center; 
    gap: 1rem; 
    padding: 0.9rem 1.25rem; 
    border-bottom: 1px solid rgba(11,29,58,0.06);
}
.arc-row:last-child {
    border-bottom: none;
}
.arc-row:nth-child(even) {
    background: transparent;
}
.arc-row:nth-child(odd) {
    background: rgba(11,29,58,0.02);
}
</style>
"""

# Let's clean out the inline styles from ALL arc-rows in the HTML
arc_html = re.sub(r'<div class="arc-row"[^>]*>', '<div class="arc-row">', arc_html)

# And add the style block before </head> if not already there
if ".arc-row {" not in arc_html:
    arc_html = arc_html.replace('</head>', style_block + '</head>')

with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
    f.write(arc_html)

print("Archive fixed!")
