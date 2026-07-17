import os
import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Determine the background color based on the body class
    if 'class="bg-navy"' in content or 'class="bg-navy ' in content or "'bg-navy'" in content:
        bg_color = '#0B1D3A' # Navy
    else:
        bg_color = '#FBF7F0' # Cream

    anti_flash_style = f"""
    <style id="anti-flash">
        html {{ background-color: {bg_color} !important; }}
        body {{ background-color: {bg_color} !important; opacity: 0; animation: fadeInPage 0.4s ease-out forwards; }}
        @keyframes fadeInPage {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>
"""

    # Check if we already injected it
    if 'id="anti-flash"' in content:
        content = re.sub(r'<style id="anti-flash">.*?</style>', anti_flash_style.strip(), content, flags=re.DOTALL)
    else:
        # Inject right before </head>
        content = content.replace('</head>', f'{anti_flash_style}</head>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Injected anti-flash and fade-in styles into {len(html_files)} HTML files.")
