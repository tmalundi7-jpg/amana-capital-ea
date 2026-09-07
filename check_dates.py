import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()
dates = re.findall(r'letter-spacing:\s*0\.5px;">(.*?)</div>', c)
print('First 10 dates in archive:')
for d in dates[:10]:
    print(d)
