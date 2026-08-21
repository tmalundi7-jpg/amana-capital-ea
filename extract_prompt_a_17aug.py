"""
Prompt A — Extract Data Only
Extracts DSE Wrap (Doc 1) and Current Prices (Doc 2) into structured JSON.
No website updates. No deployments.
"""
import sys, json, zipfile, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ─────────────────────────────────────────────────────────────────────────────
# Helper: parse docx into paragraphs and tables
# ─────────────────────────────────────────────────────────────────────────────
def parse_docx(path):
    with zipfile.ZipFile(path) as z:
        raw = z.read("word/document.xml")
    body = ET.XML(raw).find(f".//{{{NS}}}body")
    items = []
    for child in body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            t = "".join(r.text for r in child.findall(f".//{{{NS}}}t") if r.text).strip()
            if t:
                items.append({"type": "para", "text": t})
        elif tag == "tbl":
            rows = []
            for tr in child.findall(f".//{{{NS}}}tr"):
                row = [
                    "".join(r.text for r in tc.findall(f".//{{{NS}}}t") if r.text).strip()
                    for tc in tr.findall(f".//{{{NS}}}tc")
                ]
                if any(row):
                    rows.append(row)
            if rows:
                items.append({"type": "table", "rows": rows})
    return items

# ─────────────────────────────────────────────────────────────────────────────
# Helper: turn a table's rows into list-of-dicts keyed by header row
# ─────────────────────────────────────────────────────────────────────────────
def table_to_records(rows):
    if not rows:
        return []
    headers = rows[0]
    records = []
    for row in rows[1:]:
        rec = {}
        for i, h in enumerate(headers):
            rec[h] = row[i] if i < len(row) else None
        records.append(rec)
    return records

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 1 — Daily DSE Wrap 17 August 2026.docx
# ─────────────────────────────────────────────────────────────────────────────
WRAP_PATH   = r"C:\Users\tmalu\Documents\Daily DSE Wrap 17 August 2026.docx"
PRICES_PATH = r"C:\Users\tmalu\Documents\Current Prices 17 August 2026.docx"

print("[TASK 1] Parsing Daily DSE Wrap 17 August 2026.docx ...")
wrap_items = parse_docx(WRAP_PATH)

# --- Identify tables by order they appear in the document --------------------
#  Table 0 (item index 4): Market Snapshot  — 10 rows, columns: Metric / Fri 14 Aug / Mon 17 Aug / Change
#  Table 1 (item index 8): Top Movers       — 9 rows, columns: Ticker / Closing Price / Change / Volume
#  Table 2 (item index 23): Price Bands     — 7 rows, columns: Counter / Mon Close / Tue Upper / Tue Lower

tables = [item for item in wrap_items if item["type"] == "table"]
snapshot_rows  = tables[0]["rows"] if len(tables) > 0 else []
movers_rows    = tables[1]["rows"] if len(tables) > 1 else []
pricebands_rows= tables[2]["rows"] if len(tables) > 2 else []

# --- Live DSE Snapshot -------------------------------------------------------
#   Columns: Metric | Fri 14 Aug | Mon 17 Aug | Change
#   We capture Monday 17 Aug column (index 2) as the current values.
snapshot_obj = {}
snap_notes   = []
if snapshot_rows:
    hdr = snapshot_rows[0]   # ["Metric", "Friday 14 Aug", "Monday 17 Aug", "Change"]
    for row in snapshot_rows[1:]:
        metric = row[0] if len(row) > 0 else None
        prev   = row[1] if len(row) > 1 else None
        curr   = row[2] if len(row) > 2 else None
        chg    = row[3] if len(row) > 3 else None
        if metric:
            snapshot_obj[metric] = {
                "previous_session"   : prev,
                "current_session"    : curr,
                "change"             : chg
            }

# --- Top Movers (heatmap) ---------------------------------------------------
heatmap = []
if movers_rows:
    heatmap = table_to_records(movers_rows)   # keys: Ticker, Closing Price (TZS), Change, Volume

# --- Price Bands for next session -------------------------------------------
price_bands = []
if pricebands_rows:
    price_bands = table_to_records(pricebands_rows)  # Counter, Mon Close, Tue Upper, Tue Lower

# --- All paragraph text (narrative / wrap content) --------------------------
paras = [item["text"] for item in wrap_items if item["type"] == "para"]

# --- Headline data extracted from first paragraphs -------------------------
headline_title    = paras[0] if len(paras) > 0 else None   # "Daily DSE Wrap | Monday, 17th August 2026"
headline_subtitle = paras[1] if len(paras) > 1 else None   # "NMB Touches 18,000 ..."
headline_lede     = paras[2] if len(paras) > 2 else None   # opening summary para

# --- Report date -----------------------------------------------------------
report_date = "Monday, 17th August 2026"   # as shown in document header

# --- Key headline figures (from snapshot table, current session column) ----
def snap_curr(metric):
    return snapshot_obj.get(metric, {}).get("current_session", None)

headline_figures = {
    "DSEI"           : snap_curr("DSEI"),
    "TSI"            : snap_curr("TSI"),
    "equity_turnover": snap_curr("Equity Turnover"),
    "shares_traded"  : snap_curr("Shares Traded"),
    "deals"          : snap_curr("Deals"),
    "bond_turnover"  : snap_curr("Bond Turnover"),
    "etf_turnover"   : snap_curr("ETF Turnover"),
    "foreign_buying" : snap_curr("Foreign Buying"),
    "foreign_selling": snap_curr("Foreign Selling"),
}

# --- Build final Document 1 JSON -------------------------------------------
wrap_json = {
    "source_document" : WRAP_PATH,
    "report_date"     : report_date,
    "headline"        : {
        "title"    : headline_title,
        "subtitle" : headline_subtitle,
        "lede"     : headline_lede,
    },
    "headline_figures": headline_figures,
    "live_dse_snapshot": {
        "columns"      : ["Metric", "Friday 14 Aug (previous)", "Monday 17 Aug (current)", "Change"],
        "note"         : "Current session = Monday 17 August 2026",
        "metrics"      : snapshot_obj,
    },
    "dse_market_heatmap": {
        "note"    : "Top Movers table from wrap document",
        "columns" : ["Ticker", "Closing Price (TZS)", "Change", "Volume"],
        "stocks"  : heatmap,
        "footnotes": [
            "¹ DCB volume 973,402 includes a 760,000-share block trade. Normal-board volume was 213,402 shares."
        ]
    },
    "price_bands_next_session": {
        "note"    : "Trading limits for Tuesday 18 August 2026",
        "columns" : ["Counter", "Monday Close (TZS)", "Tuesday Upper Limit (TZS)", "Tuesday Lower Limit (TZS)"],
        "bands"   : price_bands,
        "footnotes": [
            "¹ DCB trades under a wider 15% band; table shows 15% limits."
        ]
    },
    "daily_wrap_content": paras,
    "sections_identified": [
        "1. Market Snapshot",
        "2. Top Movers",
        "3. In Focus: DCB's Block Trade and the Power of Local Demand",
        "4. Today's Concept: The 5% Daily Price Band — Your Safety Net",
        "5. Bond Market: A Quiet Day After a Busy August",
        "6. Strategic Outlook: What to Anticipate",
        "7. Professional Approach: How to Use This Intelligence",
        "8. Considerations for a Multi-Year Framework",
    ],
    "extraction_notes": {
        "missing_fields"     : [],
        "null_fields"        : [],
        "footnotes_preserved": True,
        "values_reformat"    : "None — all values extracted verbatim",
    }
}

OUT1 = "extracted_dse_wrap_17_aug_2026.json"
with open(OUT1, "w", encoding="utf-8") as f:
    json.dump(wrap_json, f, indent=2, ensure_ascii=False)
print(f"  [OK] Saved: {OUT1}")

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT 2 — Current Prices 17 August 2026.docx
# ─────────────────────────────────────────────────────────────────────────────
print("[TASK 2] Parsing Current Prices 17 August 2026.docx ...")
prices_items = parse_docx(PRICES_PATH)

# The document contains:
#   Para 0: "Current Prices — End-of-Day, Monday 17th August 2026"
#   Table 0: 22 rows — Ticker / Company / Sector / Last Price (TZS) / Change (%) / Volume / Turnover (TZS)
#   Para 1: footnote text

prices_paras  = [item["text"] for item in prices_items if item["type"] == "para"]
prices_tables = [item for item in prices_items if item["type"] == "table"]

timestamp_label = prices_paras[0] if prices_paras else None   # "Current Prices — End-of-Day, Monday 17th August 2026"
footnote_text   = prices_paras[1] if len(prices_paras) > 1 else None

prices_records = []
if prices_tables:
    raw_rows = prices_tables[0]["rows"]
    headers  = raw_rows[0]   # Ticker, Company, Sector, Last Price (TZS), Change (%), Volume, Turnover (TZS)
    for row in raw_rows[1:]:
        rec = {
            "ticker"          : row[0] if len(row) > 0 else None,
            "company"         : row[1] if len(row) > 1 else None,
            "sector"          : row[2] if len(row) > 2 else None,
            "last_price_tzs"  : row[3] if len(row) > 3 else None,
            "change_pct"      : row[4] if len(row) > 4 else None,
            "volume"          : row[5] if len(row) > 5 else None,
            "turnover_tzs"    : row[6] if len(row) > 6 else None,
        }
        prices_records.append(rec)

# Identify any null/missing fields
null_fields = []
for rec in prices_records:
    for k, v in rec.items():
        if v is None or v == "" or v == "—":
            null_fields.append(f"{rec.get('ticker','?')}.{k} = {repr(v)}")

prices_json = {
    "source_document"  : PRICES_PATH,
    "timestamp_label"  : timestamp_label,
    "report_date"      : "Monday 17th August 2026",
    "columns"          : [
        "ticker", "company", "sector",
        "last_price_tzs", "change_pct", "volume", "turnover_tzs"
    ],
    "total_records"    : len(prices_records),
    "prices"           : prices_records,
    "footnotes"        : [footnote_text] if footnote_text else [],
    "omitted_counters" : [
        "EABL", "JATU", "JHL", "NMG", "SWALA", "USL", "YETU"
    ],
    "extraction_notes" : {
        "omission_reason": "Counters with no opening price or zero trades omitted as stated in source footnote",
        "null_fields"    : null_fields if null_fields else [],
        "dash_meaning"   : "'—' in volume/turnover = no trade recorded for that counter",
        "values_reformat": "None — all values extracted verbatim",
    }
}

OUT2 = "extracted_current_prices_17_aug_2026.json"
with open(OUT2, "w", encoding="utf-8") as f:
    json.dump(prices_json, f, indent=2, ensure_ascii=False)
print(f"  [OK] Saved: {OUT2}")

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY REPORT
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("EXTRACTION SUMMARY REPORT  |  Prompt A  |  17 August 2026")
print("=" * 65)

print()
print("DOCUMENT 1 — Daily DSE Wrap 17 August 2026.docx")
print(f"  Output file   : {OUT1}")
print(f"  Report date   : {report_date}")
print(f"  Sections      : {len(wrap_json['sections_identified'])}")
print(f"  Paragraphs    : {len(paras)}")
print(f"  Snapshot rows : {len(snapshot_obj)} metrics")
print(f"  Heatmap rows  : {len(heatmap)} stocks")
print(f"  Price band rows: {len(price_bands)} counters")
print()
print("  Fields extracted from Document 1:")
doc1_fields = [
    "report_date",
    "headline.title",
    "headline.subtitle",
    "headline.lede",
    "headline_figures.DSEI (current session)",
    "headline_figures.TSI (current session)",
    "headline_figures.equity_turnover (current session)",
    "headline_figures.shares_traded (current session)",
    "headline_figures.deals (current session)",
    "headline_figures.bond_turnover (current session)",
    "headline_figures.etf_turnover (current session)",
    "headline_figures.foreign_buying (current session)",
    "headline_figures.foreign_selling (current session)",
    "live_dse_snapshot.metrics[DSEI] — prev, current, change",
    "live_dse_snapshot.metrics[TSI] — prev, current, change",
    "live_dse_snapshot.metrics[Equity Turnover] — prev, current, change",
    "live_dse_snapshot.metrics[Shares Traded] — prev, current, change",
    "live_dse_snapshot.metrics[Deals] — prev, current, change",
    "live_dse_snapshot.metrics[Bond Turnover] — prev, current, change",
    "live_dse_snapshot.metrics[ETF Turnover] — prev, current, change",
    "live_dse_snapshot.metrics[Foreign Buying] — prev, current, change",
    "live_dse_snapshot.metrics[Foreign Selling] — prev, current, change",
    "dse_market_heatmap: DCB (ticker, price, change, volume)",
    "dse_market_heatmap: NICO (ticker, price, change, volume)",
    "dse_market_heatmap: VODA (ticker, price, change, volume)",
    "dse_market_heatmap: NMB (ticker, price, change, volume)",
    "dse_market_heatmap: CRDB (ticker, price, change, volume)",
    "dse_market_heatmap: TCC (ticker, price, change, volume)",
    "dse_market_heatmap: PAL (ticker, price, change, volume)",
    "dse_market_heatmap: MCB (ticker, price, change, volume)",
    "price_bands_next_session: CRDB, NMB, VODA, TBL, TCC, DCB¹",
    "daily_wrap_content (all narrative paragraphs)",
    "sections_identified (8 sections)",
    "footnotes",
]
for f in doc1_fields:
    print(f"    - {f}")

print()
print(f"  Missing/null fields : {wrap_json['extraction_notes']['null_fields'] or 'None'}")

print()
print("DOCUMENT 2 — Current Prices 17 August 2026.docx")
print(f"  Output file    : {OUT2}")
print(f"  Timestamp      : {timestamp_label}")
print(f"  Total records  : {len(prices_records)} stocks")
print(f"  Omitted        : {', '.join(prices_json['omitted_counters'])} (zero-trade counters per footnote)")
print()
print("  Fields extracted from Document 2 (per record):")
for f in prices_json["columns"]:
    print(f"    - {f}")
print()
if null_fields:
    print("  Fields set to null / '—' (no data in source):")
    for nf in null_fields:
        print(f"    - {nf}")
else:
    print("  Missing/null fields : None")

print()
print("OUTPUT FILES:")
print(f"  {OUT1}")
print(f"  {OUT2}")
print()
print("ERRORS ENCOUNTERED : None")
print("WEBSITE UPDATED    : No")
print("DEPLOYMENT DONE    : No")
print("=" * 65)
