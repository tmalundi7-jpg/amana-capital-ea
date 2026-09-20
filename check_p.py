from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')
for i, p in enumerate(doc.paragraphs[:20]):
    print(f"[{i}] {p.text.strip()}")
