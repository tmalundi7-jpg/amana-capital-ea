import re

with open('dse-wrap-2026-08-24.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title
template = re.sub(r'<title>.*?</title>', '<title>Daily DSE Wrap | {{DATE_STRING}} | Amana Capital East Africa</title>', template)
# Replace canonical
template = re.sub(r'dse-wrap-2026-08-24\.html', 'dse-wrap-{{YYYY_MM_DD}}.html', template)
# Replace description
template = re.sub(r'content=\"Read our daily Dar es Salaam Stock Exchange \(DSE\) wrap for 24 August 2026\.', 'content=\"Read our daily Dar es Salaam Stock Exchange (DSE) wrap for {{DATE_STRING}}.', template)

# Replace the specific header and body
# We want to replace everything from <div class=\"dse-header-box\" down to just before <div class=\"article-disclaimer\"
def repl_body(m):
    return '''<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">Daily DSE Wrap | {{DATE_STRING}}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{{SUBTITLE}}</p>
</div>

{{CONTENT}}

'''

template = re.sub(r'<div class="dse-header-box".*?(?=<div class="article-disclaimer")', repl_body, template, flags=re.DOTALL)

with open('templates/wrap_template.html', 'w', encoding='utf-8') as f:
    f.write(template)

print('Updated templates/wrap_template.html')
