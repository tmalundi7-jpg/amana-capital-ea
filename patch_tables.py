import bs4
import glob

files = [
    'dse-wrap-2026-08-14.html',
    'dse-wrap-2026-08-17.html',
    'dse-wrap-2026-08-19.html',
    'dse-wrap-2026-08-20.html'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            soup = bs4.BeautifulSoup(file.read(), 'html.parser')
            
        modified = False
        
        for table in soup.find_all('table'):
            tbody = table.find('tbody')
            if not tbody:
                continue
                
            for i, tr in enumerate(tbody.find_all('tr')):
                # Even/odd coloring
                if i % 2 == 1:
                    tr['style'] = "background-color: var(--cream);"
                else:
                    if 'style' in tr.attrs:
                        del tr['style']
                        
                cells = tr.find_all('td')
                for j, td in enumerate(cells):
                    text_content = td.get_text().strip()
                    style = "padding: 1rem;"
                    
                    if j == 0:
                        # First column
                        style += " font-weight: 600;"
                        
                        # Check if strong tag already exists
                        if not td.find('strong'):
                            inner_text = "".join(str(c) for c in td.contents)
                            strong_tag = soup.new_tag('strong', style="color: #000;")
                            strong_tag.append(bs4.BeautifulSoup(inner_text, 'html.parser'))
                            td.clear()
                            td.append(strong_tag)
                        else:
                            # Update existing strong tag
                            strong_tag = td.find('strong')
                            strong_tag['style'] = "color: #000;"
                    else:
                        # Gain/Loss styling
                        if '+' in text_content and ('%' in text_content or 'pts' in text_content or text_content.startswith('+')):
                            style += " color: var(--gain); font-weight: 600;"
                        elif ('-' in text_content or '–' in text_content or '−' in text_content) and ('%' in text_content or 'pts' in text_content or text_content.startswith('-') or text_content.startswith('–')):
                            style += " color: var(--loss); font-weight: 600;"
                            
                    td['style'] = style
                    modified = True
                    
        if modified:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Patched tables in {f}")
        else:
            print(f"No tables found in {f}")
            
    except Exception as e:
        print(f"Error processing {f}: {e}")

print("Done patching.")
