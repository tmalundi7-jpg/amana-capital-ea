import os
import mammoth
from bs4 import BeautifulSoup
import re

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')
docx_path = "C:\\Users\\tmalu\\Documents\\Current Prices 14 September 2026.docx"
with open(docx_path, 'rb') as f:
    res = mammoth.extract_raw_text(f)
    print(res.value)
