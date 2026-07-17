import os
import glob

def update_html():
    html_files = glob.glob('*.html')
    for file in html_files:
        with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
            content = f.read()
        
        # 1. Update main tag to Swup container
        if '<main id="swup"' not in content:
            content = content.replace('<main>', '<main id="swup" class="transition-fade">')
        
        # 2. Remove old bond calculator script tags
        content = content.replace('<script src="/js/bond-calculator.js"></script>', '')
        content = content.replace('<script src="js/bond-calculator.js"></script>', '')
        
        # 3. Insert Swup CDN before script.js if not already present
        if 'unpkg.com/swup' not in content:
            content = content.replace('<script src="script.js"></script>', '<script src="https://unpkg.com/swup@4"></script>\n    <script src="script.js"></script>')

        with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
            f.write(content)
            
    print(f"Successfully updated {len(html_files)} HTML files for Swup transitions.")

if __name__ == '__main__':
    update_html()
