import glob
import re

# 1. Update logo in HTML files
html_files = glob.glob('*.html')
count = 0
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if '<span class="logo-word-primary">Amana Capital</span>' in content:
        content = content.replace('<span class="logo-word-primary">Amana Capital</span>', '<span class="logo-word-primary">AMANA CAPITAL</span>')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
print(f'Updated logo in {count} HTML files.')

# 2. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Restore vibrant colors
css = css.replace('--navy: #051426;', '--navy: #0A1628;')
css = css.replace('--navy-alt: #0A213D;', '--navy-alt: #0F223D;')
css = css.replace('--cream: #F8F7F4;', '--cream: #FBF7F0;')
css = css.replace('--gold: #B39255;', '--gold: #E5B13B;')
css = css.replace('--gold-hover: #987A45;', '--gold-hover: #F1C453;')
css = css.replace('--gold-light: rgba(179, 146, 85, 0.1);', '--gold-light: rgba(229, 177, 59, 0.15);')

# Fix button hover
btn_hover = '''
.btn-gold-solid:hover {
  background: var(--gold-hover);
  color: var(--navy);
  border-color: var(--gold-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(229, 177, 59, 0.4);
}'''
css = re.sub(r'\.btn-gold-solid:hover\s*\{[^}]*\}', btn_hover.strip(), css)

# Fix background box for headers
header_box = '''
/* Dark Navy Box for Visibility */
.why-section-header {
    background-color: var(--navy);
    padding: 2.5rem;
    border-radius: 8px;
    margin-bottom: 2.5rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.why-section-header .section-eyebrow {
    color: var(--gold) !important;
}
.why-section-header .section-title {
    color: var(--white) !important;
    margin-bottom: 0;
}
'''
if '/* Dark Navy Box for Visibility */' not in css:
    css = css + '\n' + header_box

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Updated style.css.')
