import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

toggle = """<!-- ============================================ -->
<!-- THEME TOGGLE (Dark/Light Mode)              -->
<!-- ============================================ -->
<button id="themeToggle" class="theme-toggle" aria-label="Toggle dark/light mode" title="Toggle theme">
  <span class="theme-icon-dark" aria-hidden="true">🌙</span>
  <span class="theme-icon-light" aria-hidden="true" style="display: none;">☀️</span>
</button>
"""

# Remove toggle from wherever it currently is
content = content.replace(toggle, '')

# Add it right before the mobile-toggle button
target = '<button aria-label="Open menu" class="mobile-toggle" id="mobile-toggle">&#9776;</button>'
replacement = toggle + target

if target in content:
    content = content.replace(target, replacement)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully moved theme-toggle!")
else:
    print("Could not find mobile-toggle to place the theme-toggle.")
