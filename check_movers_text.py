content = open('17_main_full.txt', encoding='utf-8').read()
import re
match = re.search(r'<h2.*?>2\. Top Movers</h2>(.*?<table)', content, re.DOTALL)
if match:
    print("Between H2 and Table:")
    print(match.group(1))
