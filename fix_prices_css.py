with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the broken stylesheet link (- instead of ?)
c = c.replace('href="style.css-v=20260830_final_polish_27"', 'href="style.css?v=20260904_heatmap"')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed stylesheet link in current-prices.html")
print("Has correct link:", 'href="style.css?v=' in c)
