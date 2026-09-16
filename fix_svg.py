with open('current-prices.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<svg aria-hidden="true" class="brand-icon" viewbox="0 0 32 44">', '<svg aria-hidden="true" class="brand-icon" viewBox="0 0 32 44" height="36" width="26">')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated current-prices.html SVG")
