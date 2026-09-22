import docx

doc = docx.Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 21 September 2026.docx')
for p in doc.paragraphs:
    print(p.text)
