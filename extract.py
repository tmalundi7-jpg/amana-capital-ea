import zipfile
import xml.etree.ElementTree as ET
import os

def extract_docx_text(docx_path):
    text_content = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as docx_zip:
            xml_content = docx_zip.read('word/document.xml')
            tree = ET.XML(xml_content)
            
            # The namespace for WordProcessingML
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Iterate through paragraphs and tables
            for element in tree.iter():
                # Paragraphs
                if element.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                    para_text = []
                    for run in element.findall('.//w:t', namespace):
                        if run.text:
                            para_text.append(run.text)
                    if para_text:
                        text_content.append(''.join(para_text))
                
                # Tables
                if element.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl':
                    text_content.append("--- TABLE START ---")
                    for row in element.findall('.//w:tr', namespace):
                        row_data = []
                        for cell in row.findall('.//w:tc', namespace):
                            cell_text = []
                            for run in cell.findall('.//w:t', namespace):
                                if run.text:
                                    cell_text.append(run.text)
                            row_data.append(''.join(cell_text))
                        text_content.append(' | '.join(row_data))
                    text_content.append("--- TABLE END ---")
    except Exception as e:
        return f"Error extracting {docx_path}: {e}"
    
    return '\n'.join(text_content)

file1 = r"C:\Users\tmalu\OneDrive\Documents\Current Prices - 3rd July 2026.docx"
file2 = r"C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap - 3rd July 2026.docx"
file3 = r"C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 3rd July 2026.docx"

out_file = r"C:\Users\tmalu\.gemini\antigravity\scratch\docx_data.txt"

with open(out_file, "w", encoding="utf-8") as f:
    f.write(f"=== {file1} ===\n")
    if os.path.exists(file1):
        f.write(extract_docx_text(file1))
    else:
        f.write("FILE NOT FOUND")
        
    f.write(f"\n\n=== {file2} ===\n")
    if os.path.exists(file2):
        f.write(extract_docx_text(file2))
    else:
        f.write("FILE NOT FOUND")

    f.write(f"\n\n=== {file3} ===\n")
    if os.path.exists(file3):
        f.write(extract_docx_text(file3))
    else:
        f.write("FILE NOT FOUND")
        
print("Extraction complete. Wrote to docx_data.txt")
