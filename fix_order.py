import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # We want to extract the swup scripts
    m1 = re.search(r'<script src="https://unpkg.com/swup@4"></script>', c)
    if not m1: continue
    
    # Remove them
    c = re.sub(r'\s*<script src="https://unpkg.com/swup@4"></script>', '', c)
    c = re.sub(r'\s*<script src="https://unpkg.com/@swup/progress-plugin@3"></script>', '', c)
    c = re.sub(r'\s*<script src="https://unpkg.com/@swup/preload-plugin@3"></script>', '', c)
    c = re.sub(r'\s*<script src="https://unpkg.com/@swup/scripts-plugin@2"></script>', '', c)
    
    swup_scripts = '''
    <script src="https://unpkg.com/swup@4"></script>
    <script src="https://unpkg.com/@swup/progress-plugin@3"></script>
    <script src="https://unpkg.com/@swup/preload-plugin@3"></script>
    <script src="https://unpkg.com/@swup/scripts-plugin@2"></script>
    '''
    
    # Find script.min.js
    if 'script.min.js' in c:
        # replace the script tag with swup + script.min.js
        c = re.sub(r'(<script[^>]*script\.min\.js[^>]*>\s*</script>)', swup_scripts + r'\1', c)
    elif 'script.js' in c:
        c = re.sub(r'(<script[^>]*script\.js[^>]*>\s*</script>)', swup_scripts + r'\1', c)
    else:
        c = c.replace('</body>', swup_scripts + '</body>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)

print("Re-ordered Swup scripts to be before script.min.js")
