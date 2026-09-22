import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_block = '''                                <tr>
                                    <td>JHL</td>
                                    <td>Jubilee Holdings</td>
                                    <td style="color: #9A9490;">Banks & Finance</td>
                                    <td class="text-right">8,700</td>
                                    <td class="text-right change-positive" style="font-weight: 400;">+0.6%</td>
                                    <td class="text-right">60,097</td>
                                    <td class="text-right">522,843,900</td>
                                </tr>\n'''
text = text.replace(bad_block, '')

# Now we need to insert JHL after JATU
# Let's find the JATU block
jatu_match = re.search(r'<tr>\s*<td>JATU</td>.*?</tr>', text, re.DOTALL)
if jatu_match:
    jatu_block = jatu_match.group(0)
    
    jhl_block = '''
                                <tr>
                                    <td>JHL</td>
                                    <td>Jubilee Holdings</td>
                                    <td style="color: #9A9490;">Banks & Finance</td>
                                    <td class="text-right">8,700</td>
                                    <td class="text-right change-positive" style="font-weight: 400;">+0.6%</td>
                                    <td class="text-right">60,097</td>
                                    <td class="text-right">522,843,900</td>
                                </tr>'''
    
    text = text.replace(jatu_block, jatu_block + jhl_block)
    
with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done fixing JHL.')
