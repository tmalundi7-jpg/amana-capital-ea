import os
os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<div class="archive-date">14 Sep<br/>2026</div>', '<div class="archive-date">15 Sep<br/>2026</div>')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(text)
