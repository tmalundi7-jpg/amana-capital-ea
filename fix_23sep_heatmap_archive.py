"""
Fix script: Update heatmap in script.js and script.min.js with 23 Sep 2026 data,
and ensure 22 Sep wrap entry is in market-intelligence-archive.html.
"""
import re, os

REPO = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"

# ── 1. Update heatmap array in script.js ──────────────────────────────────────
NEW_HEATMAP = """[
        { symbol: 'NMB',       marketCap: 2675, change: -0.9 },
        { symbol: 'TBL',       marketCap: 3200, change: -1.0 },
        { symbol: 'CRDB',      marketCap: 1515, change:  0.4 },
        { symbol: 'VODA',      marketCap: 1200, change: -0.8 },
        { symbol: 'TPCC',      marketCap:  900, change: -0.4 },
        { symbol: 'NICO',      marketCap:  700, change: -0.8 },
        { symbol: 'KCB',       marketCap:  380, change: -0.5 },
        { symbol: 'TCC',       marketCap:  340, change: -1.6 },
        { symbol: 'TCCL',      marketCap:  300, change:  1.9 },
        { symbol: 'DCB',       marketCap:  180, change: -1.1 },
        { symbol: 'MKCB',      marketCap:  150, change:  0.0 },
        { symbol: 'TOL',       marketCap:  120, change:  1.1 },
        { symbol: 'SWIS',      marketCap:  100, change: -1.5 },
        { symbol: 'AFRIPRISE', marketCap:   80, change:  1.3 },
        { symbol: 'MCB',       marketCap:   50, change: -1.3 },
        { symbol: 'PAL',       marketCap:   40, change:  3.3 },
        { symbol: 'MUCOBA',    marketCap:   20, change:  3.6 },
        { symbol: 'MBP',       marketCap:   18, change:  2.9 },
        { symbol: 'DSE',       marketCap:   16, change:  0.0 },
        { symbol: 'TTP',       marketCap:   12, change: -2.3 }
    ]"""

js_path = os.path.join(REPO, "script.js")
with open(js_path, encoding="utf-8") as f:
    js = f.read()

# Find old array and replace
old_start = js.find("[\n        { symbol: 'NMB'")
if old_start == -1:
    # Try alternate opening
    old_start = js.rfind("[", 0, js.find("{ symbol: 'CRDB'"))
old_end = js.find("];\n", old_start) + 1  # include the ]
old_array = js[old_start:old_end]

print(f"Found old heatmap array ({len(old_array)} chars) at index {old_start}")
js_new = js[:old_start] + NEW_HEATMAP + js[old_end:]

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_new)
print("FIXED: script.js heatmap updated")

# ── 2. Update heatmap array in script.min.js ──────────────────────────────────
min_path = os.path.join(REPO, "script.min.js")
with open(min_path, encoding="utf-8") as f:
    jsm = f.read()

# Find CRDB in the min file to locate heatmap
crdb_idx = jsm.find("'CRDB'")
if crdb_idx == -1:
    crdb_idx = jsm.find('"CRDB"')

old_start_m = jsm.rfind("[", 0, crdb_idx)
old_end_m = jsm.find("]", crdb_idx) + 1
old_arr_m = jsm[old_start_m:old_end_m]
print(f"Found min.js heatmap array ({len(old_arr_m)} chars)")

# Compact version for min.js
NEW_HEATMAP_MIN = "[{symbol:'NMB',marketCap:2675,change:-0.9},{symbol:'TBL',marketCap:3200,change:-1.0},{symbol:'CRDB',marketCap:1515,change:0.4},{symbol:'VODA',marketCap:1200,change:-0.8},{symbol:'TPCC',marketCap:900,change:-0.4},{symbol:'NICO',marketCap:700,change:-0.8},{symbol:'KCB',marketCap:380,change:-0.5},{symbol:'TCC',marketCap:340,change:-1.6},{symbol:'TCCL',marketCap:300,change:1.9},{symbol:'DCB',marketCap:180,change:-1.1},{symbol:'MKCB',marketCap:150,change:0.0},{symbol:'TOL',marketCap:120,change:1.1},{symbol:'SWIS',marketCap:100,change:-1.5},{symbol:'AFRIPRISE',marketCap:80,change:1.3},{symbol:'MCB',marketCap:50,change:-1.3},{symbol:'PAL',marketCap:40,change:3.3},{symbol:'MUCOBA',marketCap:20,change:3.6},{symbol:'MBP',marketCap:18,change:2.9},{symbol:'DSE',marketCap:16,change:0.0},{symbol:'TTP',marketCap:12,change:-2.3}]"
jsm_new = jsm[:old_start_m] + NEW_HEATMAP_MIN + jsm[old_end_m:]

with open(min_path, "w", encoding="utf-8") as f:
    f.write(jsm_new)
print("FIXED: script.min.js heatmap updated")

# ── 3. Fix market-intelligence-archive.html — add 22 Sep entry ────────────────
# The 22 Sep entry to insert (copied from what was in market-intelligence.html before update)
ENTRY_22SEP = """        <a class="archive-row" href="/dse-wrap-2026-09-22">
          <div class="archive-date">22 SEP 2026</div>
          <div>
            <span class="archive-badge badge-equity">Equity</span>
            <div class="archive-content-title">DSE Daily Wrap &mdash; Tuesday, 22 September 2026</div>
            <div class="archive-content-excerpt">VODA surged 4.8% to hit the 5% daily ceiling. CRDB absorbed an 868k-share foreign exit with a 3.9x bid/offer ratio. Bond turnover skyrocketed 485% to TZS 33.59 billion.</div>
          </div>
          <span class="archive-cta">Read &rarr;</span>
        </a>
"""

arch_path = os.path.join(REPO, "market-intelligence-archive.html")
with open(arch_path, encoding="utf-8") as f:
    arch = f.read()

# Check if 22 Sep is already there
if "22 SEP 2026" in arch or "dse-wrap-2026-09-22" in arch:
    print("SKIP: 22 Sep entry already in archive")
else:
    # Insert after the opening <div class="archive-list"> tag
    insert_marker = '<div class="archive-list">'
    insert_pos = arch.find(insert_marker)
    if insert_pos == -1:
        insert_marker = 'archive-list'
        insert_pos = arch.find(insert_marker)
        insert_pos = arch.find(">", insert_pos) + 1
    else:
        insert_pos = insert_pos + len(insert_marker) + 1  # after the >

    arch_new = arch[:insert_pos] + "\n" + ENTRY_22SEP + arch[insert_pos:]
    with open(arch_path, "w", encoding="utf-8") as f:
        f.write(arch_new)
    print("FIXED: 22 Sep entry added to market-intelligence-archive.html")

# ── 4. Verify all fixes ────────────────────────────────────────────────────────
with open(js_path, encoding="utf-8") as f:
    js_v = f.read()
with open(min_path, encoding="utf-8") as f:
    jsm_v = f.read()
with open(arch_path, encoding="utf-8") as f:
    arch_v = f.read()

print("\n=== Post-fix verification ===")
ok = True
checks = [
    ("script.js MUCOBA 3.6",    "MUCOBA" in js_v and "3.6" in js_v),
    ("script.js TTP -2.3",      "TTP" in js_v and "-2.3" in js_v),
    ("script.js VODA -0.8",     "VODA" in js_v and "-0.8" in js_v),
    ("script.js CRDB 0.4",      "CRDB" in js_v and "0.4" in js_v),
    ("script.min.js MUCOBA",    "MUCOBA" in jsm_v and "3.6" in jsm_v),
    ("script.min.js TTP",       "TTP" in jsm_v and "-2.3" in jsm_v),
    ("archive has 22 Sep",      "22 SEP 2026" in arch_v or "dse-wrap-2026-09-22" in arch_v),
]
for label, result in checks:
    status = "PASS" if result else "FAIL"
    if not result:
        ok = False
    print(f"  [{status}] {label}")

if ok:
    print("\nAll fixes verified. Ready to push.")
else:
    print("\nSome checks still failing - investigate.")
