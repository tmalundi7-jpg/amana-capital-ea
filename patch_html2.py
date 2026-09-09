import glob
import re

html_files = glob.glob('*.html')

swup_scripts = '''
    <script src="https://unpkg.com/swup@4"></script>
    <script src="https://unpkg.com/@swup/progress-plugin@3"></script>
    <script src="https://unpkg.com/@swup/preload-plugin@3"></script>
    <script src="https://unpkg.com/@swup/scripts-plugin@2"></script>
'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Remove old injected scripts just in case
    c = re.sub(r'<script src="https://unpkg.com/swup@4"></script>\s*<script src="https://unpkg.com/@swup/scripts-plugin@2"></script>', '', c)
    
    if 'unpkg.com/swup@4' not in c:
        c = c.replace('</body>', swup_scripts + '</body>')
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)

with open('script.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace old swup init
old_init = '''            plugins: [
                new SwupScriptsPlugin({
                    head: true,
                    body: true
                })
            ]'''

new_init = '''            plugins: [
                new SwupScriptsPlugin({ head: true, body: true }),
                new SwupProgressPlugin(),
                new SwupPreloadPlugin()
            ]'''
c = c.replace(old_init, new_init)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(c)

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Swup plugins added")
