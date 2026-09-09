import glob
import re

html_files = glob.glob('*.html')

swup_scripts = '''
    <script src="https://unpkg.com/swup@4"></script>
    <script src="https://unpkg.com/@swup/scripts-plugin@2"></script>
'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
        
    # Replace <main ...> with <main id="swup" class="transition-fade">
    # First, let's normalize all <main> tags.
    # Be careful not to replace </main>
    c = re.sub(r'<main[^>]*>', '<main id="swup" class="transition-fade">', c)
    
    # Add script tags before </body> if they don't exist
    if 'unpkg.com/swup' not in c:
        c = c.replace('</body>', swup_scripts + '</body>')
        
    # Also, we need to ensure that script.min.js is deferred? Wait, SwupScriptsPlugin handles script execution, but it's best if script.js is loaded AFTER Swup scripts.
    # We added the swup scripts right before </body>, so if script.min.js is before </body>, it might be above swup_scripts now.
    # Let's fix that order.
    # Actually, we can just find </body> and insert the swup_scripts right BEFORE script.min.js?
    # Let's remove any existing script.min.js and append it after swup scripts.
    script_tag = ''
    if 'script.min.js' in c:
        m = re.search(r'<script[^>]*src="script\.min\.js[^>]*>\s*</script>', c)
        if m:
            script_tag = m.group(0)
            c = c.replace(script_tag, '')
            
    if 'script.js' in c and not script_tag:
        m = re.search(r'<script[^>]*src="script\.js[^>]*>\s*</script>', c)
        if m:
            script_tag = m.group(0)
            c = c.replace(script_tag, '')

    if script_tag:
        c = c.replace('</body>', script_tag + '\n</body>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)

print("All HTML files updated with Swup container and scripts.")
