import re

# Read 24th Aug as template
with open('dse-wrap-2026-08-24.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Read the current content from 1st Sep
with open('dse-wrap-2026-09-01.html', 'r', encoding='utf-8') as f:
    sep1_content = f.read()

# Extract the header box and article content from 1st Sep
m = re.search(r'(<div class="dse-header-box".*?</div>\s*<p>The Dar es Salaam Stock Exchange.*?)<div class="article-disclaimer"', sep1_content, flags=re.DOTALL)
if not m:
    print('Failed to extract content')
    exit(1)
article_body = m.group(1)

# Replace the content in the template
def repl_body(m):
    return article_body

template = re.sub(r'(<div class="dse-header-box".*?</div>\s*<p>The Dar es Salaam Stock Exchange.*?)<div class="article-disclaimer"', repl_body, template, flags=re.DOTALL)

# Update title and canonical link
template = re.sub(r'<title>.*?</title>', '<title>Daily DSE Wrap | Tuesday, 1 September 2026 | Amana Capital East Africa</title>', template)
template = template.replace('wrap for 24 August 2026.', 'wrap for Tuesday, 1 September 2026.')
template = template.replace('dse-wrap-2026-08-24.html', 'dse-wrap-2026-09-01.html')

# Write it out
with open('dse-wrap-2026-09-01.html', 'w', encoding='utf-8') as f:
    f.write(template)
print('Done!')
