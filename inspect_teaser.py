import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('index.html', encoding='utf-8').read()

# Teaser section
for pat in ['teaser', 'Today\'s DSE', 'Latest Research', 'Read the Full Wrap']:
    idx = c.find(pat)
    if idx != -1:
        print(f"[{pat}]:")
        print(c[max(0,idx-50):idx+600])
        print('---')
        break

c2 = open('market-intelligence.html', encoding='utf-8').read()

# MI spotlight / archive featured section
for pat in ['spotlight', 'featured', 'arc-spotlight', 'archive-featured']:
    idx = c2.find(pat)
    if idx != -1:
        print(f"\nMI [{pat}]:")
        print(c2[max(0,idx-50):idx+600])
        print('---')
        break

# MI date / report date
idx = c2.find('Latest Report')
if idx == -1:
    idx = c2.find('latest-report')
if idx != -1:
    print(f"\nMI date area:")
    print(c2[max(0,idx-50):idx+300])
