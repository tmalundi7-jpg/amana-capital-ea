
with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
start_idx = content.find(start_str)
end_idx = content.find('<div class="table-container">')

print(content[start_idx:start_idx+1000])
