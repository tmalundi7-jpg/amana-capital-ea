
with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
start_idx = content.find(start_str)
end_idx = content.find('<div class="table-container">')

if start_idx != -1 and end_idx != -1:
    print(repr(content[end_idx-30:end_idx+30]))
