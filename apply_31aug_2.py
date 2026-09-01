import json
import re
import os
import shutil

with open('extracted_31aug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Copy base
shutil.copy('dse-wrap-2026-08-28.html', 'dse-wrap-2026-08-31.html')

with open('dse-wrap-2026-08-31.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update titles and dates
html = re.sub(r'<title>.*?</title>', '<title>Daily DSE Wrap | 31 August 2026 | Amana Capital</title>', html)
html = re.sub(r'Monday, 17th August 2026|Friday, 28th August 2026|28 August 2026', '31 August 2026', html)

# The content starts at <!-- ARTICLE_BODY_START --> and ends at <!-- ARTICLE_BODY_END -->
wrap_title = data['wrap']['paragraphs'][1]
intro_p = ""
for i, p in enumerate(data['wrap']['paragraphs']):
    if "The era of 15% risk-free yields is ending" in p or "The Dar es Salaam Stock Exchange" in p or "A session that began with" in p or "Monday's session" in p:
        intro_p = p
        break

html = re.sub(r'<h1 class="wrap-title">.*?</h1>', f'<h1 class="wrap-title">{wrap_title}</h1>', html)
html = re.sub(r'<p class="wrap-intro">.*?</p>', f'<p class="wrap-intro">{intro_p}</p>', html)

# Build content paragraphs
body_html = ""
skip_next = False
in_list = False

start_idx = 0
for i, p in enumerate(data['wrap']['paragraphs']):
    if p == intro_p:
        start_idx = i + 1
        break

for p in data['wrap']['paragraphs'][start_idx:-2]: # skip disclaimer
    p = p.strip()
    if not p: continue
    
    # Check if heading
    if re.match(r'^\d+\.\s+[A-Z]', p):
        if in_list:
            body_html += "</ul>\n"
            in_list = False
        body_html += f"<h2>{p}</h2>\n"
    elif p.startswith("Near-Term") or p.startswith("Medium-Term") or p.startswith("Long-Term") or "Key Catalyst" in p:
        if in_list:
            body_html += "</ul>\n"
            in_list = False
        body_html += f"<h3>{p}</h3>\n"
    elif p.startswith("NMB") or p.startswith("CRDB") or p.startswith("VODA") or p.startswith("Bond yields") or p.startswith("The Bank of Tanzania") or p.startswith("The government's"):
        if not in_list:
            body_html += "<ul>\n"
            in_list = True
        body_html += f"<li>{p}</li>\n"
    else:
        if in_list:
            body_html += "</ul>\n"
            in_list = False
        body_html += f"<p>{p}</p>\n"

if in_list:
    body_html += "</ul>\n"

# Add tables
table_html = "<h3>Market Performance Metrics</h3>\n<div class='table-responsive'>\n<table class='data-table'>\n"
t1 = data['wrap']['tables'][0]
table_html += f"<thead><tr><th>{t1[0][0]}</th><th>{t1[0][1]}</th><th>{t1[0][2]}</th><th>{t1[0][3]}</th></tr></thead>\n<tbody>\n"
for row in t1[1:]:
    cls = ""
    if "+" in row[3]: cls = "gain"
    if "-" in row[3] or "\ufffd" in row[3]: cls = "loss"
    table_html += f"<tr><td><strong>{row[0]}</strong></td><td>{row[1]}</td><td>{row[2]}</td><td class='{cls}'>{row[3]}</td></tr>\n"
table_html += "</tbody></table></div>\n"

body_html = table_html + body_html

html = re.sub(r'<!-- ARTICLE_BODY_START -->.*?<!-- ARTICLE_BODY_END -->', f'<!-- ARTICLE_BODY_START -->\n{body_html}\n<!-- ARTICLE_BODY_END -->', html, flags=re.DOTALL)

with open('dse-wrap-2026-08-31.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Generated dse-wrap-2026-08-31.html")
