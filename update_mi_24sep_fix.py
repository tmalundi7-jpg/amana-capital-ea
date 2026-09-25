import re
import os

REPO = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"

def read_file(filename):
    with open(os.path.join(REPO, filename), "r", encoding="utf-8") as f:
        return f.read()

def write_file(filename, content):
    with open(os.path.join(REPO, filename), "w", encoding="utf-8") as f:
        f.write(content)

# 1. Fix market-intelligence-archive.html
arch = read_file("market-intelligence-archive.html")
arch_entry_23sep = """        <div class="arc-row">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px;">23 Sep 2026</div>
          <div>
            <div style="font-weight: 700; font-size: 0.88rem; color: var(--navy); margin-bottom: 0.2rem; line-height: 1.3;">Daily DSE Wrap | Wednesday, 23rd September 2026</div>
            <div style="font-size: 0.78rem; color: rgba(11,29,58,0.5); line-height: 1.4;">DSEI fell 21.05 pts to 4,638.18. CRDB showed a 4.34x bid/offer ratio as foreign selling collapsed to 5.34%. Bond market absorbed TZS 39.47 billion.</div>
          </div>
          <a href="/dse-wrap-2026-09-23" style="font-size: 0.78rem; font-weight: 700; color: var(--gold); text-decoration: none; white-space: nowrap;">Read &rarr;</a>
        </div>\n"""

# Insert right after <div id="archiveList"...>
if '23 Sep 2026' not in arch and '/dse-wrap-2026-09-23' not in arch:
    target = '<div id="archiveList" style="border: 1px solid rgba(11,29,58,0.09); border-radius: 8px; overflow: hidden; background: #fff;">'
    arch = arch.replace(target, target + '\n' + arch_entry_23sep)
    write_file("market-intelligence-archive.html", arch)
    print("Fixed market-intelligence-archive.html")

# 2. Fix current-prices.html block trade shares
cp = read_file("current-prices.html")
# Replace the specific span structure
old_block = '429,000 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span>'
new_block = '140,968 <span style="font-size: 0.95rem; font-weight: 400; color: #6B7280;">shares</span>'
if old_block in cp:
    cp = cp.replace(old_block, new_block)
    write_file("current-prices.html", cp)
    print("Fixed current-prices.html block trade volume")
