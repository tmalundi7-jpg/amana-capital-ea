from bs4 import BeautifulSoup
import re
with open('dse-wrap-2026-09-17.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's isolate the title, date, and content manually
soup = BeautifulSoup(html, 'html.parser')
main = soup.find('main')
container = main.find('div', class_='container')
inner = container.find('div')
if not inner:
    inner = container

# we want to keep the breadcrumbs, title, date, but replace everything after the date until the disclaimer.
