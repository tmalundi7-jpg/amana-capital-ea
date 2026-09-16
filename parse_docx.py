import zipfile
import xml.etree.ElementTree as ET
import os

files = [
    "C:\\Users\\tmalu\\Documents\\Daily DSE Wrap 07 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Daily DSE Wrap 08 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Daily DSE Wrap 09 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Daily DSE Wrap 10 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Daily DSE Wrap 11 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Current Prices 07 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Current Prices 08 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Current Prices 09 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Current Prices 10 September 2026.docx",
    "C:\\Users\\tmalu\\Documents\\Current Prices 11 September 2026.docx"
]

def extract_text(filepath):
    try:
        with zipfile.ZipFile(filepath) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        paragraphs = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error reading {filepath}: {e}"

with open("extracted_week.txt", "w", encoding="utf-8") as out:
    for file in files:
        out.write(f"--- {os.path.basename(file)} ---\n")
        out.write(extract_text(file))
        out.write("\n\n")

print("Extraction complete.")
