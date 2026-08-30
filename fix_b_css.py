import re, shutil

print("=== FIX B: Regenerate style.min.css & fix encoding ===")

# Read style.css
with open('style.css', 'r', encoding='utf-8', errors='replace') as f:
    css = f.read()

# Fix replacement chars
css_fixed = css.replace('\ufffd', '-')

# Write cleaned style.css back
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css_fixed)

print("style.css: encoding fixed")

# Minify CSS (basic minification - remove comments, extra spaces, newlines)
# Remove block comments
mini = re.sub(r'/\*.*?\*/', '', css_fixed, flags=re.DOTALL)
# Remove single-line comments
mini = re.sub(r'//.*?\n', '\n', mini)
# Collapse whitespace
mini = re.sub(r'\s+', ' ', mini)
# Remove spaces around delimiters
mini = re.sub(r'\s*([{}:;,>~+])\s*', r'\1', mini)
# Remove trailing/leading whitespace
mini = mini.strip()

# Backup old min
shutil.copy('style.min.css', 'style.min.css.bak')

with open('style.min.css', 'w', encoding='utf-8') as f:
    f.write(mini)

print(f"style.min.css regenerated: {len(mini)} bytes (was: {len(css)} original)")
print("Done.")
