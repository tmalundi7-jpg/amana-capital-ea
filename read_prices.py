from docx import Document

doc = Document(r'C:\Users\tmalu\Documents\Current Prices 18 September 2026.docx')

for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        print(cells)

