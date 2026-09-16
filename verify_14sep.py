import os
import sys

work_dir = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
html_file = os.path.join(work_dir, "market-intelligence.html")
js_file = os.path.join(work_dir, "script.min.js")

checks_passed = True

def check(condition, msg):
    global checks_passed
    if condition:
        print(f"[PASS] {msg}")
    else:
        print(f"[FAIL] {msg}")
        checks_passed = False

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

with open(js_file, "r", encoding="utf-8") as f:
    js = f.read()

print("--- HTML CHECKS ---")
check("4,689.98" in html, "4,689.98 -> at least 1 hit")
check("10,446.48" in html, "10,446.48 -> at least 1 hit")
check("6.33 bn" in html, "6.33 bn -> at least 1 hit")
check("6330000000" in html, "6330000000 -> at least 1 hit")
check("14 September 2026" in html, "14 September 2026 -> at least 1 hit")
check("dse-wrap-2026-09-14" in html, "dse-wrap-2026-09-14 -> at least 1 hit")
check("dse-wrap-2026-09-07" in html, "dse-wrap-2026-09-07 -> at least 1 hit (07 Sep row still present)")
check(">TOL<" in html and "5.7%" in html, "TOL in gainers -> present")
check(">TTP<" in html and "-5.6%" in html, "TTP in losers -> present")

check("4,585.52" not in html, "OLD 4,585.52 -> 0 hits")
check("10,101.09" not in html, "OLD 10,101.09 -> 0 hits")
check("17.31 bn" not in html, "OLD 17.31 bn -> 0 hits")
check("17310000000" not in html, "OLD 17310000000 -> 0 hits")
check("7 September 2026" not in html, "OLD 7 September 2026 -> 0 hits")

print("\n--- JS CHECKS ---")
check("change: 2.8" in js, "change: 2.8 -> present (CRDB)")
check("change: 5.7" in js, "change: 5.7 -> present (TOL)")
check("change: -4.3" in js, "change: -4.3 -> present (TCCL)")
check("change: 3.8" in js, "change: 3.8 -> present (KCB)")
check("change: 2.2" not in js, "OLD change: 2.2 for CRDB -> 0 hits")
check("change: 10.4" not in js, "OLD change: 10.4 for TOL -> 0 hits")

if checks_passed:
    print("\nALL CHECKS PASSED.")
else:
    print("\nSOME CHECKS FAILED.")
    sys.exit(1)
