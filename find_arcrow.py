import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()
needle = '<div class="arc-row">'
idx = c.find(needle)
print('First arc-row at:', idx)
if idx != -1:
    print(c[idx:idx+400])
