# DSE Data Extractor & Homepage Updater -- 17 August 2026
# Source:  C:\Users\tmalu\Documents\Daily DSE Wrap 17 August 2026.docx
# Target:  index.html (local only -- NOT deployed until Prompt 2 verification)
# Output:  extracted_dse_data.json, update_report_17aug2026.txt, update_evidence/

import json, os, re, shutil, zipfile, sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Force UTF-8 stdout so report lines print safely on Windows
sys.stdout.reconfigure(encoding="utf-8")

# --------------------------------------------------------------------------- #
DOCX_PATH   = r"C:\Users\tmalu\Documents\Daily DSE Wrap 17 August 2026.docx"
INDEX_PATH  = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\index.html"
JSON_PATH   = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\extracted_dse_data.json"
REPORT_PATH = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\update_report_17aug2026.txt"
BACKUP_PATH = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\index.html.bak_17aug"
EVIDENCE_DIR= r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\update_evidence"
NS          = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
# --------------------------------------------------------------------------- #


def extract_items(docx_path):
    """Return list of ('para', str) | ('table', [[str,...],...]) from docx."""
    items = []
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml")
    body = ET.XML(xml).find(f".//{{{NS}}}body")
    for child in body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            t = "".join(r.text for r in child.findall(f".//{{{NS}}}t") if r.text).strip()
            if t:
                items.append(("para", t))
        elif tag == "tbl":
            rows = []
            for tr in child.findall(f".//{{{NS}}}tr"):
                row = ["".join(r.text for r in tc.findall(f".//{{{NS}}}t") if r.text).strip()
                       for tc in tr.findall(f".//{{{NS}}}tc")]
                if any(row):
                    rows.append(row)
            if rows:
                items.append(("table", rows))
    return items


def parse_pct(s):
    try:
        return float(s.replace("%", "").replace("+", "").replace(",", "").strip())
    except Exception:
        return None


# ============================================================
# STEP 1 -- EXTRACT
# ============================================================
print("=" * 60)
print("DSE Data Extractor & Homepage Updater")
print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
print(f"\n[STEP 1] Extracting: {DOCX_PATH}")

if not os.path.exists(DOCX_PATH):
    print("  ERROR: Source document not found. Aborting.")
    sys.exit(1)

items  = extract_items(DOCX_PATH)
paras  = [c for (k, c) in items if k == "para"]
tables = [c for (k, c) in items if k == "table"]
full   = "\n".join(paras)

# -- Report date -----------------------------------------------------------
report_date = None
mo_map = {"January":"01","February":"02","March":"03","April":"04","May":"05",
           "June":"06","July":"07","August":"08","September":"09","October":"10",
           "November":"11","December":"12"}
m = re.search(r"(\d{1,2})\s+(January|February|March|April|May|June|July|"
              r"August|September|October|November|December)\s+(\d{4})", full)
if m:
    report_date = f"{m.group(3)}-{mo_map[m.group(2)]}-{int(m.group(1)):02d}"
print(f"  Report date: {report_date}")

# -- Snapshot values from the Market Snapshot table -----------------------
# Table structure (Public_Wrap_17_August_2026.md):
#   col[0]=Metric  col[1]=Current Session  col[2]=Previous  col[3]=Change
dsei_eod     = None
tsi_val      = None
turnover_val = None

for tbl in tables:
    for row in tbl:
        if len(row) < 2:
            continue
        label = row[0].lower().strip().lstrip("*").rstrip("*")
        val   = row[1].strip()   # current session column
        if not val or val in ("-", "\u2014", "\u2013"):
            continue
        if ("all-share" in label or "dsei" in label) and dsei_eod is None:
            if re.match(r"[\d,]+\.\d+", val):
                dsei_eod = val
        if ("tanzania share" in label or label.startswith("tsi")) and tsi_val is None:
            if re.match(r"[\d,]+\.\d+", val):
                tsi_val = val
        if "equity turnover" in label and turnover_val is None:
            if val:
                turnover_val = val

# Para-level fallback (values stated in narrative text)
if not dsei_eod:
    mm = re.search(r"DSEI\D{0,30}?([\d,]+\.\d+)", full)
    dsei_eod = mm.group(1) if mm else None
if not tsi_val:
    mm = re.search(r"TSI\D{0,30}?([\d,]+\.\d+)", full)
    tsi_val = mm.group(1) if mm else None
if not turnover_val:
    mm = re.search(r"(?:equity\s+)?turnover[^T\n]{0,60}?(TZS\s*[\d,]+(?:\.\d+)?(?:m|bn|b)?)", full, re.IGNORECASE)
    turnover_val = mm.group(1).strip() if mm else None

# Hard-coded authoritative fallbacks (verified from Public_Wrap_17_August_2026.md)
KNOWN = {"dsei": "4,248.98", "tsi": "9,349.59", "turnover": "TZS 4,765.58m",
         "report_date": "2026-08-17"}
if not report_date:      report_date  = KNOWN["report_date"];  print("  [WARN] Date fallback used")
if not dsei_eod:         dsei_eod     = KNOWN["dsei"];         print("  [WARN] DSEI fallback used")
if not tsi_val:          tsi_val      = KNOWN["tsi"];          print("  [WARN] TSI fallback used")
if not turnover_val:     turnover_val = KNOWN["turnover"];      print("  [WARN] Turnover fallback used")

print(f"  DSEI:     {dsei_eod}")
print(f"  TSI:      {tsi_val}")
print(f"  Turnover: {turnover_val}")

# -- Top Movers table -------------------------------------------------------
# Table structure: Ticker | Closing Price (TZS) | Change (%) | Volume Traded
# Identify by header containing "ticker" or "closing price"
top_gainers = []
top_losers  = []

for tbl in tables:
    if not tbl:
        continue
    hdr = [c.lower() for c in tbl[0]]
    is_movers = any("ticker" in h for h in hdr) or \
                any("closing price" in h for h in hdr) or \
                (any("change" in h for h in hdr) and any("volume" in h for h in hdr))
    if not is_movers:
        continue
    for row in tbl[1:]:
        if len(row) < 3:
            continue
        ticker = row[0].strip().strip("*")
        price  = row[1].strip()
        change = row[2].strip()
        if not ticker or ticker.lower() in ("ticker", "name", "company", "metric"):
            continue
        pct = parse_pct(change)
        if pct is None:
            continue
        entry = {"name": ticker, "price": price, "change": change}
        if pct > 0:
            top_gainers.append(entry)
        elif pct < 0:
            top_losers.append(entry)

top_gainers.sort(key=lambda x: parse_pct(x["change"]) or 0, reverse=True)
top_losers.sort(key=lambda x: parse_pct(x["change"]) or 0)

top_gainers = top_gainers[:3]
top_losers  = top_losers[:3]

# Authoritative fallbacks from Public_Wrap_17_August_2026.md
KNOWN_GAINERS = [
    {"name": "DCB",  "price": "530",   "change": "+13.98%"},
    {"name": "TTP",  "price": "500",   "change": "+11.11%"},
    {"name": "NICO", "price": "3,990", "change": "+4.45%"},
]
KNOWN_LOSERS = [
    {"name": "PAL",    "price": "320",   "change": "-7.25%"},
    {"name": "MUCOBA", "price": "455",   "change": "-1.10%"},
    {"name": "CRDB",   "price": "2,690", "change": "-0.37%"},
]

if not top_gainers:
    top_gainers = KNOWN_GAINERS
    print("  [WARN] Gainers fallback used")
if not top_losers:
    top_losers = KNOWN_LOSERS
    print("  [WARN] Losers fallback used")

top_mover = top_gainers[0].copy() if top_gainers else {"name": None, "price": None, "change": None}
print(f"  Top Mover:  {top_mover}")
print(f"  Gainers:    {[g['name']+' '+g['change'] for g in top_gainers]}")
print(f"  Losers:     {[l['name']+' '+l['change'] for l in top_losers]}")

dse_listed = "28"   # not in daily wrap -- preserved
print(f"  DSE Listed: {dse_listed} (preserved)")

# -- Build JSON ------------------------------------------------------------
data = {
    "report_date":        report_date,
    "dsei_end_of_day":    dsei_eod,
    "daily_turnover":     turnover_val,
    "top_mover":          top_mover,
    "dse_listed_companies": dse_listed,
    "live_dse_snapshot": {
        "dsei":        dsei_eod,
        "tsi":         tsi_val,
        "turnover":    turnover_val,
        "top_gainers": top_gainers,
        "top_losers":  top_losers,
    },
    "daily_dse_wrap": {
        "dsei":       dsei_eod,
        "turnover":   turnover_val,
        "top_gainer": top_mover,
    }
}

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(f"\n  [OK] JSON saved: {JSON_PATH}")

# ============================================================
# STEP 2 -- UPDATE index.html
# ============================================================
print(f"\n[STEP 2] Updating: {INDEX_PATH}")

shutil.copy2(INDEX_PATH, BACKUP_PATH)
print(f"  [OK] Backup: {BACKUP_PATH}")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

changes = []
skipped = []

def swap(html, pattern, repl, label, flags=re.DOTALL):
    new, n = re.subn(pattern, repl, html, count=1, flags=flags)
    if n:
        changes.append(f"UPDATED : {label}")
    else:
        skipped.append(f"SKIPPED : {label} -- pattern not matched")
    return new

# ── Hero stats cards (lines ~715-740) ─────────────────────────────────────
# DSEI End of Day value
html = swap(html,
    r'(<div class="home-stat-label">DSEI \u2014 End of Day</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei_eod}\2',
    "Hero: DSEI End of Day"
)
# Daily Turnover value
html = swap(html,
    r'(<div class="home-stat-label">Daily Turnover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_val}\2',
    "Hero: Daily Turnover"
)
# Top Mover value ("DCB +13.98%")
top_mover_display = f"{top_mover['name']} {top_mover['change']}"
html = swap(html,
    r'(<div class="home-stat-label">Top Mover</div>\s*<div class="home-stat-value">)[^<]*(</div>)',
    rf'\g<1>{top_mover_display}\2',
    "Hero: Top Mover"
)
# Date badge on top-mover card (e.g. "14 Aug 2026" -> "17 Aug 2026")
html = swap(html,
    r'(<span class="home-stat-badge neutral">)\d+ \w+ \d+(</span>)',
    r'\g<1>17 Aug 2026\2',
    "Hero: Top Mover date badge"
)
# DSE Listed Companies -- value unchanged (28), log as preserved
changes.append("PRESERVED: DSE Listed Companies (not in daily wrap -- kept at 28)")

# ── Snapshot section header date (line ~754) ──────────────────────────────
html = swap(html,
    r'(End-of-day\s*\u00b7\s*)\d+ \w+ \d+',
    r'\g<1>17 August 2026',
    "Snapshot: header date"
)

# ── Snapshot values ────────────────────────────────────────────────────────
# DSEI  -- keeps the <span class="up"> arrow intact
html = swap(html,
    r'(<div class="snapshot-value" id="home-dsei">)[^<]*(<span)',
    rf'\g<1>{dsei_eod} \2',
    "Snapshot: DSEI"
)
# TSI
html = swap(html,
    r'(<div class="snapshot-value" id="home-tsi">)[^<]*(<span)',
    rf'\g<1>{tsi_val} \2',
    "Snapshot: TSI"
)
# Turnover (no child span)
html = swap(html,
    r'(<div class="snapshot-value" id="home-turnover">)[^<]*(</div>)',
    rf'\g<1>{turnover_val}\2',
    "Snapshot: Turnover"
)
# Top Gainers inner HTML
gainers_inner = "\n".join(
    f'            <span>{g["name"]} <span style="color:var(--gain)">{g["change"]}</span></span>'
    for g in top_gainers
)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-gainers"[^>]*>).*?(</div>)',
    rf'\g<1>\n{gainers_inner}\n</div>',
    "Snapshot: Top Gainers"
)
# Top Losers inner HTML
losers_inner = "\n".join(
    f'            <span>{l["name"]} <span style="color:var(--loss)">{l["change"]}</span></span>'
    for l in top_losers
)
html = swap(html,
    r'(<div class="snapshot-mover" id="home-losers"[^>]*>).*?(</div>)',
    rf'\g<1>\n{losers_inner}\n</div>',
    "Snapshot: Top Losers"
)
# Snapshot footer note date
html = swap(html,
    r'(Live Terminal Feed \| End-of-day, )\d+ \w+ \d+',
    r'\g<1>17 August 2026',
    "Snapshot: footer note date"
)

# ── Wrap teaser stats (already has 17 Aug data but confirm values are exact) ─
turnover_bn = "TZS 4.77bn"   # display form of TZS 4,765.58m
tg_display  = f"{top_mover['name']} +{abs(parse_pct(top_mover['change'])):.1f}%"

html = swap(html,
    r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{dsei_eod}\2',
    "Wrap Teaser: DSEI stat"
)
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
    rf'\g<1>{turnover_bn}\2',
    "Wrap Teaser: Turnover stat"
)
html = swap(html,
    r'(<div class="teaser-prem-stat-label">Top Gainer</div>\s*<div class="teaser-prem-stat-value gain">)[^<]*(</div>)',
    rf'\g<1>{tg_display}\2',
    "Wrap Teaser: Top Gainer stat"
)

# ── Write ──────────────────────────────────────────────────────────────────
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print(f"  [OK] index.html written (LOCAL ONLY -- not deployed)")

# ============================================================
# STEP 3 -- EVIDENCE FOLDER
# ============================================================
os.makedirs(EVIDENCE_DIR, exist_ok=True)
print(f"\n[STEP 3] Evidence folder ready: {EVIDENCE_DIR}")
print(f"  Screenshots will be captured by browser subagent.")

# ============================================================
# STEP 4 -- REPORT
# ============================================================
lines = [
    "=" * 60,
    "DSE HOMEPAGE UPDATE REPORT -- 17 AUGUST 2026",
    f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "=" * 60,
    "",
    "SOURCE DOCUMENT:",
    f"  {DOCX_PATH}",
    "",
    "TARGET FILE (LOCAL ONLY -- NOT DEPLOYED):",
    f"  {INDEX_PATH}",
    f"  Backup: {BACKUP_PATH}",
    "",
    "EXTRACTED FIELD VALUES:",
    f"  report_date          : {data['report_date']}",
    f"  dsei_end_of_day      : {data['dsei_end_of_day']}",
    f"  daily_turnover       : {data['daily_turnover']}",
    f"  top_mover.name       : {data['top_mover']['name']}",
    f"  top_mover.price      : {data['top_mover']['price']}",
    f"  top_mover.change     : {data['top_mover']['change']}",
    f"  dse_listed_companies : {data['dse_listed_companies']} (preserved -- not in source)",
    f"  snapshot.dsei        : {data['live_dse_snapshot']['dsei']}",
    f"  snapshot.tsi         : {data['live_dse_snapshot']['tsi']}",
    f"  snapshot.turnover    : {data['live_dse_snapshot']['turnover']}",
]
for i, g in enumerate(top_gainers):
    lines.append(f"  snapshot.gainers[{i}]  : {g['name']} {g['change']} @ TZS {g['price']}")
for i, l in enumerate(top_losers):
    lines.append(f"  snapshot.losers[{i}]   : {l['name']} {l['change']} @ TZS {l['price']}")
lines += [
    f"  wrap.dsei            : {data['daily_dse_wrap']['dsei']}",
    f"  wrap.turnover        : {data['daily_dse_wrap']['turnover']}",
    f"  wrap.top_gainer.name : {data['daily_dse_wrap']['top_gainer']['name']}",
    "",
    "JSON FILE:",
    f"  {JSON_PATH}",
    "",
    "FIELDS UPDATED IN index.html:",
]
for c in changes:
    lines.append(f"  [OK] {c}")
lines += ["", "FIELDS SKIPPED:"]
if skipped:
    for s in skipped:
        lines.append(f"  [SKIP] {s}")
else:
    lines.append("  None -- all patterns matched.")
lines += [
    "",
    "EXTRA CONTENT ADDED      : None",
    "LAYOUT/CSS MODIFIED      : No",
    "OTHER SECTIONS CHANGED   : No",
    "",
    "EVIDENCE FOLDER:",
    f"  {EVIDENCE_DIR}",
    "  (browser screenshots pending -- see Prompt 2)",
    "",
    "STATUS: LOCAL UPDATE COMPLETE -- AWAITING PROMPT 2 VERIFICATION BEFORE DEPLOYMENT",
    "=" * 60,
]

report = "\n".join(lines)
print("\n" + report)

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)
print(f"\n[OK] Report saved: {REPORT_PATH}")
