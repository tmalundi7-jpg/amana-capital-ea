content = open('dse-wrap-2026-09-17.html', encoding='utf-8').read()
import re
print("H1 matches:", re.findall(r'<h1.*?>', content))
print("Divs with article:", re.findall(r'<div[^>]*class=["\'][^"\']*article[^"\']*["\'][^>]*>', content))
