import re
from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

i = 0
while i < len(paragraphs):
    if 'Gainers' in paragraphs[i]:
        print("At i =", i, "found Gainers")
    i += 1
