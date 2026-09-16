
# Diagnose current-prices.html block trades section before update

with open('current-prices.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
m = re.search(r'block-trades-container', content)
if m:
    print('block-trades-container found at:', m.start())
    print('CONTEXT:', repr(content[m.start():m.start()+800]))
else:
    print('block-trades-container NOT found')
    # Find the nearest thing
    m2 = re.search(r'block.trad', content, re.IGNORECASE)
    if m2:
        print('Alternative found:', repr(content[m2.start()-100:m2.start()+400]))
    else:
        print('No block trade section found at all')
        # Find where NMB appears
        idx = content.find('NMB')
        if idx >= 0:
            print('NMB at:', idx)
            print(repr(content[idx-200:idx+300]))
