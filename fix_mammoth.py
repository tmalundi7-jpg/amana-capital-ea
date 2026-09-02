import re

with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the article_html generation
old_code = '''    # Create the full article HTML
    article_html = f\'\'\'<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">{title}</h1>
                    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{subtitle}</p>
                </div>
                {processed_html}
\'\'\'

    template_path = os.path.join("templates", "wrap_template.html")'''

new_code = '''    # The template already has the header box, so just pass the processed HTML
    article_html = processed_html

    template_path = os.path.join("templates", "wrap_template.html")'''

if old_code in c:
    c = c.replace(old_code, new_code)
    with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed mammoth_html_wrap.py header box duplication!")
else:
    print("Could not find the old code block in mammoth_html_wrap.py.")
