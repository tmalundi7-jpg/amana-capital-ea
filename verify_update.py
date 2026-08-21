import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = [
    ("Hero DSEI value",         r'home-stat-label.*?DSEI.*?home-stat-value.*?>(.*?)<', "4,248.98"),
    ("Hero Turnover value",     r"Daily Turnover.*?home-stat-value.*?>(.*?)<", "TZS 4,765.58m"),
    ("Hero Top Mover value",    r"Top Mover.*?home-stat-value.*?>(.*?)<", "DCB +13.98%"),
    ("Hero date badge",         r'home-stat-badge neutral[^>]*>(.*?)<', "17 Aug 2026"),
    ("Snapshot header date",    r"End-of-day[^0-9]*([0-9]+ \w+ [0-9]+)", "17 August 2026"),
    ("Snapshot DSEI",           r'id="home-dsei">(.*?)<span', "4,248.98"),
    ("Snapshot TSI",            r'id="home-tsi">(.*?)<span', "9,349.59"),
    ("Snapshot Turnover",       r'id="home-turnover">(.*?)</div>', "TZS 4,765.58m"),
    ("Snapshot Gainer DCB",     r'home-gainers.*?DCB.*?--gain.*?>(.*?)<', "+13.98%"),
    ("Snapshot Gainer TTP",     r'home-gainers.*?TTP.*?--gain.*?>(.*?)<', "+11.11%"),
    ("Snapshot Gainer NICO",    r'home-gainers.*?NICO.*?--gain.*?>(.*?)<', "+4.45%"),
    ("Snapshot Loser PAL",      r'home-losers.*?PAL.*?--loss.*?>(.*?)<', "-7.25%"),
    ("Snapshot Loser MUCOBA",   r'home-losers.*?MUCOBA.*?--loss.*?>(.*?)<', "-1.10%"),
    ("Snapshot footer date",    r"Live Terminal Feed[^0-9]*([0-9]+ \w+ [0-9]+)", "17 August 2026"),
    ("Teaser DSEI stat",        r'teaser-prem-stat-label.*?DSEI.*?teaser-prem-stat-value.*?>(.*?)<', "4,248.98"),
    ("Teaser Turnover stat",    r'teaser-prem-stat-label.*?Turnover.*?teaser-prem-stat-value.*?>(.*?)<', "TZS 4.77bn"),
    ("Teaser Top Gainer stat",  r'teaser-prem-stat-label.*?Top Gainer.*?teaser-prem-stat-value.*?>(.*?)<', "DCB +14.0%"),
]

print("VERIFICATION CHECKS")
print("=" * 60)
all_pass = True

for label, pattern, expected in checks:
    m = re.search(pattern, html, re.DOTALL)
    if m:
        found = m.group(1).strip()
        ok = expected in found
        if not ok:
            all_pass = False
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got \"{found[:70]}\"")
    else:
        all_pass = False
        print(f"  [FAIL] {label}: pattern not found in HTML")

# Check old date is gone
snap_start = html.find("SNAPSHOT_CARD_START")
snap_end   = html.find("SNAPSHOT_CARD_END")
snap_block = html[snap_start:snap_end] if snap_start >= 0 else ""

old_in_snapshot = "14 August 2026" in snap_block
print(f"  [{'FAIL' if old_in_snapshot else 'PASS'}] Old snapshot date (14 August) removed")

if old_in_snapshot:
    all_pass = False

print()
print("=" * 60)
print("OVERALL: " + ("ALL CHECKS PASSED" if all_pass else "ONE OR MORE CHECKS FAILED"))
