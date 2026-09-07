import mammoth
import re

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 04 September 2026.docx'
template_path = 'dse-wrap-2026-09-03.html'
output_path = 'dse-wrap-2026-09-04.html'

with open(docx_path, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html_content = result.value

# Clean up Mammoth HTML for Amana styling
html_content = html_content.replace('<h1>', '<h2 class="wrap-section-title">')
html_content = html_content.replace('</h1>', '</h2>')
html_content = html_content.replace('<h2>', '<h2 class="wrap-section-title">')
html_content = html_content.replace('</h2>', '</h2>')
html_content = html_content.replace('<table>', '<div class="table-responsive"><table class="data-table">')
html_content = html_content.replace('</table>', '</table></div>')
# Fix missing table headers since mammoth just outputs <tr><td>
html_content = html_content.replace('<tr><td>Metric</td>', '<thead><tr><th>Metric</th>')
html_content = html_content.replace('<td>Change</td></tr>', '<th>Change</th></tr></thead><tbody>')
html_content = html_content.replace('<tr><td>Ticker</td>', '</tbody></table></div><div class="table-responsive"><table class="data-table"><thead><tr><th>Ticker</th>')
html_content = html_content.replace('<td>Volume</td></tr>', '<th>Volume</th></tr></thead><tbody>')
html_content = html_content.replace('<tr><td>Counter</td>', '</tbody></table></div><div class="table-responsive"><table class="data-table"><thead><tr><th>Counter</th>')
html_content = html_content.replace('<td>Monday Lower Limit (TZS)</td></tr>', '<th>Monday Lower Limit (TZS)</th></tr></thead><tbody>')

# Add </tbody> at the end of the last table
html_content = html_content.replace('</table>', '</tbody></table>')

# Make the first paragraph the excerpt/intro if we want, or just let it be.
# Wrap in article-content
html_content = f'<div class="article-content">\n{html_content}\n</div>'

# Now load the template from 03 Sep
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace the article content
# Find the start of article-content
start_idx = template.find('<div class="article-content">')
# Find the end of article-content (it ends right before </article>)
end_idx = template.find('</article>')

if start_idx != -1 and end_idx != -1:
    new_page = template[:start_idx] + html_content + '\n                ' + template[end_idx:]
else:
    print("Could not find article-content bounds in template.")
    exit(1)

# Update page metadata
new_page = new_page.replace('3rd September 2026', '4th September 2026')
new_page = new_page.replace('03 September 2026', '04 September 2026')
new_page = new_page.replace('3 September 2026', '4 September 2026')
new_page = new_page.replace('2026-09-03', '2026-09-04')
new_page = new_page.replace('Thursday', 'Friday')

# Write the new wrap page
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_page)

print("dse-wrap-2026-09-04.html created successfully.")
