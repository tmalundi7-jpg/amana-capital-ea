def update_hero():
    with open('market-intelligence.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('<strong>07 Sep 2026</strong>\n                        Latest Report', '<strong>14 Sep 2026</strong>\n                        Latest Report')

    with open('market-intelligence.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Hero updated.")

update_hero()
