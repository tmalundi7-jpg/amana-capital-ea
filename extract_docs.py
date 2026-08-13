import zipfile
import xml.etree.ElementTree as ET
import json
import sys

def extract_docx(path):
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        data = {"text": [], "tables": []}
        
        for p in tree.findall('.//w:p', namespaces):
            texts = [node.text for node in p.findall('.//w:t', namespaces) if node.text]
            p_text = ''.join(texts).strip()
            if p_text:
                data["text"].append(p_text)
                
        for table in tree.findall('.//w:tbl', namespaces):
            table_data = []
            for row in table.findall('.//w:tr', namespaces):
                row_data = []
                for cell in row.findall('.//w:tc', namespaces):
                    texts = [node.text for node in cell.findall('.//w:t', namespaces) if node.text]
                    row_data.append(''.join(texts).strip())
                table_data.append(row_data)
            data["tables"].append(table_data)
            
        return data
    except Exception as e:
        return {"error": str(e)}

prices = extract_docx(r"C:\Users\tmalu\OneDrive\Documents\Current Prices - 3rd July 2026.docx")
wrap = extract_docx(r"C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 3rd July 2026.docx")

with open("extracted_data.json", "w") as f:
    json.dump({"prices": prices, "wrap": wrap}, f, indent=2)

print("Done")
