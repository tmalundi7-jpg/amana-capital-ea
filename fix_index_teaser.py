import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<div class="teaser-prem-date">Tuesday, 1st September 2026</div>', '<div class="teaser-prem-date">Wednesday, 2nd September 2026</div>')
c = c.replace('<h3 class="teaser-prem-title">Daily DSE Wrap | Tuesday, 1st September 2026</h3>', '<h3 class="teaser-prem-title">Daily DSE Wrap | Wednesday, 2nd September 2026</h3>')
old_body = 'The Dar es Salaam Stock Exchange began September with a session that may prove to be the most significant of the quarter. Equity turnover climbed to TZS 16.39 billion, the highest in recent memory, driven by NMB\'s continuing post-split activity and a surge in CRDB volume. But the headline numbers don\'t tell the real story. For the first time in weeks, foreign investors were net neutral — buying almost exactly as much as they sold. At the same time, government bond turnover collapsed by 68% from Monday\'s record high. Put these two signals together, and the message is clear: the handoff from foreign to local capital is complete, and the long-awaited rotation from bonds into equities may have begun.'
new_body = 'The Dar es Salaam Stock Exchange delivered a session of striking contrasts on Wednesday. Equity trading cooled dramatically to TZS 4.01 billion, a 75% drop from Tuesday\'s NMB-driven surge, while the government bond market exploded to TZS 37.92 billion — the largest single-day figure this quarter. The message is clear: institutions are not abandoning the market; they are rushing to lock in double-digit tax-free yields before they compress further.'
c = c.replace(old_body, new_body)

# And replace the link from -01 to -02 just in case it didn't work before
c = c.replace('href="/dse-wrap-2026-09-01"', 'href="/dse-wrap-2026-09-02"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed index.html teaser!")
