import bs4

with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

# First, remove the bad JHL block from the top
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

# Let's see the order of counters in the table
soup = bs4.BeautifulSoup(text, 'html.parser')
table = soup.find('table', class_='data-table')
if table:
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            if tds:
                print(tds[0].get_text(strip=True))
