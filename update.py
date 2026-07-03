import os

directory = '.'

for root, _, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False
            
            # Inject toggle before mobile-toggle
            if 'id="theme-toggle"' not in content:
                content = content.replace(
                    '<button class="mobile-toggle"',
                    '<button id="theme-toggle" class="theme-toggle" aria-label="Toggle Dark Mode">🌙</button>\n            <button class="mobile-toggle"'
                )
                modified = True
            
            # Inject script before </body>
            if 'theme-toggle.js' not in content:
                content = content.replace(
                    '</body>',
                    '<script src="/js/theme-toggle.js"></script>\n</body>'
                )
                modified = True
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
