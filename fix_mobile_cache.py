import glob
import re

files = glob.glob("*.html")
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(f, 'r', encoding='utf-16') as file:
            content = file.read()
    
    # Bump CSS
    content = re.sub(r'style\.css\?v=[^"\'\s>]+', 'style.css?v=20260914_revert_07sep', content)
    # Bump JS
    content = re.sub(r'script\.min\.js\?v=[^"\'\s>]+', 'script.min.js?v=20260914_revert_07sep', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Finished cache bust.")
