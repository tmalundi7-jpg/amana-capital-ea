#!/usr/bin/env python3
"""
fix_about_hero.py
-----------------
1. Replaces <section class="ab-hero">...</section> in about.html with the
   canonical premium navy-plaque layout.
2. Bumps every cache-buster query string in ALL *.html files to
   v=20260830_final_polish_27.
"""

import re
import glob
import os

# ── 1.  TARGET HTML ──────────────────────────────────────────────────────────
NEW_HERO = '''\
<section class="ab-hero">
    <div class="container">
        <div class="ab-hero-inner">
            <!-- Left: Massive Navy Plaque -->
            <div style="background-color: var(--navy); border: 2px solid var(--gold); padding: 5rem 4rem; border-radius: 6px; box-shadow: 0 16px 60px rgba(11,29,58,0.25); display: flex; flex-direction: column; justify-content: center;">
                <div style="color: var(--gold); font-size: 0.75rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 2rem; display: flex; align-items: center; gap: 0.75rem;">
                    <span style="display: inline-block; width: 6px; height: 6px; background: var(--gold); border-radius: 50%;"></span>
                    Our Core Purpose
                </div>
                <h1 style="font-family: \'Cormorant Garamond\', serif; font-size: 5.5rem; font-weight: 400; color: var(--cream); line-height: 0.95; margin: 0; letter-spacing: -2px;">
                    About<br>Amana<br>Capital<span style="color: var(--gold);">.</span>
                </h1>
                <div style="width: 60px; height: 2px; background: var(--gold); margin-top: 2.5rem; opacity: 0.6;"></div>
            </div>

            <!-- Right: Mission Statement -->
            <div style="padding: 1rem 0 1rem 3.5rem; display: flex; flex-direction: column; justify-content: center; gap: 2rem;">
                <p style="font-family: \'Cormorant Garamond\', serif; font-size: 2.1rem; color: var(--navy); line-height: 1.4; margin: 0;">
                    Amana Capital East Africa Limited exists to deliver institutional-grade investment research, advisory, and fund management services rooted in the Dar es Salaam Stock Exchange and East African capital markets.
                </p>
                <div style="width: 70px; height: 3px; background: linear-gradient(90deg, var(--gold), rgba(200,150,46,0.3));"></div>
                <p style="font-size: 1.1rem; color: rgba(11,29,58,0.78); line-height: 1.85; margin: 0; border-left: 3px solid var(--gold); padding-left: 1.25rem;">
                    Our core purpose is to equip Tanzanian investors &mdash; both at home and across the global diaspora &mdash; with the clarity, discipline, and long-horizon perspective needed to build lasting wealth in the region&#x27;s frontier markets.
                </p>
            </div>
        </div>
    </div>
</section>'''

# ── 2.  REPLACE HERO IN about.html ───────────────────────────────────────────
ABOUT = 'about.html'

with open(ABOUT, 'r', encoding='utf-8') as fh:
    original = fh.read()

pattern = r'<section class="ab-hero">.*?</section>'
new_content, n = re.subn(pattern, NEW_HERO, original, count=1, flags=re.DOTALL)

if n == 0:
    raise RuntimeError('Could not find <section class="ab-hero"> block in about.html')

with open(ABOUT, 'w', encoding='utf-8') as fh:
    fh.write(new_content)

print(f'[OK] Replaced ab-hero section in {ABOUT}')

# ── 3.  BUMP CACHE BUSTERS IN ALL *.html FILES ───────────────────────────────
NEW_VERSION = 'v=20260830_final_polish_27'
CACHE_PATTERN = re.compile(r'v=[\w._-]+')

html_files = glob.glob('*.html')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as fh:
        text = fh.read()
    updated, count = CACHE_PATTERN.subn(NEW_VERSION, text)
    if count:
        with open(fname, 'w', encoding='utf-8') as fh:
            fh.write(updated)
        print(f'[OK] {fname}: bumped {count} cache-buster(s) -> {NEW_VERSION}')
    else:
        print(f'[--] {fname}: no cache-busters found')

print('\nDone.')
