with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('id="mi-turnover">10.20 bn</div>', 'id="mi-turnover">TZS 10.20 bn</div>')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)
