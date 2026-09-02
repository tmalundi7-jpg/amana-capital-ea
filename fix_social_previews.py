import glob
import os

meta_tags = """
    <!-- Open Graph / LinkedIn Preview -->
    <meta property="og:image" content="https://www.amana-capital-ea.co.tz/og-image-v2.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <!-- Twitter Preview -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="https://www.amana-capital-ea.co.tz/og-image-v2.png" />
"""

def inject_meta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'og:image' not in c:
        c = c.replace('</head>', meta_tags + '</head>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Injected into {filepath}")
    else:
        print(f"Already injected in {filepath}")

# Update template
inject_meta(os.path.join("templates", "wrap_template.html"))

# Update all existing wrap files so they work right now
for f in glob.glob("dse-wrap-*.html"):
    inject_meta(f)
