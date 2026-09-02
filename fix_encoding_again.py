import re

with open('dse-wrap-2026-09-01.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the left arrow
c = c.replace('+? Back', '&larr; Back')
c = c.replace('? Back', '&larr; Back')

# Fix any stray encoding issues in the 1st Sep text just in case
c = c.replace('neutral ?" buying', 'neutral &mdash; buying')
c = c.replace('compressing ?" falling', 'compressing &mdash; falling')
c = c.replace('two weeks ?" the', 'two weeks &mdash; the')
c = c.replace('flow reversal ?" all', 'flow reversal &mdash; all')
c = c.replace('opportunities are there ?" in', 'opportunities are there &mdash; in')

c = c.replace('neutral ?" buying', 'neutral &mdash; buying')
c = c.replace('compressing ?" falling', 'compressing &mdash; falling')
c = c.replace('two weeks ?" the', 'two weeks &mdash; the')
c = c.replace('flow reversal ?" all', 'flow reversal &mdash; all')
c = c.replace('opportunities are there ?" in', 'opportunities are there &mdash; in')

c = c.replace('</em>A<a', '</em> <a')
c = c.replace('</a>Aand', '</a> and')
c = c.replace('</a>and', '</a> and')
c = c.replace('<strong>A', '<strong>')
c = c.replace('</strong>A', '</strong> ')

with open('dse-wrap-2026-09-01.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed encoding issues")
