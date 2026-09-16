import re
import json

with open('extracted_prices.json', 'r', encoding='utf-8') as f:
    prices_data = json.load(f)

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

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<tbody>.*?</tbody>', f'<tbody>\n{prices_html}                        </tbody>', c, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Restored CP table")
