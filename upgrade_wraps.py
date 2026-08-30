import re
import glob

# 1. Update style.css
css_updates = """
/* --- DSE WRAP ARTICLE UPGRADE --- */
.dse-article-card {
    background-color: var(--cream) !important;
    border: 2px solid var(--gold) !important;
    color: var(--navy) !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1) !important;
}
.dse-article-card p, 
.dse-article-card li {
    color: #1a2a3a !important;
    font-size: 1.05rem;
    line-height: 1.8;
}
.dse-article-card .dse-header-box {
    background-color: var(--navy) !important;
    border-bottom: 4px solid var(--gold) !important;
    border: none !important;
}
.dse-article-card .dse-header-box h1 {
    color: var(--cream) !important;
    font-family: 'Cormorant Garamond', serif !important;
}
.dse-article-card .dse-header-box p {
    color: var(--gold) !important;
}
.dse-article-card h2 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--navy) !important;
    border-bottom: 1px solid rgba(11,29,58,0.1) !important;
    padding-bottom: 0.5rem !important;
    margin-top: 3rem !important;
}
.dse-article-card h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--navy) !important;
}
.dse-article-card .key-takeaways {
    background-color: white !important;
    border: 1px solid rgba(200,150,46,0.3) !important;
    border-left: 4px solid var(--gold) !important;
}
.dse-article-card .key-takeaways h3 {
    color: var(--navy) !important;
}
.dse-article-card table {
    border: 1px solid rgba(11,29,58,0.1) !important;
}
.dse-article-card table th {
    background-color: var(--navy) !important;
    color: var(--cream) !important;
}
.dse-article-card table td {
    color: var(--navy) !important;
    border-bottom: 1px solid rgba(11,29,58,0.1) !important;
}
.dse-article-card .article-disclaimer {
    border-top: 1px solid rgba(11,29,58,0.2) !important;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_updates)

# 2. Inject class into all DSE wrap pages
for fname in glob.glob('dse-wrap-*.html'):
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace <div class="card" style="padding: 3rem;">
    # with <div class="card dse-article-card" style="padding: 3rem;">
    content = content.replace('<div class="card" style="padding: 3rem;">', '<div class="card dse-article-card" style="padding: 3rem;">')
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Update cache buster across ALL files
html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c2 = f.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_16', c2)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(c2)

print('Updated DSE Wrap Pages')
