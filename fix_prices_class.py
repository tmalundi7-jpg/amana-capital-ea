import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# TCCL has change-neutral class but it should be change-negative for -4.0%
c = open('current-prices.html', encoding='utf-8').read()

# Fix all negatives that got classified as neutral (the – is an en-dash \u2013)
c = c.replace('<td class="change-neutral">\u20134.0%</td>', '<td class="change-negative">\u20134.0%</td>')
c = c.replace('<td class="change-neutral">\u20132.1%</td>', '<td class="change-negative">\u20132.1%</td>')
c = c.replace('<td class="change-neutral">\u20131.8%</td>', '<td class="change-negative">\u20131.8%</td>')
c = c.replace('<td class="change-neutral">\u20131.6%</td>', '<td class="change-negative">\u20131.6%</td>')
c = c.replace('<td class="change-neutral">\u20131.4%</td>', '<td class="change-negative">\u20131.4%</td>')
c = c.replace('<td class="change-neutral">\u20131.3%</td>', '<td class="change-negative">\u20131.3%</td>')
c = c.replace('<td class="change-neutral">\u20131.0%</td>', '<td class="change-negative">\u20131.0%</td>')
c = c.replace('<td class="change-neutral">\u20130.2%</td>', '<td class="change-negative">\u20130.2%</td>')

# Generic: any change-neutral cell containing – should be change-negative
c = re.sub(r'class="change-neutral">(\u2013[^<]+)</td>',
           r'class="change-negative">\1</td>', c)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("OK  current-prices.html negative changes fixed")

# Also fix index.html h3 teaser-prem-title - the regex found a CSS block not the content
# Need to find it after TEASER_CARD_START
c2 = open('index.html', encoding='utf-8').read()
idx = c2.find('TEASER_CARD_START')
if idx == -1:
    idx = c2.find('teaser-premium')
    
block = c2[idx:idx+2000]
print("\nTeaser h3 in block:")
h3m = re.search(r'<h3 class="teaser-prem-title">(.*?)</h3>', block, re.DOTALL)
if h3m:
    print(repr(h3m.group(1)[:120]))
