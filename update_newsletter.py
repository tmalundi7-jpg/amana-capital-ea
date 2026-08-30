import re
import glob

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the text to 'Join Our Research Network'
old_text = r'<h2>Never Miss a<br/><em>Market Signal</em></h2>\n  <p>Daily DSE wraps and macroeconomic briefings delivered to your inbox every trading day. Institutional quality. Completely free.</p>'
new_text = r'<h2>Join Our Research Network</h2>\n  <p>Exclusive institutional-grade DSE wraps and macroeconomic briefings delivered to your inbox every trading day. No noise &mdash; only signal.</p>'
content = re.sub(old_text, new_text, content, flags=re.DOTALL)

old_form = r'<input name="email" placeholder="Enter your institutional email" required="" type="email"/>\n  <button type="submit">Subscribe to Daily Intelligence</button>\n  <p style="font-size:0.7rem;color:rgba\(251,247,240,0.25\);margin:0;">No spam\. Unsubscribe at any time\.</p>'
new_form = r'<input name="email" placeholder="Your institutional email address" required="" type="email"/>\n  <button type="submit">Subscribe to Intelligence Briefing</button>\n  <p style="font-size:0.65rem;color:rgba(251,247,240,0.25);margin:0;">No spam. Unsubscribe at any time. For serious investors.</p>'
content = re.sub(old_form, new_form, content, flags=re.DOTALL)

# Reduce the font sizes in the CSS block
content = re.sub(r'\.mi-subscribe h2 \{[\s\S]*?font-size: 2rem;', '.mi-subscribe h2 {\n        font-family: \'Cormorant Garamond\', serif;\n        font-size: 1.6rem;', content)
content = re.sub(r'\.mi-subscribe p \{ color: rgba\(251,247,240,0\.5\); font-size: 0\.88rem;', '.mi-subscribe p { color: rgba(251,247,240,0.5); font-size: 0.78rem;', content)
content = re.sub(r'\.mi-sub-form input \{[\s\S]*?font-size: 0\.88rem;', '.mi-sub-form input {\n        padding: 0.75rem 1rem;\n        background: rgba(255,255,255,0.06);\n        border: 1px solid rgba(200,150,46,0.25);\n        border-radius: 8px;\n        color: var(--cream);\n        font-family: inherit;\n        font-size: 0.78rem;', content)
content = re.sub(r'\.mi-sub-form button \{[\s\S]*?font-size: 0\.88rem;', '.mi-sub-form button {\n        padding: 0.75rem;\n        background: var(--gold);\n        border: none;\n        border-radius: 8px;\n        color: var(--navy);\n        font-weight: 700;\n        font-size: 0.78rem;', content)


with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(content)

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_15', c2)
    
    if fname == 'market-intelligence.html':
        content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_15', content)
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(content)
    else:
        with open(fname, 'w', encoding='utf-8') as f3:
            f3.write(c2)

print('Updated text and reduced font sizes')
