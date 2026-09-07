import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()

idx = c.find('<div class="arc-row" style="background: rgba(11,29,58,0.02);">')
if idx == -1:
    idx = c.find('<div class="arc-row"')
    
DATE = "Wednesday, 2nd September 2026"
TITLE = "Daily DSE Wrap | Wednesday, 2nd September 2026"
EXCERPT = "The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion, a 75% drop from Tuesday's NMB-driven surge, while the government bond market exploded to TZS 37.92 billion — the largest single-day figure this quarter. The message is clear: institutions are not abandoning the market; they are rushing to lock in double-digit tax-free yields before they compress further."

# We need to insert right after the 03 Sep arc-row. Let's find the closing tag of 03 Sep arc-row
first_row_idx = c.find('<div class="arc-row">')

# Search for the next arc-row
next_row_idx = c.find('<div class="arc-row"', first_row_idx + 10)
if next_row_idx != -1:
    new_entry = (
        f'<div class="arc-row" style="background: rgba(11,29,58,0.02);">\n'
        f'                <div class="arc-date">{DATE}</div>\n'
        f'                <div class="arc-title">\n'
        f'                    <a href="/dse-wrap-2026-09-02">{TITLE}</a>\n'
        f'                </div>\n'
        f'                <div class="arc-excerpt">{EXCERPT[:196]}...</div>\n'
        f'            </div>\n            '
    )
    # The existing next_row needs to have no background, since it's the 3rd one now.
    # We will just insert new_entry before next_row_idx, and replace the background style in next_row_idx
    c = c[:next_row_idx] + new_entry + c[next_row_idx:].replace(' style="background: rgba(11,29,58,0.02);"', '', 1)
    
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("OK, inserted 02 Sep into archive.")
else:
    print("Could not find the second arc-row.")
