content = open('do_update_prices_perfect2.py', 'r', encoding='utf-8').read()
content = content.replace(".replace('', '&minus;')", "")
with open('do_update_prices_perfect3.py', 'w', encoding='utf-8') as f:
    f.write(content)
