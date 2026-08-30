import re
import glob

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# The problem: there's a residual override that applies Plus Jakarta Sans AFTER Cormorant Garamond
# on snapshot-value. We need to find it and remove it.

# The culprit is a rule appended to the end of style.css during "Global Fonts" work that
# accidentally overrode snapshot-value with Plus Jakarta Sans:
#   .snapshot-value {
#     font-family: 'Plus Jakarta Sans', sans-serif !important;
#   }

# Find that specific rule
bad_rule_pattern = r'\.snapshot-value \{\s*font-family: \'Plus Jakarta Sans\', sans-serif !important;\s*\}'
css = re.sub(bad_rule_pattern, '/* [removed bad font override] */', css)

# Also fix teaser-prem-stat-value: remove the Inter sans-serif override
bad_rule2 = r'\.home-teaser \.teaser-prem-left \.teaser-prem-stat-value \{\s*color: var\(--navy\) !important;\s*font-family: \'Inter\', sans-serif !important;\s*font-weight: 600 !important;\s*font-variant-numeric: tabular-nums !important;\s*\}'
css = re.sub(bad_rule2, '.home-teaser .teaser-prem-left .teaser-prem-stat-value { font-family: \'Cormorant Garamond\', serif !important; font-variant-numeric: tabular-nums !important; font-weight: 700 !important; color: var(--cream) !important; }', css)

# Now append a single authoritative final rule at the VERY END that overrides everything
# This will always win because it is the last definition in the file.
final_rule = """

/* ====== AUTHORITATIVE TYPOGRAPHY LOCK - DO NOT OVERRIDE ====== */
/* All three snapshot contexts must render in Cormorant Garamond */
.snapshot-value,
.teaser-prem-stat-value {
    font-family: 'Cormorant Garamond', serif !important;
    font-variant-numeric: tabular-nums !important;
    font-weight: 700 !important;
}
/* Gainers/Losers percentage labels keep their color but stay in sans for readability */
.snapshot-item span[style*="gain"],
.snapshot-item span[style*="loss"],
.teaser-prem-stat-value.gain,
.teaser-prem-stat-value.loss {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
}
/* ============================================================= */
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(final_rule)

# Bump cache buster on all HTML files
html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname:
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c = f2.read()
    c = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_23', c)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c)

print('Done — authoritative font lock applied and cache bumped to v23')
