from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
for p in paragraphs:
    if 'Gainers' in p:
        print("FOUND:", repr(p))
