import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATE_LONG = "Thursday, 3rd September 2026"
DSEI      = "4,442.62"
TSI       = "9,653.89"
TURNOVER  = "TZS 42.93 bn"
GAINERS   = [("MBP", "+8.2%"), ("NMG", "+7.9%"), ("KCB", "+3.9%")]
LOSERS    = [("TCCL", "-4.0%"), ("TTP", "-2.1%"), ("DSE", "-1.8%")]
WRAP_URL  = "/dse-wrap-2026-09-03"

def check(label, val, html, good_if='in'):
    val_clean = val.replace('\xa0', ' ')
    if good_if == 'in':
        ok = val_clean in html
    else:
        ok = val_clean not in html
    status = "PASS" if ok else "FAIL"
    if not ok:
        print(f"  [{status}] {label}: '{val_clean}' NOT FOUND")
    else:
        print(f"  [{status}] {label}")

print("\n============ index.html ============")
c = open('index.html', encoding='utf-8').read()
check("snapshot date (End-of-day)", "End-of-day &middot; 3 September 2026", c)
check("terminal feed date", "Terminal Feed | End-of-day &middot; 3 September 2026", c)
check("DSEI id", DSEI, c)
check("TSI id", TSI, c)
check("Turnover id", TURNOVER, c)
check("Gainer 1 MBP", "MBP", c)
check("Gainer 1 +8.2%", "+8.2%", c)
check("Gainer 2 NMG", "NMG", c)
check("Gainer 2 +7.9%", "+7.9%", c)
check("Gainer 3 KCB", "KCB", c)
check("Gainer 3 +3.9%", "+3.9%", c)
check("Loser 1 TCCL", "TCCL", c)
check("Loser 1 -4.0%", "-4.0%", c)
check("Loser 2 TTP", "TTP", c)
check("Loser 2 -2.1%", "-2.1%", c)
check("Loser 3 DSE", 'DSE', c)
check("Loser 3 -1.8%", "-1.8%", c)
check("Teaser date", "Thursday, 3rd September 2026", c)
check("Teaser headline", "TZS 30 Billion", c)
check("CTA link", WRAP_URL, c)
check("OLD date not in teaser", "2nd September 2026", c, good_if='not_in')

print("\n============ market-intelligence.html ============")
c = open('market-intelligence.html', encoding='utf-8').read()
check("Hero date 03 Sep", "03 Sep 2026", c)
check("Snapshot date", "3 September 2026", c)
check("DSEI", DSEI, c)
check("TSI", TSI, c)
check("Turnover", TURNOVER, c)
check("Gainer MBP", "MBP", c)
check("+8.2%", "+8.2%", c)
check("Loser TCCL", "TCCL", c)
check("-4.0%", "-4.0%", c)
check("spotlight URL", WRAP_URL, c)
check("spotlight date", "Thursday, 3rd September 2026", c)

print("\n============ market-intelligence-archive.html ============")
c = open('market-intelligence-archive.html', encoding='utf-8').read()
check("03 Sep arc-row entry", "dse-wrap-2026-09-03", c)
check("03 Sep headline in archive", "TZS 30 Billion", c)

print("\n============ current-prices.html ============")
c = open('current-prices.html', encoding='utf-8').read()
check("AFRIPRISE row", "AFRIPRISE", c)
check("CRDB 2680", "2,680", c)
check("MBP +8.2%", "+8.2%", c)
check("TCCL -4.0%", "-4.0%", c)
check("Prices date", "3rd September 2026", c)

print("\n============ dse-wrap-2026-09-03.html ============")
c = open('dse-wrap-2026-09-03.html', encoding='utf-8').read()
check("Title", "Thursday, 3rd September 2026", c)
check("Headline", "TZS 30 Billion", c)
check("Section 7 gold border", "border-left: 4px solid var(--gold)", c)
check("No bad unicode", "\ufffd", c, good_if='not_in')
check("No NBSP", "\xa0", c, good_if='not_in')
check("OG image tag", "og:image", c)

print("\nDone.")
