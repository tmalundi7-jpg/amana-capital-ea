import json, re, sys, zipfile, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")

# ── Load sources ──────────────────────────────────────────────────────────────
with open("extracted_dse_data.json", encoding="utf-8") as f:
    J = json.load(f)

with open("index.html", encoding="utf-8") as f:
    HTML = f.read()

# ── Helper: extract plain text from a region of HTML ─────────────────────────
def text_in(html, pattern):
    """Return first capture group of pattern searched over full HTML (DOTALL)."""
    m = re.search(pattern, html, re.DOTALL)
    return m.group(1).strip() if m else None

# ── Pull expected values from JSON ────────────────────────────────────────────
E = {
    "dsei_eod"   : J["dsei_end_of_day"],          # 4,248.98
    "turnover"   : J["daily_turnover"],            # TZS 4,765.58m
    "tm_name"    : J["top_mover"]["name"],         # DCB
    "tm_change"  : J["top_mover"]["change"],       # +13.98%
    "listed"     : J["dse_listed_companies"],      # 28
    "snap_dsei"  : J["live_dse_snapshot"]["dsei"], # 4,248.98
    "snap_tsi"   : J["live_dse_snapshot"]["tsi"],  # 9,349.59
    "snap_turn"  : J["live_dse_snapshot"]["turnover"],
    "g0_name"    : J["live_dse_snapshot"]["top_gainers"][0]["name"],
    "g0_chg"     : J["live_dse_snapshot"]["top_gainers"][0]["change"],
    "g1_name"    : J["live_dse_snapshot"]["top_gainers"][1]["name"],
    "g1_chg"     : J["live_dse_snapshot"]["top_gainers"][1]["change"],
    "g2_name"    : J["live_dse_snapshot"]["top_gainers"][2]["name"],
    "g2_chg"     : J["live_dse_snapshot"]["top_gainers"][2]["change"],
    "l0_name"    : J["live_dse_snapshot"]["top_losers"][0]["name"],
    "l0_chg"     : J["live_dse_snapshot"]["top_losers"][0]["change"],
    "l1_name"    : J["live_dse_snapshot"]["top_losers"][1]["name"],
    "l1_chg"     : J["live_dse_snapshot"]["top_losers"][1]["change"],
    "l2_name"    : J["live_dse_snapshot"]["top_losers"][2]["name"],
    "l2_chg"     : J["live_dse_snapshot"]["top_losers"][2]["change"],
    "wrap_dsei"  : J["daily_dse_wrap"]["dsei"],
    "wrap_turn"  : J["daily_dse_wrap"]["turnover"],
    "wrap_tg"    : J["daily_dse_wrap"]["top_gainer"]["name"],
    "report_date": J["report_date"],
}

# Derive display forms
E["tm_display"]   = E["tm_name"] + " " + E["tm_change"]      # DCB +13.98%
raw_pct = float(E["tm_change"].replace("%","").replace("+","").replace(",",""))
E["tg_display"]   = E["tm_name"] + " +" + f"{abs(raw_pct):.1f}%"  # DCB +14.0%
E["turn_bn"]      = "TZS 4.77bn"                              # display in teaser

# ── Extract values from HTML ──────────────────────────────────────────────────

def h(pat):
    return text_in(HTML, pat)

A = {}

# Hero stats
A["hero_dsei"]    = h(r'DSEI \u2014 End of Day.*?home-stat-value[^>]*>([^<]+)<')
A["hero_turn"]    = h(r'Daily Turnover.*?home-stat-value[^>]*>([^<]+)<')
A["hero_mover"]   = h(r'Top Mover.*?home-stat-value[^>]*>([^<]+)<')
A["hero_date"]    = h(r'home-stat-badge neutral[^>]*>([^<]+)<')
A["hero_listed"]  = h(r'DSE Listed Companies.*?home-stat-value[^>]*>([^<]+)<')

# Snapshot header date
A["snap_hdr_date"] = h(r'End-of-day\s*\u00b7\s*([0-9]+ \w+ [0-9]+)')

# Snapshot values
A["snap_dsei"]   = h(r'id="home-dsei">([0-9,\.]+)\s*<span')
A["snap_tsi"]    = h(r'id="home-tsi">([0-9,\.]+)\s*<span')
A["snap_turn"]   = h(r'id="home-turnover">([^<]+)</div>')

# Snapshot gainers block — extract the three name+change pairs
gainers_block = h(r'id="home-gainers"[^>]*>(.*?)</div>')
losers_block  = h(r'id="home-losers"[^>]*>(.*?)</div>')

def extract_movers(block):
    """Return list of (name, change) from the gainers/losers inner HTML."""
    if not block:
        return []
    spans = re.findall(r'<span>(\w+)\s+<span[^>]*>([^<]+)</span></span>', block)
    return spans

g_spans = extract_movers(gainers_block)
l_spans = extract_movers(losers_block)

A["g0"] = g_spans[0] if len(g_spans) > 0 else None
A["g1"] = g_spans[1] if len(g_spans) > 1 else None
A["g2"] = g_spans[2] if len(g_spans) > 2 else None
A["l0"] = l_spans[0] if len(l_spans) > 0 else None
A["l1"] = l_spans[1] if len(l_spans) > 1 else None
A["l2"] = l_spans[2] if len(l_spans) > 2 else None

# Snapshot footer date
A["snap_footer"]  = h(r'Live Terminal Feed \| End-of-day, ([0-9]+ \w+ [0-9]+)')

# Teaser stats — extract the block between comment markers
tb_m = re.search(r'TEASER_CARD_START(.*?)TEASER_CARD_END', HTML, re.DOTALL)
teaser_block = tb_m.group(1) if tb_m else ""

def ht(pat):
    return text_in(teaser_block, pat) if teaser_block else None

A["teas_date"]   = ht(r'teaser-prem-date[^>]*>([^<]+)<')
A["teas_dsei"]   = ht(r'teaser-prem-stat-label[^>]*>DSEI.*?teaser-prem-stat-value[^>]*>([^<]+)<')
A["teas_turn"]   = ht(r'teaser-prem-stat-label[^>]*>Turnover.*?teaser-prem-stat-value[^>]*>([^<]+)<')
A["teas_tg"]     = ht(r'teaser-prem-stat-label[^>]*>Top Gainer.*?teaser-prem-stat-value[^>]*>([^<]+)<')

# Old dates that must NOT appear in updated sections
snap_section = HTML[HTML.find("SNAPSHOT_CARD_START"):HTML.find("SNAPSHOT_CARD_END")]
A["old_14aug_in_snap"] = "14 August 2026" in snap_section or "14 Aug 2026" in snap_section
A["old_14aug_in_hero"] = "14 Aug 2026" in HTML[HTML.find("home-hero-stats"):HTML.find("home-hero-stats")+800]

# ── Build QA checks ──────────────────────────────────────────────────────────
results = []

def chk(label, actual, expected, note=""):
    ok = (actual is not None) and (expected in actual or actual == expected)
    results.append((label, ok, actual, expected, note))

chk("DSEI — End of Day (hero)",              A["hero_dsei"],    E["dsei_eod"])
chk("Daily Turnover (hero)",                  A["hero_turn"],    E["turnover"])
chk("Top Mover name+change (hero)",           A["hero_mover"],   E["tm_display"])
chk("Date badge on hero",                     A["hero_date"],    "17 Aug 2026")
chk("DSE Listed Companies (hero)",            A["hero_listed"],  E["listed"])
chk("Snapshot header date",                   A["snap_hdr_date"],"17 August 2026")
chk("Snapshot DSEI",                          A["snap_dsei"],    E["snap_dsei"])
chk("Snapshot TSI",                           A["snap_tsi"],     E["snap_tsi"])
chk("Snapshot Turnover",                      A["snap_turn"],    E["snap_turn"])
chk("Snapshot Top Gainer 1 name",            str(A["g0"][0]) if A["g0"] else None, E["g0_name"])
chk("Snapshot Top Gainer 1 change",          str(A["g0"][1]) if A["g0"] else None, E["g0_chg"])
chk("Snapshot Top Gainer 2 name",            str(A["g1"][0]) if A["g1"] else None, E["g1_name"])
chk("Snapshot Top Gainer 2 change",          str(A["g1"][1]) if A["g1"] else None, E["g1_chg"])
chk("Snapshot Top Gainer 3 name",            str(A["g2"][0]) if A["g2"] else None, E["g2_name"])
chk("Snapshot Top Gainer 3 change",          str(A["g2"][1]) if A["g2"] else None, E["g2_chg"])
chk("Snapshot Top Loser 1 name",             str(A["l0"][0]) if A["l0"] else None, E["l0_name"])
chk("Snapshot Top Loser 1 change",           str(A["l0"][1]) if A["l0"] else None, E["l0_chg"])
chk("Snapshot Top Loser 2 name",             str(A["l1"][0]) if A["l1"] else None, E["l1_name"])
chk("Snapshot Top Loser 2 change",           str(A["l1"][1]) if A["l1"] else None, E["l1_chg"])
chk("Snapshot Top Loser 3 name",             str(A["l2"][0]) if A["l2"] else None, E["l2_name"])
chk("Snapshot Top Loser 3 change",           str(A["l2"][1]) if A["l2"] else None, E["l2_chg"])
chk("Snapshot footer date",                  A["snap_footer"],  "17 August 2026")
chk("Wrap teaser date line",                 A["teas_date"],    "17 August 2026")
chk("Wrap teaser DSEI stat",                 A["teas_dsei"],    E["wrap_dsei"])
chk("Wrap teaser Turnover stat",             A["teas_turn"],    E["turn_bn"])
chk("Wrap teaser Top Gainer stat",           A["teas_tg"],      E["tg_display"])
chk("Old date (14 Aug) absent from snapshot",str(not A["old_14aug_in_snap"]), "True",
    "Old date must be gone")
chk("Old date (14 Aug) absent from hero",    str(not A["old_14aug_in_hero"]), "True",
    "Old date must be gone")

# ── Print QA report ──────────────────────────────────────────────────────────
PASS_ALL = all(r[1] for r in results)

print("=" * 65)
print("QA VERIFICATION REPORT  |  17 August 2026 DSE Homepage Update")
print("=" * 65)
print()
print("QA CHECKLIST")
print()
for label, ok, actual, expected, note in results:
    mark = "[PASS]" if ok else "[FAIL]"
    print(f"  {mark}  {label}")
    if not ok:
        print(f"         Expected : {expected}")
        print(f"         Got      : {actual}")
    if note:
        print(f"         Note     : {note}")

print()
print("-" * 65)
total = len(results)
passed = sum(1 for r in results if r[1])
failed = total - passed
print(f"Total checks: {total}   Passed: {passed}   Failed: {failed}")
print()
if PASS_ALL:
    print("Overall Result: PASS")
    print("=> All checks passed. Homepage is verified. Safe to deploy.")
else:
    print("Overall Result: FAIL")
    print("=> DO NOT DEPLOY. Return failed items to Prompt 1 operator.")
print("=" * 65)

# Write report to file
with open("qa_report_17aug2026.txt", "w", encoding="utf-8") as f:
    f.write(f"QA VERIFICATION REPORT  |  17 August 2026 DSE Homepage Update\n")
    f.write("=" * 65 + "\n\n")
    for label, ok, actual, expected, note in results:
        mark = "PASS" if ok else "FAIL"
        f.write(f"  [{mark}]  {label}\n")
        if not ok:
            f.write(f"         Expected : {expected}\n")
            f.write(f"         Got      : {actual}\n")
    f.write(f"\nTotal: {total}   Passed: {passed}   Failed: {failed}\n")
    f.write(f"Overall Result: {'PASS' if PASS_ALL else 'FAIL'}\n")

import sys
sys.exit(0 if PASS_ALL else 1)
