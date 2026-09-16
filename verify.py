import re
from bs4 import BeautifulSoup

with open('current-prices.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

table = soup.find('table', class_='gold-grid-table')
if table:
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 5:
            ticker = cells[0].get_text(strip=True)
            change_cell = cells[4]
            change_val = change_cell.get_text(strip=True)
            classes = change_cell.get('class', [])
            print(f"{ticker}: {change_val} | Classes: {classes}")
