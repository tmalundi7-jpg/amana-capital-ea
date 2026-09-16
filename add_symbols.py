import os

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')
with open('script.min.js', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''        { symbol: 'MBP', marketCap: 65, change: 3.5 },
        { symbol: 'MCB', marketCap: 62, change: 1.3 },
        { symbol: 'TTP', marketCap: 110, change: -5.6 },
        { symbol: 'MUCOBA', marketCap: 14, change: -4.3 },
        { symbol: 'NMG', marketCap: 50, change: 0.0 }'''

content = content.replace('''        { symbol: 'MBP', marketCap: 65, change: 3.5 },
        { symbol: 'MCB', marketCap: 62, change: 1.3 },
        { symbol: 'NMG', marketCap: 50, change: 0.0 }''', replacement)

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(content)
