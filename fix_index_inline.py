import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the inline <style> block in index.html that overrides teaser-prem-stat-value
#    Old: font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600;
#    New: match the main snapshot exactly — same font, same size, same weight

old_teaser_css = """.teaser-prem-stat-value {
          font-family: 'Cormorant Garamond', serif;
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--cream);
      }
      .teaser-prem-stat-value.gain { color: #22c55e; }"""

new_teaser_css = """.teaser-prem-stat-value {
          font-family: 'Cormorant Garamond', serif;
          font-variant-numeric: tabular-nums;
          font-size: 1.4rem;
          font-weight: 700;
          color: var(--cream);
          letter-spacing: -0.5px;
      }
      .teaser-prem-stat-value.gain { 
          color: #22c55e;
          font-family: 'Plus Jakarta Sans', sans-serif;
          font-size: 0.85rem;
          font-weight: 700;
      }"""

if old_teaser_css in html:
    html = html.replace(old_teaser_css, new_teaser_css)
    print("Replaced inline teaser-prem-stat-value style block")
else:
    # Try a looser match with regex
    html = re.sub(
        r'\.teaser-prem-stat-value \{\s*font-family: \'Cormorant Garamond\', serif;\s*font-size: 1\.5rem;\s*font-weight: 600;\s*color: var\(--cream\);\s*\}\s*\.teaser-prem-stat-value\.gain \{ color: #22c55e; \}',
        new_teaser_css,
        html
    )
    print("Used regex to replace inline teaser-prem-stat-value")

# 2. Also fix the .teaser-prem-stats inline CSS (currently flex, old layout) to match the tile design
old_stats_css = """.teaser-prem-stats {
          display: flex;
          gap: 3rem;
          padding-top: 2rem;
          border-top: 1px solid rgba(179,146,85,0.2);
      }"""

new_stats_css = """.teaser-prem-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 0.75rem;
          padding-top: 1.5rem;
      }"""

if old_stats_css in html:
    html = html.replace(old_stats_css, new_stats_css)
    print("Replaced .teaser-prem-stats inline CSS")

# 3. Add tile background styles to .teaser-prem-stat / .teaser-prem-stats > div
old_label_css = """.teaser-prem-stat-label {
          font-size: 0.65rem;
          color: rgba(251,247,240,0.6);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 0.4rem;
          font-weight: 600;
      }"""

new_label_css = """.teaser-prem-stat-label {
          font-size: 0.65rem;
          color: var(--gold);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 0.5rem;
          font-weight: 700;
      }
      .teaser-prem-stat,
      .teaser-prem-stats > div {
          background-color: var(--navy);
          border: 1px solid rgba(200,150,46,0.3);
          border-top: 3px solid var(--gold);
          padding: 1.25rem;
          border-radius: 4px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
          display: flex;
          flex-direction: column;
      }"""

if old_label_css in html:
    html = html.replace(old_label_css, new_label_css)
    print("Replaced .teaser-prem-stat-label and added tile CSS")

# 4. Bump cache
html = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_24', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Also bump all other HTML files
html_files = glob.glob('*.html')
for fname in html_files:
    if fname == 'index.html' or 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_24', c)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c)

print("Done — inline styles in index.html fixed, cache bumped to v24")
