import re
import glob

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_hero = re.search(r'<section class=\"ab-hero\">.*?</section>', content, re.DOTALL).group(0)

new_hero = '''<section class="ab-hero">
    <div class="container">
        <div class="ab-hero-inner">
            <!-- Left Side: Title -->
            <div>
                <div style="color: var(--gold); font-size: 0.85rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.5rem;">Our Core Purpose</div>
                <h1 style="font-family: 'Cormorant Garamond', serif; font-size: 5rem; font-weight: 400; color: var(--navy); line-height: 1; margin: 0;">
                    About<br>Amana<br>Capital<span style="color: var(--gold);">.</span>
                </h1>
            </div>
            
            <!-- Right Side: Premium Navy Box -->
            <div style="background-color: var(--navy); border: 2px solid var(--gold); padding: 4rem 3.5rem; border-radius: 4px; box-shadow: 0 10px 40px rgba(11,29,58,0.15);">
                <p style="font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; color: var(--cream); line-height: 1.6; margin-bottom: 2rem;">
                    Amana Capital East Africa Limited exists to deliver institutional-grade investment research, advisory, and fund management services rooted in the Dar es Salaam Stock Exchange and East African capital markets.
                </p>
                
                <div style="width: 50px; height: 2px; background-color: var(--gold); margin-bottom: 2rem;"></div>
                
                <p style="font-size: 1.05rem; color: rgba(251,247,240,0.7); line-height: 1.8; margin: 0;">
                    Our core purpose is to equip Tanzanian investors &mdash; both at home and across the global diaspora &mdash; with the clarity, discipline, and long-horizon perspective needed to build lasting wealth in the region's frontier markets.
                </p>
            </div>
        </div>
    </div>
</section>'''

content = content.replace(old_hero, new_hero)

# Bump cache globally just in case they're sensitive to it
content = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_17', content)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

html_files = glob.glob('*.html')
for fname in html_files:
    if fname == 'about.html' or 'test_pdf' in fname or '.bak' in fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
    c2 = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260830_final_polish_17', c2)
    with open(fname, 'w', encoding='utf-8') as f3:
        f3.write(c2)

print('Updated about.html hero section')
