import re
import glob

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

hero_pattern = r'<section class="ab-hero" style="background: var\(--cream\); padding: 7rem 0 6rem;">.*?</section>'
new_hero = """<section class="ab-hero">
    <div class="container" style="max-width: 800px; text-align: center; padding: 6rem 0;">
        <div style="color: var(--gold); font-size: 0.8rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2rem;">Our Core Purpose</div>
        <h1 style="font-family: 'Cormorant Garamond', serif; font-size: 4.5rem; font-weight: 400; color: var(--navy); line-height: 1.1; margin-bottom: 3rem;">About<br>Amana<br>Capital<span style="color: var(--gold);">.</span></h1>
        
        <p style="font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; color: var(--navy); line-height: 1.6; margin-bottom: 2rem;">
            Amana Capital East Africa Limited exists to deliver institutional-grade investment research, advisory, and fund management services rooted in the Dar es Salaam Stock Exchange and East African capital markets.
        </p>
        
        <div style="width: 60px; height: 2px; background-color: var(--gold); margin: 0 auto 2rem auto;"></div>
        
        <p style="font-size: 1.1rem; color: rgba(11,29,58,0.8); line-height: 1.8; font-weight: 400;">
            Our core purpose is to equip Tanzanian investors &mdash; both at home and across the global diaspora &mdash; with the clarity, discipline, and long-horizon perspective needed to build lasting wealth in the region's frontier markets.
        </p>
    </div>
</section>"""

html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)
with open('about.html', 'w', encoding='utf-8') as f:
    f.write(html)

html_files = glob.glob('*.html')
for fname in html_files:
    if 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_design_revert', content)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
