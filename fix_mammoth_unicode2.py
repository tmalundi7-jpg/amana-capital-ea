with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

# I will just add the correct replace statements right before "output_path ="
inject = '''
    final_html = final_html.replace('\\ufffd', '—')
    final_html = final_html.replace('\\xa0', ' ')
    output_path =
'''

c = c.replace('output_path =', inject.strip() + ' ')

with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
    f.write(c)
