import zipfile, re, sys
sys.stdout.reconfigure(encoding='utf-8')

wrap_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 04 September 2026.docx'
prices_path = r'C:\Users\tmalu\Documents\Current Prices 04 September 2026.docx'

def extract_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    text = re.sub(r'<[^>]+>', ' ', xml)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

wrap_text = extract_text(wrap_path)
prices_text = extract_text(prices_path)

print("=== WRAP DOCUMENT (first 8000 chars) ===")
print(wrap_text[:8000])
print("\n\n=== CURRENT PRICES DOCUMENT (first 4000 chars) ===")
print(prices_text[:4000])
