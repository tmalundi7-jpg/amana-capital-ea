import os

checks_passed = 0
checks_failed = 0

def check(label, result):
    global checks_passed, checks_failed
    status = "PASS" if result else "FAIL"
    if result:
        checks_passed += 1
    else:
        checks_failed += 1
    print(f"  [{status}] {label}")

# market-intelligence.html
with open("market-intelligence.html", encoding="utf-8") as f:
    mi = f.read()

print("=== market-intelligence.html ===")
check("Date: 23 Sep 2026", "23 Sep 2026" in mi)
check("DSEI 4,638.18", "4,638.18" in mi)
check("TSI 10,309.18", "10,309.18" in mi)
check("Equity turnover 4.13", "4.13" in mi)
check("Bond turnover 39.4x", "39.48" in mi or "39.47" in mi)
check("Top gainer MUCOBA", "MUCOBA" in mi)
check("Top gainer PAL", "PAL" in mi)
check("Top loser TTP -2.3", "TTP" in mi and "-2.3" in mi)
check("Top loser TCC -1.6", "TCC" in mi and "-1.6" in mi)
check("New wrap link 23 Sep", "dse-wrap-2026-09-23" in mi)
check("Cache buster v=20260923a", "v=20260923a" in mi)
check("22 Sep entry REMOVED from archive section", mi.count("dse-wrap-2026-09-22") <= 1)

# script.js heatmap
with open("script.js", encoding="utf-8") as f:
    js = f.read()

print("\n=== script.js heatmap ===")
check("MUCOBA +3.6", "MUCOBA" in js and "3.6" in js)
check("TTP -2.3", "TTP" in js and "-2.3" in js)
check("CRDB 2820", "CRDB" in js and "2820" in js)
check("NMB 2120", "NMB" in js and "2120" in js)
check("VODA 1310", "VODA" in js and "1310" in js)
check("MBP 2.9", "MBP" in js and "2.9" in js)
check("TCC -1.6", "TCC" in js and "-1.6" in js)
check("MCB -1.3", "MCB" in js and "-1.3" in js)

# script.min.js
with open("script.min.js", encoding="utf-8") as f:
    jsmin = f.read()
print("\n=== script.min.js heatmap ===")
check("MUCOBA in min.js", "MUCOBA" in jsmin and "3.6" in jsmin)
check("VODA 1310 in min.js", "VODA" in jsmin and "1310" in jsmin)

# market-intelligence-archive.html
with open("market-intelligence-archive.html", encoding="utf-8") as f:
    arch = f.read()
print("\n=== market-intelligence-archive.html ===")
check("22 Sep entry in archive", "22 SEP 2026" in arch or "22 Sep 2026" in arch or "dse-wrap-2026-09-22" in arch)

# current-prices.html
with open("current-prices.html", encoding="utf-8") as f:
    cp = f.read()
print("\n=== current-prices.html ===")
check("Date: 23 September", "23" in cp and "September" in cp)
check("CRDB price 2,820", "2,820" in cp or "2820" in cp)
check("VODA price 1,310", "1,310" in cp or "1310" in cp)
check("TCC price 13,170", "13,170" in cp or "13170" in cp)
check("NMB block trade 429,000", "429,000" in cp or "429000" in cp)
check("MUCOBA 430", "430" in cp)

# dse-wrap-2026-09-23.html
print("\n=== dse-wrap-2026-09-23.html ===")
check("File exists", os.path.exists("dse-wrap-2026-09-23.html"))
if os.path.exists("dse-wrap-2026-09-23.html"):
    with open("dse-wrap-2026-09-23.html", encoding="utf-8") as f:
        wrap = f.read()
    check("23 Sep date in wrap page", "23" in wrap and "September" in wrap)
    check("Has full HTML structure (nav)", "<nav" in wrap)

print(f"\n{'='*40}")
print(f"TOTAL: {checks_passed} PASSED, {checks_failed} FAILED")
if checks_failed == 0:
    print("ALL CHECKS PASSED - Safe to confirm live.")
else:
    print("FAILURES DETECTED - Review required.")
