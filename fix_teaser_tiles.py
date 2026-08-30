import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------
# Replace the old .teaser-prem-stats inline CSS (flex layout, no tiles)
# with the new grid + tile layout that matches the main DSE Snapshot
# -------------------------------------------------------
old_stats_block = """.teaser-prem-stats {
          display: flex;
          gap: 3rem;
          padding-top: 2rem;
          border-top: 1px solid rgba(179,146,85,0.2);
      }
      .teaser-prem-stat-label {
          font-size: 0.65rem;
          color: rgba(251,247,240,0.6);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 0.4rem;
          font-weight: 600;
      }
      .teaser-prem-stat-value {
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

new_stats_block = """.teaser-prem-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 0.75rem;
          padding-top: 1.5rem;
      }
      /* Each stat tile — identical to main DSE Snapshot tiles */
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
      }
      .teaser-prem-stat-label {
          font-size: 0.65rem;
          color: var(--gold);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 0.5rem;
          font-weight: 700;
          min-height: 24px;
          display: flex;
          align-items: flex-end;
      }
      /* Numbers — Cormorant Garamond exactly like main DSE Snapshot */
      .teaser-prem-stat-value {
          font-family: 'Cormorant Garamond', serif;
          font-variant-numeric: tabular-nums;
          font-size: 1.4rem;
          font-weight: 700;
          color: var(--cream);
          letter-spacing: -0.5px;
      }
      /* Top Gainer percentage — slightly smaller sans-serif */
      .teaser-prem-stat-value.gain {
          font-family: 'Plus Jakarta Sans', sans-serif;
          font-size: 0.85rem;
          font-weight: 700;
          color: #22c55e;
      }"""

if old_stats_block in html:
    html = html.replace(old_stats_block, new_stats_block)
    print("Replaced inline stats CSS block exactly")
else:
    # Fallback: find and replace with regex
    old_pattern = r'\.teaser-prem-stats \{[^}]+\}\s*\.teaser-prem-stat-label \{[^}]+\}\s*\.teaser-prem-stat-value \{[^}]+\}\s*\.teaser-prem-stat-value\.gain \{[^}]+\}'
    if re.search(old_pattern, html, re.DOTALL):
        html = re.sub(old_pattern, new_stats_block, html, flags=re.DOTALL)
        print("Replaced inline stats CSS block via regex fallback")
    else:
        print("WARNING: Could not find block — checking for partial match")
        # Try patching just the display:flex -> grid
        html = html.replace(
            '.teaser-prem-stats {\n          display: flex;\n          gap: 3rem;\n          padding-top: 2rem;\n          border-top: 1px solid rgba(179,146,85,0.2);\n      }',
            '.teaser-prem-stats {\n          display: grid;\n          grid-template-columns: repeat(3, 1fr);\n          gap: 0.75rem;\n          padding-top: 1.5rem;\n      }'
        )
        print("Applied partial patch for display:flex -> grid")

# Bump cache
html = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_26', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Bump cache on all other HTML
html_files = glob.glob('*.html')
for fname in html_files:
    if fname == 'index.html' or 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_26', c)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c)

print("Done — cache bumped to v26")
