import sys, zipfile, xml.etree.ElementTree as ET, json
sys.stdout.reconfigure(encoding="utf-8")

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def dump_docx(path):
    items = []
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    body = ET.XML(xml).find(f".//{{{NS}}}body")
    for child in body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            t = "".join(r.text for r in child.findall(f".//{{{NS}}}t") if r.text).strip()
            if t:
                items.append({"type": "para", "text": t})
        elif tag == "tbl":
            rows = []
            for tr in child.findall(f".//{{{NS}}}tr"):
                row = ["".join(r.text for r in tc.findall(f".//{{{NS}}}t") if r.text).strip()
                       for tc in tr.findall(f".//{{{NS}}}tc")]
                if any(row):
                    rows.append(row)
            if rows:
                items.append({"type": "table", "rows": rows})
    return items

wrap_path  = r"C:\Users\tmalu\Documents\Daily DSE Wrap 17 August 2026.docx"
prices_path = r"C:\Users\tmalu\Documents\Current Prices 17 August 2026.docx"

wrap_items  = dump_docx(wrap_path)
prices_items = dump_docx(prices_path)

with open("_raw_wrap_17aug.json", "w", encoding="utf-8") as f:
    json.dump(wrap_items, f, indent=2, ensure_ascii=False)

with open("_raw_prices_17aug.json", "w", encoding="utf-8") as f:
    json.dump(prices_items, f, indent=2, ensure_ascii=False)

print(f"Wrap  items: {len(wrap_items)}")
print(f"Prices items: {len(prices_items)}")

# Print summary of tables found
print("\n--- WRAP TABLES ---")
for i, item in enumerate(wrap_items):
    if item["type"] == "table":
        print(f"Table #{i}: {len(item['rows'])} rows")
        for r in item["rows"][:3]:
            print(f"   {r}")
        if len(item["rows"]) > 3:
            print(f"   ... ({len(item['rows'])-3} more rows)")

print("\n--- PRICES TABLES ---")
for i, item in enumerate(prices_items):
    if item["type"] == "table":
        print(f"Table #{i}: {len(item['rows'])} rows")
        for r in item["rows"][:5]:
            print(f"   {r}")
        if len(item["rows"]) > 5:
            print(f"   ... ({len(item['rows'])-5} more rows)")

print("\n--- WRAP PARAGRAPHS (first 15) ---")
for item in wrap_items[:15]:
    if item["type"] == "para":
        print(f"  PARA: {item['text'][:120]}")
