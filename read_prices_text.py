from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Current Prices 18 September 2026.docx')
for p in doc.paragraphs:
    print(p.text.strip())
