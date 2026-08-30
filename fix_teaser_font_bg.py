import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def patch_inline_style(html, old_pattern, new_rule):
    match = re.search(old_pattern, html, re.DOTALL)
    if match:
        html = html[:match.start()] + new_rule + html[match.end():]
        return html, True
    return html, False

# 1. Update font size of teaser-prem-stat-value to match snapshot exactly (2rem)
html, ok = patch_inline_style(
    html,
    r'\.teaser-prem-stat-value \{[^}]+\}',
    """.teaser-prem-stat-value {
          font-family: 'Cormorant Garamond', serif;
          font-variant-numeric: tabular-nums;
          font-size: 2rem;
          font-weight: 400;
          color: var(--cream);
          letter-spacing: -0.5px;
      }"""
)
print("teaser-prem-stat-value patched:", ok)

# 2. Update background of teaser-prem-right to solid navy
html, ok = patch_inline_style(
    html,
    r'\.teaser-prem-right \{[^}]+\}',
    """.teaser-prem-right {
          padding: 4rem 3rem;
          display: flex;
          flex-direction: column;
          justify-content: center;
          background: var(--navy);
      }"""
)
print("teaser-prem-right patched:", ok)

# Bump cache
html = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v5', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

html_files = glob.glob('*.html')
bumped = 0
for fname in html_files:
    if fname == 'index.html' or 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    new_c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_mobile_v5', c)
    if new_c != c:
        bumped += 1
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(new_c)

print(f"Done. Cache bumped on {bumped} additional files.")
