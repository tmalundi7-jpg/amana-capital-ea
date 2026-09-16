import glob
import re
import os

files = glob.glob("*.html")
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated = re.sub(r'style\.css\?v=[^"\'\s>]+', 'style.css?v=20260914_mobile_fix', content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(updated)
    except Exception as e:
        print(f"Failed to process {f} as utf-8. Trying utf-16.")
        with open(f, 'r', encoding='utf-16') as file:
            content = file.read()
        
        updated = re.sub(r'style\.css\?v=[^"\'\s>]+', 'style.css?v=20260914_mobile_fix', content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(updated)

print("Finished CSS cache bust.")
