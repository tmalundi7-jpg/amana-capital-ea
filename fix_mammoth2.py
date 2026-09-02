import re
c = open('mammoth_html_wrap.py', 'r', encoding='utf-8').read()
c = re.sub(r'article_html = f\'\'\'<div class=\\"dse-header-box.*?}processed_html}\n\'\'\'', 'article_html = processed_html', c, flags=re.DOTALL)
open('mammoth_html_wrap.py', 'w', encoding='utf-8').write(c)
print('Fixed mammoth_html_wrap.py')
