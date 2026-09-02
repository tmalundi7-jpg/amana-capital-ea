import re

with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Add a replacement for \ufffd in the final output
if "final_html = final_html.replace('{{CONTENT}}', article_html)" in c:
    new_code = '''final_html = final_html.replace('{{CONTENT}}', article_html)
    
    # Fix unicode encoding issues (en-dash, etc) that get parsed as replacement characters
    final_html = final_html.replace('\\ufffd', '-')'''
    c = c.replace("final_html = final_html.replace('{{CONTENT}}', article_html)", new_code)
    
    with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated mammoth_html_wrap.py to automatically fix encoding issues.")
else:
    print("Could not find replacement block in mammoth script.")
