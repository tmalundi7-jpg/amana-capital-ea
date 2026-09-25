from docx import Document

doc = Document(r"C:\Users\tmalu\Documents\Current Prices 25 September 2026.docx")
for table in doc.tables:
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        print(" | ".join(cells))
