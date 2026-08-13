import os
import glob
import re

html_files = glob.glob('dse-wrap-*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace <p>Upper limit: ...</p> with <p><strong>Upper limit: ...</strong></p>
    # Note: Sometimes it might already be bolded, or partially bolded, so we need to handle that.
    # We will search for <p>Upper limit:.*?</p> and <p>Lower limit:.*?</p>
    
    # First, let's just make sure we don't double bold if it's already <p><strong>Upper limit:
    content = re.sub(r'<p>Upper limit:(.*?)</p>', r'<p><strong>Upper limit:\1</strong></p>', content)
    content = re.sub(r'<p>Lower limit:(.*?)</p>', r'<p><strong>Lower limit:\1</strong></p>', content)
    
    # Also handle cases where there might be a space before the colon
    content = re.sub(r'<p>Upper limit :(.*?)</p>', r'<p><strong>Upper limit:\1</strong></p>', content)
    content = re.sub(r'<p>Lower limit :(.*?)</p>', r'<p><strong>Lower limit:\1</strong></p>', content)
    
    # Clean up double strongs if any
    content = content.replace('<strong><strong>', '<strong>')
    content = content.replace('</strong></strong>', '</strong>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {len(html_files)} files.")
