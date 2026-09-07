import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('index.html', encoding='utf-8').read()

idx = c.find('TEASER_CARD_START')
block = c[idx:idx+2500]

# Replace Top Gainer:
block = re.sub(
    r'(<div class="teaser-prem-stat-label">Top Gainer</div>.*?<span>)[^<]*(</span>.*?<span[^>]*>)[^<]*(</span>)',
    r'\g<1>MBP\g<2>+8.2%\g<3>',
    block, flags=re.DOTALL
)

# Replace Top Loser if it exists (not seen in the snippet above, but let's check)
block = re.sub(
    r'(<div class="teaser-prem-stat-label">Top Loser</div>.*?<span>)[^<]*(</span>.*?<span[^>]*>)[^<]*(</span>)',
    r'\g<1>TCCL\g<2>-4.0%\g<3>',
    block, flags=re.DOTALL
)

c = c[:idx] + block + c[idx+2500:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated teaser Gainer/Loser.")
