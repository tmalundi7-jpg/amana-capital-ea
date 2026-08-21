import sys, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def analyse(fname):
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    print(f'\n=== {fname} ({os.path.getsize(fname)//1000}KB) ===')
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    clean = [re.sub('<[^>]+>','',s).strip() for s in h2s]
    for i, t in enumerate(clean, 1):
        print(f'  H2-{i}: {t[:80]}')
    print(f'  Tables: {html.count("<table")}')
    print(f'  Gold side-box: {"YES" if "border-left: 4px solid var(--gold)" in html else "NO"}')
    print(f'  Nav risk-profiler: {"YES" if "risk-profiler" in html else "NO"}')
    print(f'  Nav About: {"YES" if "/about" in html else "NO"}')
    print(f'  CSS ref style.css: {"YES" if "style.css" in html else "NO"}')
    print(f'  CSS ref style.min.css: {"YES" if "style.min.css" in html else "NO"}')
    # Identify if intro para exists (before first h2)
    first_h2_pos = html.find('<h2')
    intro_section = html[:first_h2_pos] if first_h2_pos > 0 else ''
    intro_paras = intro_section.count('<p>')
    print(f'  Intro paragraphs before first H2: {intro_paras}')

files = [
    'dse-wrap-2026-08-13.html',
    'dse-wrap-2026-08-14.html',
    'dse-wrap-2026-08-17.html',
    'dse-wrap-2026-08-18.html',
    'dse-wrap-2026-08-19.html',
    'dse-wrap-2026-08-20.html',
    'dse-wrap-2026-08-21.html',
]

for f in files:
    analyse(f)
