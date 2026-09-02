import re

with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the first arc-row, which should be 02 Sep 2026
pattern = r'<div class="arc-row">.*?02 Sep 2026.*?</div>\s*</div>\s*<div><a class="arc-read".*?</a></div>\s*</div>'
match = re.search(pattern, c, re.DOTALL)
if match:
    c = c[:match.start()] + c[match.end():]
    # clean up any extra blank lines
    c = re.sub(r'\n\s*\n', '\n', c)
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Removed 02 Sep 2026 from archive list.")
else:
    print("Could not find the 02 Sep 2026 block.")

