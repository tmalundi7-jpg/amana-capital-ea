with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("Thursday\\'s", "Thursday's")

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(html)
