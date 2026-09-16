import docx

def read_docx(file_path):
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        if para.text.strip():
            print("PARA:", para.text)
    
    for table in doc.tables:
        print("\nTABLE:")
        for row in table.rows:
            row_data = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
            print(" | ".join(row_data))

read_docx(r"C:\Users\tmalu\Documents\Current Prices 11 September 2026.docx")
