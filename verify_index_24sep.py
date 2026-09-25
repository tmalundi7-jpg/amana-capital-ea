import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = []
checks.append(("Snapshot Date", "24 September 2026" in html))
checks.append(("Wrap Date", "Thursday, 24th September 2026" in html))
checks.append(("DSEI", "4,658.16" in html))
checks.append(("TSI", "10,362.31" in html))
checks.append(("Turnover", "TZS 2.73 bn" in html))
checks.append(("Gainers", "TCCL" in html and "NICO" in html and "CRDB" in html))
checks.append(("Losers", "MUCOBA" in html and "PAL" in html and "AFRIPRISE" in html))
checks.append(("Wrap Body", "The Dar es Salaam Stock Exchange delivered a quieter session on Thursday" in html))
checks.append(("No 23 Sep remaining", "23 September 2026" not in html and "23rd September" not in html))

ok = True
for c, result in checks:
    print(f"[{'PASS' if result else 'FAIL'}] {c}")
    if not result: ok = False

if ok: print("\nALL CHECKS PASSED.")
