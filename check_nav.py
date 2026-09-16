import glob

def get_nav(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    start = content.find('<nav class="navbar">')
    end = content.find('</nav>')
    if start != -1 and end != -1:
        return content[start:end+6]
    return None

index_nav = get_nav('index.html')
print(f'index_nav length: {len(index_nav) if index_nav else 0}')

diff_count = 0
for file in glob.glob('**/*.html', recursive=True):
    nav = get_nav(file)
    if nav and nav != index_nav:
        print(f'Diff in {file}')
        diff_count += 1
print(f'Total differing headers: {diff_count}')
