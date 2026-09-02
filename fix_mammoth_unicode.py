with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("replace('\\\\ufffd', '-')", "replace('\\ufffd', '—').replace('\\xa0', ' ')")

with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
    f.write(c)
