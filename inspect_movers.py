import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for filename in ['index.html', 'market-intelligence.html']:
    print(f"\n===== {filename} =====")
    c = open(filename, encoding='utf-8').read()
    
    # Show the gainers section
    idx = c.find('home-gainers') if filename == 'index.html' else c.find('GAINERS_START')
    if idx != -1:
        print(f"\nGainers section (~400 chars):")
        print(c[idx:idx+500])
    
    # Show the losers section  
    idx = c.find('home-losers') if filename == 'index.html' else c.find('LOSERS_START')
    if idx != -1:
        print(f"\nLosers section (~400 chars):")
        print(c[idx:idx+500])

    # Show the snapshot subtitle (the "End-of-day" span)
    idx = c.find('End-of-day')
    if idx != -1:
        print(f"\nSnapshot subtitle:")
        print(c[max(0,idx-120):idx+150])
