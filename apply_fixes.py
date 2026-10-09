import os, glob, re

repo = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"

# 1. index.html replacements
index_path = os.path.join(repo, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Copy replacements
idx = idx.replace("Tanzania's Premier Investment Advisory", "Tanzania's Premier Market Intelligence")
idx = idx.replace("Institutional-grade market intelligence, daily DSE analysis, and bespoke investment advisory for East Africa's discerning investors.", "Institutional-grade market intelligence and daily DSE analysis for East Africa's discerning investors.")
idx = idx.replace("03 &mdash; Advisory", "03 &mdash; Research")
idx = idx.replace("Investment Advisory", "Custom Research")
idx = idx.replace("Bespoke portfolio construction for sophisticated investors and institutions.", "Tailored market reports and data analysis for sophisticated investors and institutions.")
# Note: handle both mdash and em-dash
idx = re.sub(r'We hold ourselves to the fiduciary standard (.*?|\n)*? your interests before ours, without exception\.', 'We hold ourselves to the highest editorial standard &mdash; accuracy and independence in every report, without exception.', idx)

# Checkbox
idx = idx.replace('<input type="checkbox" checked', '<input type="checkbox"')

# Risk Notice - index.html
risk_notice_html = """
<div class="risk-notice" style="background:rgba(201,162,39,.08);border:1px solid rgba(201,162,39,.25);border-radius:8px;padding:1rem 1.5rem;margin:2rem auto;max-width:800px;text-align:center;font-size:.85rem;color:rgba(250,246,238,.7);">
  <strong style="color:#c9a227;">Risk Warning:</strong> Investing in securities involves risk. Capital is at risk and past performance does not guarantee future results. Our content is for informational and educational purposes only and does not constitute financial advice. CMSA registration is currently pending &mdash; we operate as an independent research publisher.
</div>
"""
# insert after hero section
if 'class="risk-notice"' not in idx:
    idx = re.sub(r'(<section class="hero".*?</section>)', r'\1\n' + risk_notice_html, idx, count=1, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx)

# 2. Risk Notice - market-intelligence.html
mi_path = os.path.join(repo, "market-intelligence.html")
with open(mi_path, "r", encoding="utf-8") as f:
    mi = f.read()

# insert at top of page content
if 'class="risk-notice"' not in mi:
    mi = re.sub(r'(<div class="container page-terminal">)', r'\1\n' + risk_notice_html, mi, count=1)

with open(mi_path, "w", encoding="utf-8") as f:
    f.write(mi)

# 3. Footer Legal Links (All pages)
footer_links_html = """
<div style="display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: center; margin: 0.5rem 0;">
<a href="/privacy-policy" style="color: var(--mist); opacity: 0.6; text-decoration: none; font-size:0.75rem; transition: color 0.2s;">Privacy Policy</a>
<a href="/terms-of-service" style="color: var(--mist); opacity: 0.6; text-decoration: none; font-size:0.75rem; transition: color 0.2s;">Terms of Service</a>
<a href="/cookie-policy" style="color: var(--mist); opacity: 0.6; text-decoration: none; font-size:0.75rem; transition: color 0.2s;">Cookie Policy</a>
<a href="/complaints-procedure" style="color: var(--mist); opacity: 0.6; text-decoration: none; font-size:0.75rem; transition: color 0.2s;">Complaints Procedure</a>
</div>
"""
wrap_disclaimer = """
<p style="font-size:.8rem;color:rgba(250,246,238,.5);margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.1);">
  <strong>Disclaimer:</strong> This report is for informational and educational purposes only and does not constitute financial, legal, or tax advice. Capital is at risk. Past performance does not guarantee future results. All investment decisions are solely your responsibility.
</p>
"""

all_html = glob.glob(os.path.join(repo, "*.html"))
for path in all_html:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "Privacy Policy" not in html:
        html = re.sub(r'(<div[^>]*>&copy;\s*2026\s*Amana Capital East Africa Limited.*?</div>)', footer_links_html + r'\n\1', html, flags=re.DOTALL)
    
    if "dse-wrap" in path and "archive" not in path:
        old_disclaimer_pattern = r'<p style="font-size:\s*0\.85rem[^>]*>.*?For general informational and educational purposes only.*?<\/p>'
        html = re.sub(old_disclaimer_pattern, wrap_disclaimer, html, flags=re.DOTALL)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
print("Replacements done.")
