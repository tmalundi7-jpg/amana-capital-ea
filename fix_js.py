import os

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')
with open('script.min.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{ symbol: 'MBP', marketCap: 65, change: 3.4 }", "{ symbol: 'MBP', marketCap: 65, change: 3.5 }")

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(content)
