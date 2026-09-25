import os
import re

REPO = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"

def read_file(filename):
    with open(os.path.join(REPO, filename), "r", encoding="utf-8") as f:
        return f.read()

checks = []

# market-intelligence.html
mi = read_file("market-intelligence.html")
checks.append(("MI Hero Date", "24 Sep 2026" in mi))
checks.append(("MI Snapshot Date", ">24 September 2026<" in mi))
checks.append(("MI DSEI", '<div class="snapshot-value" id="mi-dsei">4,658.16</div>' in mi))
checks.append(("MI TSI", '<div class="snapshot-value" id="mi-tsi">10,362.31</div>' in mi))
checks.append(("MI Turnover", '<div class="snapshot-value" data-format-type="bn" data-tzs-value="2730000000" id="mi-turnover">TZS 2.73 bn</div>' in mi))
checks.append(("MI Top Gainer", "TCCL" in mi and "+3.7%" in mi))
checks.append(("MI Top Loser", "MUCOBA" in mi and "-5.8%" in mi))
checks.append(("MI Archive entry", 'href="/dse-wrap-2026-09-24"' in mi))

# market-intelligence-archive.html
arch = read_file("market-intelligence-archive.html")
checks.append(("Archive 23 Sep entry", "23 Sep 2026" in arch and 'href="/dse-wrap-2026-09-23"' in arch))

# current-prices.html
cp = read_file("current-prices.html")
checks.append(("CP Date", "Thursday 24th September 2026" in cp))
checks.append(("CP Pre-arranged", "140,968 shares" in cp))
checks.append(("CP TCCL price", "3,920" in cp and "+3.7%" in cp))
checks.append(("CP MUCOBA price", "405" in cp and "-5.8%" in cp))

# script.js and script.min.js
js = read_file("script.js")
jsm = read_file("script.min.js")
checks.append(("JS TCCL heatmap", "symbol: 'TCCL'" in js and "3.7" in js))
checks.append(("JS MUCOBA heatmap", "symbol: 'MUCOBA'" in js and "-5.8" in js))
checks.append(("JSM TCCL heatmap", "symbol:'TCCL'" in jsm and "3.7" in jsm))
checks.append(("JSM MUCOBA heatmap", "symbol:'MUCOBA'" in jsm and "-5.8" in jsm))

ok = True
print("\n=== VERIFICATION RESULTS ===")
for label, passed in checks:
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {label}")
    if not passed: ok = False

if ok:
    print("\nALL CHECKS PASSED.")
else:
    print("\nSOME CHECKS FAILED.")
