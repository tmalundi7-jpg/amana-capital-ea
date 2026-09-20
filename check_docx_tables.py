from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')
for i, table in enumerate(doc.tables):
    print(f'--- Table {i} ---')
    for row in table.rows[:3]:
        print([cell.text.strip() for cell in row.cells])
