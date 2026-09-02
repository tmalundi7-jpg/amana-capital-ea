with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    c = f.read()

start_idx = c.find('<div class="arc-row">')
end_idx = c.find('<div class="arc-row">', start_idx + 1)

first_row = c[start_idx:end_idx]

if '02 Sep 2026' in first_row:
    c = c[:start_idx] + c[end_idx:]
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully removed the 02 Sep 2026 row!")
else:
    print("The first row does not contain 02 Sep 2026.")
