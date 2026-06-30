import os
import re

pattern = re.compile(r'losses\s+(?:â€”|—|â€"|-)\s+including\s+the\s+total\s+loss\s+of\s+your\s+invested\s+capital\s+(?:â€”|—|â€"|-)\s+which\s+you\s+alone\s+will\s+bear\.?', re.DOTALL)
replacement = 'losses including the total loss of your invested capital which you alone will bear.'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                continue
            
            changed = False
            if pattern.search(content):
                content = pattern.sub(replacement, content)
                changed = True
            
            if 'â€”' in content:
                content = content.replace('â€”', '-')
                changed = True
                
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filepath}")
