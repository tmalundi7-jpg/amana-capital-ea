#!/usr/bin/env python3
"""
fix_pages_group3.py
Audit and fix the 5 most recent DSE daily wrap HTML pages.
"""
import os
import re

BASE = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea'
INCLUDES_DIR = os.path.join(BASE, '_includes')

TARGET_FILES = [
    'dse-wrap-2026-08-28.html',
    'dse-wrap-2026-08-27.html',
    'dse-wrap-2026-08-26.html',
    'dse-wrap-2026-08-21.html',
    'dse-wrap-2026-08-20.html',
]

KEY_TAKEAWAYS = {
    'dse-wrap-2026-08-28.html': (
        'Friday 28 August 2026',
        [
            'Equity turnover surged to TZS 21.59 bn driven by a 7.35 mn-share NMB block trade on the pre-arranged board.',
            'Foreign selling reached 21.68% of turnover with zero foreign buying; local capital absorbed all supply without distress.',
            'NMB +4.6% to 2,030 post-split; PAL +13.1%; TOL +9.4%. DCB fell 5.2%; MCB fell 4.8%.',
            'Market capitalisation rose from TZS 36.53 bn to TZS 38.23 bn (+4.6%).',
            'Bond market: TZS 12.55 bn traded; government bond yields 10.4-11.5% tax-free.',
        ]
    ),
    'dse-wrap-2026-08-27.html': (
        'Thursday 27 August 2026',
        [
            'Equity turnover surged to TZS 21.59 bn on a historic NMB block trade of 7.36 mn shares.',
            'Foreign selling 21.68% of turnover vs zero foreign buying; local institutions absorbed all supply.',
            'NMB +4.6% to 2,030 post-split; PAL +13.1%; TOL +9.4%. DCB fell 5.2%; MCB fell 4.8%.',
            'Market cap rose to TZS 38.23 bn, a genuine 4.6% increase despite a full foreign exit.',
            'Bond turnover: TZS 12.55 bn in government paper; yields 10.4-11.5% tax-free.',
        ]
    ),
    'dse-wrap-2026-08-26.html': (
        'Monday 24 August 2026',
        [
            'NMB 10-for-1 share split took effect; price adjusted from approx TZS 17,700 to 1,850.',
            'Equity turnover surged 458% to TZS 7.72 bn; shares traded up 429% to 3.83 mn.',
            'DSEI dropped from 4,250 to 1,364 - an index rebase, not a market decline. Market cap rose 2.5% to TZS 37.45 tn.',
            'MBP led gainers at +12.5% to 2,070. DCB fell 4.0% to 485, reversing its speculative spike.',
            'NMB now trades under the 5% daily price band (price is above TZS 1,000).',
        ]
    ),
    'dse-wrap-2026-08-21.html': (
        'Friday 21 August 2026',
        [
            'Equity turnover fell to TZS 1.38 bn, the lowest in over a week, as investors stepped back ahead of the weekend.',
            'Bond turnover surged to TZS 15.54 bn, signalling decisive rotation into tax-free fixed-income assets.',
            'CRDB unchanged at 2,690; NMB did not trade - possible quiet period ahead of ex-dividend announcement.',
            'DCB fell 9.0% to 505; MCB dropped 3.4%; NICO lost 3.8%.',
            'Daily price bands still apply on quiet days - always verify before placing orders.',
        ]
    ),
    'dse-wrap-2026-08-20.html': (
        'Thursday 20 August 2026',
        [
            'Equity turnover fell 55.7% to TZS 3.16 bn as block-driven activity normalised.',
            'Zero foreign buying and selling recorded for the first time in months - the DSE is now a fully locally owned market.',
            'DCB fell 11.2% to 555, reversing its block-driven speculative spike - a textbook pullback.',
            'CRDB unchanged at 2,690 despite absorbing a 100,000-share block. VODA flat at 1,030.',
            'Bond market: TZS 5.83 bn in government paper; 25-yr 13.25% bond yielding 11.0-12.1% tax-free.',
        ]
    ),
}

KT_TPL = (
    '<div class="key-takeaways" style="background: #fff8e8; border-left: 4px solid #e5b13b; '
    'border-radius: 6px; padding: 1.5rem 2rem; margin: 1.5rem 0 2rem 0; '
    'box-shadow: 0 2px 8px rgba(229,177,59,0.10);">\n'
    '  <h3 style="color: #0a1628; margin-top: 0; margin-bottom: 0.75rem; font-size: 1.1rem; '
    'letter-spacing: 0.02em;">&#9733; Key Takeaways &mdash; {date}</h3>\n'
    '  <ul style="margin: 0; padding-left: 1.4rem; color: #333; line-height: 1.75;">\n'
    '{items}\n'
    '  </ul>\n'
    '</div>'
)


def build_kt(fname):
    date, pts = KEY_TAKEAWAYS[fname]
    items = '\n'.join('    <li>' + p + '</li>' for p in pts)
    return KT_TPL.format(date=date, items=items)


def load_inc(name):
    path = os.path.join(INCLUDES_DIR, name)
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def fix_file(fname):
    path = os.path.join(BASE, fname)
    changes = []

    with open(path, encoding='utf-8', errors='replace') as f:
        content = f.read()
    orig = content

    # ── 1. Jekyll {% include %} tags ──────────────────────────────────────────
    def repl_inc(m):
        n = m.group(1).strip().strip("'\"")
        inc_path = os.path.join(INCLUDES_DIR, n)
        if os.path.isfile(inc_path):
            changes.append('[INCLUDE] Replaced {%% include "%s" %%} with inlined content' % n)
            return load_inc(n)
        changes.append('[INCLUDE] WARNING: %s not found in _includes/' % n)
        return m.group(0)

    c2 = re.sub(
        r'\{%-?\s*include\s+[\'"]([^\'"]+)[\'"]\s*-?%\}',
        repl_inc,
        content
    )
    if c2 != content:
        content = c2

    # ── 2. Escape garbage \1\n ────────────────────────────────────────────────
    c2 = re.sub(r'\\1\\n', '', content)
    if c2 != content:
        cnt = len(re.findall(r'\\1\\n', orig))
        changes.append('[ESCAPE] Removed %d instance(s) of \\1\\n garbage sequence' % cnt)
        content = c2

    # ── 3. style.min.css -> style.css?v=20260830 ─────────────────────────────
    c2 = re.sub(r'style\.min\.css(?:\?[^"\']*)?', 'style.css?v=20260830', content)
    if c2 != content:
        changes.append('[CSS] Replaced style.min.css with style.css?v=20260830')
        content = c2

    # ── 4. style.css?v=<old> -> style.css?v=20260830 ─────────────────────────
    c2 = re.sub(r'style\.css\?v=(?!20260830)[^"\'>\s]*', 'style.css?v=20260830', content)
    if c2 != content:
        changes.append('[CSS] Updated style.css version query string to v=20260830')
        content = c2

    # ── 5. Hamburger icon ─────────────────────────────────────────────────────
    # Replace literal U+2630 (☰) character first (most common garbled form)
    c2 = content.replace('\u2630', '&#9776;')
    if c2 != content:
        changes.append('[NAV] Replaced literal U+2630 (☰) hamburger character with &#9776;')
        content = c2

    # Then normalise inside button.mobile-toggle
    c2 = re.sub(
        r'(<button[^>]*mobile-toggle[^>]*>)\s*(?:&#9778;|&#8801;|&#x2630;|&#x2261;|&#9784;|&#9776;)\s*(</button>)',
        r'\1&#9776;\2',
        content, flags=re.IGNORECASE | re.DOTALL
    )
    if c2 != content:
        changes.append('[NAV] Normalised mobile-toggle hamburger to &#9776;')
        content = c2

    # ── 6. Dropdown arrows ────────────────────────────────────────────────────
    # Replace literal ▾ (U+25BE) and ▼ (U+25BC)
    c2 = content.replace('\u25be', '&#9660;').replace('\u25bc', '&#9660;')
    if c2 != content:
        changes.append('[NAV] Replaced literal dropdown arrow characters with &#9660;')
        content = c2

    c2 = re.sub(r'(?:&#9662;|&#x25be;|&#x25bc;)', '&#9660;', content)
    if c2 != content:
        changes.append('[NAV] Normalised dropdown arrow entities to &#9660;')
        content = c2

    # ── 7. Key Takeaway box ───────────────────────────────────────────────────
    if not re.search(r'key-takeaways', content, re.IGNORECASE):
        # Find the dse-header-box div and then the first </p> after it
        hdr_pos = content.find('dse-header-box')
        search_from = 0
        if hdr_pos != -1:
            # Find the closing </div> of the header box
            hdr_end = content.find('</div>', hdr_pos)
            if hdr_end != -1:
                search_from = hdr_end + len('</div>')

        first_para_end = content.find('</p>', search_from)
        if first_para_end != -1:
            insert_pos = first_para_end + len('</p>')
            kt_block = '\n\n' + build_kt(fname) + '\n'
            content = content[:insert_pos] + kt_block + content[insert_pos:]
            changes.append('[KEY-TAKEAWAY] Inserted key-takeaways box after intro paragraph')
        else:
            changes.append('[KEY-TAKEAWAY] WARNING: Could not locate intro </p> for insertion')
    else:
        changes.append('[KEY-TAKEAWAY] Already present — skipped')

    # ── Save ──────────────────────────────────────────────────────────────────
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, changes


def main():
    print('=' * 65)
    print('fix_pages_group3.py  —  DSE Wrap Audit and Fix')
    print('=' * 65)
    total_changed = 0

    for fname in TARGET_FILES:
        print('\n[FILE] %s' % fname)
        path = os.path.join(BASE, fname)
        if not os.path.isfile(path):
            print('  ERROR: File not found at %s' % path)
            continue
        changed, log = fix_file(fname)
        for entry in log:
            print('  %s' % entry)
        if changed:
            print('  => FILE UPDATED')
            total_changed += 1
        else:
            print('  => No changes needed')

    print('\n' + '=' * 65)
    print('Done. %d/%d file(s) updated.' % (total_changed, len(TARGET_FILES)))
    print('=' * 65)


if __name__ == '__main__':
    main()
