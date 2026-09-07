import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('market-intelligence-archive.html', encoding='utf-8').read()

# Check current state of archive - show first 2 arc-rows
idx = c.find('arc-row')
print("First 800 chars of arc-row section:")
print(c[max(0,idx-30):idx+800])
