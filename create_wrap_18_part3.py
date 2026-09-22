import mammoth
from bs4 import BeautifulSoup
docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx'
with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    soup = BeautifulSoup(result.value, 'html.parser')
    for i, p in enumerate(soup.find_all('p')[:10]):
        print(f"[{i}]: {p.get_text()}")
