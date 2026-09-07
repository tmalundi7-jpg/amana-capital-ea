import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Look for gainers/losers structure and snapshot date areas
for filename in ['index.html', 'market-intelligence.html']:
    print(f"\n===== {filename} =====")
    c = open(filename, encoding='utf-8').read()
    
    # Find snapshot date area
    for pat in ['September 2026', 'snapshot-date', 'terminal-date', 'Terminal Feed', 'End-of-day', 'snapshot']:
        idx = c.find(pat)
        if idx != -1:
            print(f"  [{pat}] context: {c[max(0,idx-80):idx+100].replace(chr(10),' ')}")

    # Find gainer/loser sections
    for pat in ['home-gainers', 'home-losers', 'gainer', 'loser', 'Gainer', 'Loser']:
        idx = c.find(pat)
        if idx != -1:
            print(f"\n  [{pat}]:\n  {c[max(0,idx-50):idx+200].replace(chr(10),' ')}")
            break
