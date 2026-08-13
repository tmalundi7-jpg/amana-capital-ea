import os
import re
from bs4 import BeautifulSoup

def fix_prices(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    for table in soup.find_all('table', class_='data-table'):
        # In current-prices, the change column is the 5th column (index 4)
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 4:
                td = tds[4]
                text = td.text.strip()
                if '%' in text:
                    # It's the change column
                    # Remove any existing color inline styles
                    style = td.get('style', '')
                    style = re.sub(r'color:\s*[^;]+;', '', style)
                    
                    if text.startswith('+'):
                        td['style'] = style + " color: var(--gain); font-weight: 600;"
                    elif text.startswith('-') or text.startswith('–') or text.startswith('?') or '–' in text or '?' in text:
                        # Sometimes word docs use weird minus signs
                        # If it's literally just 0.0%, don't color it red
                        if '0.0%' in text and not text.startswith('-') and not text.startswith('–'):
                            td['style'] = style
                        else:
                            td['style'] = style + " color: var(--loss); font-weight: 600;"
                    else:
                        td['style'] = style

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    fix_prices('current-prices.html')
    print("Fixed current-prices.html")
