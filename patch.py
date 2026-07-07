import os

directory = '.'

for root, _, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if '??</button>' in content:
                content = content.replace('??</button>', '🌙</button>')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
