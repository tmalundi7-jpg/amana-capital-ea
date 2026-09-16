import sys
import zipfile
import xml.etree.ElementTree as ET

def read_docx(path):
    with zipfile.ZipFile(path) as docx:
        xml_content = docx.read('word/document.xml')
        tree = ET.XML(xml_content)
        # Extract text from w:t elements
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        texts = [node.text for node in tree.findall('.//w:t', ns) if node.text]
        return ''.join(texts)

print("Wrap:", len(read_docx(r"C:\Users\tmalu\Documents\Daily DSE Wrap 11 September 2026.docx")))
print("Prices:", len(read_docx(r"C:\Users\tmalu\Documents\Current Prices 11 September 2026.docx")))
