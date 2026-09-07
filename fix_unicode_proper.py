import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('dse-wrap-2026-09-04.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix common unicode issues from mammoth
c = c.replace('?"', '—')
c = c.replace('?T', "'")
c = c.replace('', '')

with open('dse-wrap-2026-09-04.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Cleaned up unicode properly.")
