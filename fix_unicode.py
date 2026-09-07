import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('dse-wrap-2026-09-04.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the specific artifacts created by the earlier script
c = c.replace('?"', '—')

with open('dse-wrap-2026-09-04.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Fixed encoding artifacts.")
