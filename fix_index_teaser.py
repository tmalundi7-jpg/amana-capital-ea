import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('index.html', encoding='utf-8').read()

DSEI = "4,442.62"
TURNOVER = "TZS 42.93 bn"
GAIN = "MBP +8.2%"
LOSS = "TCCL -4.0%"

idx = c.find('TEASER_CARD_START')
if idx != -1:
    block = c[idx:idx+2500]
    
    # We want to replace the teaser-prem-stat-value contents in the block
    block = re.sub(
        r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
        rf'\g<1>{DSEI}\g<2>',
        block
    )
    block = re.sub(
        r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
        rf'\g<1>{TURNOVER}\g<2>',
        block
    )
    
    # Wait, the Top Gainer and Top Loser stats also exist!
    # Let's see how they are structured
    print("Top Gainer and Loser part of block:")
    print(block[block.find('Top Gainer'):block.find('Top Gainer')+500])
    
    # We will replace these manually
    c = c[:idx] + block + c[idx+2500:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated teaser stats.")
