import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

def style_row(m):
    inner = m.group(1)
    # The first td is ticker
    inner = re.sub(r'<td>([A-Z]+)</td>', r'<td><strong>\1</strong></td>', inner, count=1)
    # The third td is sector
    def style_sector(m_sec):
        return f'<td><span class="sector-badge">{m_sec.group(1)}</span></td>'
    # Find the 3rd td.
    tds = re.findall(r'<td.*?>(.*?)</td>', inner)
    if len(tds) >= 7:
        sector = tds[2]
        inner = inner.replace(f'<td>{sector}</td>', f'<td><span class="sector-badge">{sector}</span></td>')
    return f'<tr>\n{inner}\n</tr>'

c = re.sub(r'<tr>\n(.*?)\n</tr>', style_row, c, flags=re.DOTALL)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)
