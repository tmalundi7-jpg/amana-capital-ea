import re
import os

with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: Remove duplicate title header box
pattern1 = r'article_html = f\'\'\'<div class=\\"dse-header-box.*?{processed_html}\n\'\'\''
if re.search(pattern1, c, re.DOTALL):
    c = re.sub(pattern1, 'article_html = processed_html', c, flags=re.DOTALL)
else:
    # try without backslashes
    pattern1_no_bs = r'article_html = f\'\'\'<div class="dse-header-box.*?{processed_html}\n\'\'\''
    c = re.sub(pattern1_no_bs, 'article_html = processed_html', c, flags=re.DOTALL)

# Fix 2: Update Section 7 wrapping style
old_sec7_style = 'wrapper[\'style\'] = "background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"'
new_sec7_style = 'wrapper[\'style\'] = "background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;"\n            wrapper[\'class\'] = [] # remove dse-header-box class'
if old_sec7_style in c:
    c = c.replace(old_sec7_style, new_sec7_style)

with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed mammoth_html_wrap.py!")
