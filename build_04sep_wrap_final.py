import mammoth
import re

docx_path = r'C:\Users\tmalu\Documents\Daily DSE Wrap 04 September 2026.docx'
template_path = 'dse-wrap-2026-09-03.html'
output_path = 'dse-wrap-2026-09-04.html'

with open(docx_path, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html_content = result.value

# Clean up Mammoth HTML
html_content = html_content.replace('<h1>', '<h2 class="wrap-section-title">')
html_content = html_content.replace('</h1>', '</h2>')
html_content = html_content.replace('<h2>', '<h2 class="wrap-section-title">')
html_content = html_content.replace('</h2>', '</h2>')
html_content = html_content.replace('<table>', '<div class="table-responsive"><table class="data-table">')
html_content = html_content.replace('</table>', '</table></div>')
html_content = html_content.replace('<p><strong>', '<h2 class="wrap-section-title">')
html_content = html_content.replace('</strong></p>', '</h2>')
html_content = html_content.replace('<thead>', '')
html_content = html_content.replace('</thead>', '')
html_content = html_content.replace('<tbody>', '')
html_content = html_content.replace('</tbody>', '')

match = re.search(r'<h2 class="wrap-section-title">(.*?)</h2><h2 class="wrap-section-title">(.*?)</h2>(.*)', html_content, re.DOTALL)
if match:
    title = match.group(1).strip()
    subtitle = match.group(2).strip()
    body = match.group(3).strip()
else:
    print("Could not parse title and subtitle.")
    exit(1)

header_box = f"""<div class="dse-header-box" style="background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h1 style="margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;">{title}</h1>
    <p style="font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;">{subtitle}</p>
</div>"""

with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

start_idx = template.find('<div class="dse-header-box"')
end_idx = template.find('<p><em>For general informational')

if start_idx != -1 and end_idx != -1:
    new_page = template[:start_idx] + header_box + '\n\n' + body + '\n\n' + template[end_idx:]
else:
    print("Could not find article bounds in template.")
    exit(1)

# Update page metadata
new_page = new_page.replace('3rd September 2026', '4th September 2026')
new_page = new_page.replace('03 September 2026', '04 September 2026')
new_page = new_page.replace('3 September 2026', '4 September 2026')
new_page = new_page.replace('2026-09-03', '2026-09-04')
new_page = new_page.replace('Thursday', 'Friday')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_page)

print("dse-wrap-2026-09-04.html created successfully.")
