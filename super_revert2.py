import subprocess
import re
import glob

# Get index.html from 170ca15
old_index = subprocess.check_output(['git', 'show', '170ca15:index.html']).decode('utf-8')

# Extract the SNAPSHOT_CARD block from old index
old_snap_block = re.search(r'<!-- SNAPSHOT_CARD_START -->.*?<!-- SNAPSHOT_CARD_END -->', old_index, flags=re.DOTALL).group(0)

# Replace in current index
with open('index.html', 'r', encoding='utf-8') as f:
    curr_index = f.read()
curr_index = re.sub(r'<!-- SNAPSHOT_CARD_START -->.*?<!-- SNAPSHOT_CARD_END -->', old_snap_block, curr_index, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(curr_index)

# Bump cache
html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mega_revert', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Restored HTML for index snapshot. Cache bumped on {bumped} files.")
