import mammoth
from bs4 import BeautifulSoup
docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 18 September 2026.docx'
with open(docx_path, 'rb') as docx_file:
    result = mammoth.convert_to_html(docx_file)
    soup = BeautifulSoup(result.value, 'html.parser')
    print("H1 count:", len(soup.find_all('h1')))
    print("H2 count:", len(soup.find_all('h2')))
    print("H3 count:", len(soup.find_all('h3')))
    print("P count:", len(soup.find_all('p')))
