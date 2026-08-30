import os
import re

dir_path = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea'

def read_file(name):
    with open(os.path.join(dir_path, name), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(name, content):
    with open(os.path.join(dir_path, name), 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Edit index.html
content = read_file('index.html')
content = content.replace('<span class="live-badge">Live Feed</span>', '')
content = content.replace('Live Terminal Feed | End-of-day', 'Terminal Feed | End-of-day')
content = content.replace('Live DSE Snapshot', 'DSE Snapshot')
content = content.replace('class="teaser-prem-right"', 'class="teaser-prem-right premium-upgrade"')
write_file('index.html', content)

# 2. Edit market-intelligence.html
content = read_file('market-intelligence.html')
content = content.replace('Live DSE Snapshot', 'DSE Snapshot')
content = content.replace('NSE, USE, RSE', 'DSE')
content = content.replace('<div style="height: 300px; position: relative; width: 100%;">', '<div style="width: 100%; overflow-x: auto;"><div style="height: 300px; position: relative; width: 100%; min-width: 600px;">')
content = content.replace('</div>\n<p style="font-size: 0.75rem;', '</div></div>\n<p style="font-size: 0.75rem;')
write_file('market-intelligence.html', content)

# 3. Edit bond-calculator.html
content = read_file('bond-calculator.html')
content = re.sub(r'(<th[^>]+)text-align:right([^>]*>Nominal Income</th>)', r'\g<1>text-align:left\g<2>', content)
content = re.sub(r'(<th[^>]+)text-align:right([^>]*>Cum\. Nominal</th>)', r'\g<1>text-align:left\g<2>', content)
content = re.sub(r'(<th[^>]+)text-align:right([^>]*>Cum\. Real Value</th>)', r'\g<1>text-align:left\g<2>', content)
write_file('bond-calculator.html', content)

content = read_file('script.js')
content = re.sub(r'<td style="([^"]*?)text-align:right([^"]*?)">\$\{formatCurrency\(thisYearIncome\)\}', r'<td style="\g<1>text-align:left\g<2>">${formatCurrency(thisYearIncome)}', content)
content = re.sub(r'<td style="([^"]*?)text-align:right([^"]*?)">\$\{formatCurrency\(nominalValue\)\}', r'<td style="\g<1>text-align:left\g<2>">${formatCurrency(nominalValue)}', content)
content = re.sub(r'<td style="([^"]*?)text-align:right([^"]*?)">\$\{formatCurrency\(currentRealValue\)\}', r'<td style="\g<1>text-align:left\g<2>">${formatCurrency(currentRealValue)}', content)
write_file('script.js', content)

# 4. Edit about.html
content = read_file('about.html')
content = content.replace('class="ab-mission-card"', 'class="ab-mission-card premium-about"')
write_file('about.html', content)

# 5. Append CSS to style.css
css_append = """
/* Added by script */
.snapshot-grid {
  display: flex !important;
  flex-wrap: nowrap !important;
  justify-content: space-between !important;
  align-items: flex-start !important;
  overflow-x: auto !important;
}
.snapshot-item {
  flex: 1 1 0 !important;
  min-width: min-content !important;
}
.snapshot-value {
  white-space: nowrap !important;
}
.snapshot-mover {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.25rem !important;
  white-space: nowrap !important;
}
.premium-upgrade {
  border: 1px solid var(--gold) !important;
  background: linear-gradient(135deg, rgba(179,146,85,0.1), rgba(179,146,85,0.02)) !important;
  box-shadow: inset 0 0 20px rgba(179,146,85,0.05) !important;
  position: relative;
}
.premium-upgrade::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 3px;
  background: var(--gold);
}
.premium-about {
  column-count: 2;
  column-gap: 3rem;
  column-rule: 1px solid rgba(179,146,85,0.2);
  border: 1px solid rgba(179,146,85,0.2);
  padding: 3rem;
  background: rgba(255,255,255,0.01);
  box-shadow: 0 4px 30px rgba(0,0,0,0.1);
}
.premium-about p:first-child::first-letter {
  font-family: 'Cormorant Garamond', serif;
  float: left;
  font-size: 4.5rem;
  line-height: 0.8;
  padding-right: 0.5rem;
  color: var(--gold);
  font-weight: 400;
}
@media (max-width: 768px) {
  .premium-about { column-count: 1; }
}
"""
content = read_file('style.css')
content += css_append
write_file('style.css', content)

# 6. Update cache busters in all .html files
for f_name in os.listdir(dir_path):
    if f_name.endswith('.html'):
        c = read_file(f_name)
        c_new = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish', c)
        if c != c_new:
            write_file(f_name, c_new)

print('Done')
