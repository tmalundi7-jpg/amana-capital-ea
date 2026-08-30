import re
import glob

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix max-width of mi-subscribe-inner to match mi-layout (1040px)
content = re.sub(r'\.mi-subscribe-inner \{ display: grid; grid-template-columns: 1fr 1fr; gap: 6rem; align-items: center; max-width: 100%; margin: 0; \}', 
                 '.mi-subscribe-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 6rem; align-items: center; max-width: 1040px; margin: 0 auto; }', 
                 content, flags=re.DOTALL)

# Revert text back to what user pasted
old_text = r'<h2>Join Our Research Network</h2>\n  <p>Exclusive institutional-grade DSE wraps and macroeconomic briefings delivered to your inbox every trading day\. No noise &mdash; only signal\.</p>'
new_text = r'<h2>Never Miss a<br/><em>Market Signal</em></h2>\n  <p>Daily DSE wraps and macroeconomic briefings delivered to your inbox every trading day. Institutional quality. Completely free.</p>'
content = re.sub(old_text, new_text, content, flags=re.DOTALL)

old_form = r'<input name="email" placeholder="Your institutional email address" required="" type="email"/>\n  <button type="submit">Subscribe to Intelligence Briefing</button>\n  <p style="font-size:0\.7rem;color:rgba\(251,247,240,0\.25\);margin:0;">No spam\. Unsubscribe at any time\. For serious investors\.</p>'
new_form = r'<input name="email" placeholder="Enter your institutional email" required="" type="email"/>\n  <button type="submit">Subscribe to Daily Intelligence</button>\n  <p style="font-size:0.7rem;color:rgba(251,247,240,0.25);margin:0;">No spam. Unsubscribe at any time.</p>'
content = re.sub(old_form, new_form, content, flags=re.DOTALL)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(content)

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_14', c2)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c2)

print('Aligned newsletter and reverted text')
