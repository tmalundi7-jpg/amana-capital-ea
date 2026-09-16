import re
import json
import shutil
import datetime

# 1. Load data
with open('extracted_data.json', 'r', encoding='utf-8') as f:
    wrap_data = json.load(f)

with open('extracted_prices.json', 'r', encoding='utf-8') as f:
    prices_data = json.load(f)

# 2. Prepare wrap data
excerpt = 'The Dar es Salaam Stock Exchange delivered a sobering but instructive session on Wednesday. After two days of falling bond turnover that suggested institutional money was rotating into equities, the bond market came roaring back with TZS 35.95 billion in trades — the largest in a week.'

# Generate HTML for current prices
prices_html = ''
for row in prices_data['tables'][0][1:]:
    ticker, comp, sector, price, change, vol, turn = row
    
    change_class = ''
    if '+' in change:
        change_class = ' change-positive'
    elif '-' in change or '–' in change: # Handle both hyphen and en-dash
        change_class = ' change-negative'
        
    prices_html += f'''                            <tr>
                                <td><strong>{ticker}</strong></td>
                                <td>{comp}</td>
                                <td style="color: var(--mist);">{sector}</td>
                                <td class="text-right"><strong>{price}</strong></td>
                                <td class="text-right{change_class}"><strong>{change}</strong></td>
                                <td class="text-right">{vol}</td>
                                <td class="text-right">{turn}</td>
                            </tr>
'''

# Update current-prices.html
with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the date
c = re.sub(r'7 September 2026', '9 September 2026', c)
c = re.sub(r'07 Sep 2026', '09 Sep 2026', c)

# Replace table body
c = re.sub(r'<tbody>.*?</tbody>', f'<tbody>\n{prices_html}                        </tbody>', c, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated current-prices.html')

# Update market-intelligence-archive.html
with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
    arc = f.read()

# We need to PREPEND the 07 Sep row to the top of the archive grid.
# The grid has id="archive-grid" or similar. Let's check format.
# Wait, let's just find the first archive-card and insert before it.
row_07_sep = '''<div class="archive-card">
<div class="archive-date">07 Sep 2026</div>
<div class="archive-badge badge-equity">Equities</div>
<h3 class="archive-content-title"><a href="/dse-wrap-2026-09-07">Daily DSE Wrap | Monday, 7th September 2026</a></h3>
<p class="archive-content-excerpt">Bond money floods into equities as the rotation signal fires. Equity turnover more than doubled to TZS 17.31 billion while bond turnover collapsed to TZS 7.99 billion. The TSI crossed 10,000...</p>
</div>
'''

if '07 Sep 2026' not in arc:
    arc = re.sub(r'(<div class="archive-grid">)', r'\g<1>\n' + row_07_sep, arc)
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(arc)
    print('Updated market-intelligence-archive.html')

# Update market-intelligence.html
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    mi = f.read()

mi = re.sub(r'07 Sep 2026', '09 Sep 2026', mi)
mi = re.sub(r'7 September 2026', '9 September 2026', mi)

# Replace the archive row for 07 Sep with 09 Sep
old_archive_row = r'<a class="archive-row" href="/dse-wrap-2026-09-07">.*?</a>'
new_archive_row = '''<a class="archive-row" href="/dse-wrap-2026-09-09">
<div class="archive-date">09 Sep<br/>2026</div>
<div>
<div class="archive-badge badge-equity">Equities</div>
<div class="archive-content-title">Daily DSE Wrap | Wednesday, 9th September 2026</div>
<div class="archive-content-excerpt">The Dar es Salaam Stock Exchange delivered a sobering but instructive session on Wednesday. After two days of falling bond turnover that suggested institutional money was rotating into equities...</div>
</div>
<span class="archive-cta">Read &rarr;</span>
</a>'''

mi = re.sub(old_archive_row, new_archive_row, mi, flags=re.DOTALL)

# Update Snapshot values
mi = re.sub(r'(id="mi-dsei">).*?(</div>)', r'\g<1>4,581.18\g<2>', mi)
mi = re.sub(r'(id="mi-tsi">).*?(</div>)', r'\g<1>10,152.62\g<2>', mi)
mi = re.sub(r'(id="mi-turnover">).*?(</div>)', r'\g<1>TZS 6.23 bn\g<2>', mi)
mi = re.sub(r'(id="mi-deals">).*?(</div>)', r'\g<1>3,762\g<2>', mi)
mi = re.sub(r'(id="mi-volume">).*?(</div>)', r'\g<1>2,839,603\g<2>', mi)

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(mi)
print('Updated market-intelligence.html')
