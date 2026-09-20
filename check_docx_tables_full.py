from docx import Document
doc = Document(r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx')
for i, table in enumerate(doc.tables[:4]):
    print(f'--- Table {i} ---')
    for row in table.rows:
        print([cell.text.strip().replace('\n', ' ') for cell in row.cells])
