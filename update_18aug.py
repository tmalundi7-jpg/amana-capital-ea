import re
import os
import shutil
from bs4 import BeautifulSoup

def update_18_aug():
    workspace = r'c:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea'
    os.chdir(workspace)

    # Backup files
    for file in ['index.html', 'market-intelligence-archive.html', 'current-prices.html']:
        shutil.copy(file, file + '.bak_18aug')

    # Data to inject
    dsei = '4,238.03'
    dsei_change = '–0.3%' # From text: –10.95 pts (–0.3%)
    tsi = '9,315.05'
    turnover = 'TZS 6.84 billion'
    top_mover = 'DCB +13.2%'
    listed_companies = '28'
    date_str = '18 Aug 2026'
    full_date_str = '18 August 2026'
    teaser_title = 'Block Trades Keep Local Investors Firmly in Control'
    teaser_body = 'The Dar es Salaam Stock Exchange delivered another session of healthy, locally driven trading on Tuesday, with turnover climbing to TZS 6.84 billion. Large pre-arranged transactions in NICO and continued strong activity in DCB highlighted the depth of institutional interest, while foreign investors remained almost entirely on the sidelines. The All-Share Index eased only slightly, consolidating near its monthly high.'
    wrap_link = '/dse-wrap-2026-08-18'

    gainers_html = """
            <span>DCB <span style="color:var(--gain)">+13.2%</span></span>
            <span>MCB <span style="color:var(--gain)">+3.7%</span></span>
            <span>KCB <span style="color:var(--gain)">+1.0%</span></span>
            <span>NICO <span style="color:var(--gain)">+0.8%</span></span>
    """
    
    losers_html = """
            <span>TCCL <span style="color:var(--loss)">-3.6%</span></span>
            <span>TBL <span style="color:var(--loss)">-1.4%</span></span>
            <span>SWIS <span style="color:var(--loss)">-0.8%</span></span>
            <span>CRDB <span style="color:var(--loss)">-0.4%</span></span>
    """

    # --- Update index.html ---
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    soup = BeautifulSoup(idx_html, 'html.parser')

    # Hero stats
    dsei_label = soup.find(string=re.compile('DSEI — End of Day'))
    if dsei_label:
        dsei_label.find_next('div').string = dsei
        badge = dsei_label.find_parent('div').find_parent('div').find_next_sibling('span')
        badge.string = f'▼ {dsei_change}'
        badge['class'] = 'home-stat-badge down'
        if 'up' in badge['class']: badge['class'].remove('up')
        badge['style'] = 'background: rgba(239,68,68,0.15); color: #ef4444;'

    turnover_label = soup.find(string=re.compile('Daily Turnover'))
    if turnover_label:
        turnover_label.find_next('div').string = turnover
        badge = turnover_label.find_parent('div').find_parent('div').find_next_sibling('span')
        badge.string = '▲ +43.5%' 
        badge['class'] = 'home-stat-badge up'
        if badge.has_attr('style'): del badge['style']

    top_mover_label = soup.find(string=re.compile('Top Mover'))
    if top_mover_label:
        top_mover_label.find_next('div').string = top_mover
        badge = top_mover_label.find_parent('div').find_parent('div').find_next_sibling('span')
        badge.string = '18 Aug 2026'

    # Live snapshot
    home_dsei = soup.find(id='home-dsei')
    if home_dsei:
        home_dsei.clear()
        home_dsei.append(f'{dsei} ')
        span = soup.new_tag('span', attrs={'class': 'down'})
        span.string = '▼'
        span['style'] = 'color: #ef4444;'
        home_dsei.append(span)

    home_tsi = soup.find(id='home-tsi')
    if home_tsi:
        home_tsi.clear()
        home_tsi.append(f'{tsi} ')
        span = soup.new_tag('span', attrs={'class': 'down'})
        span.string = '▼'
        span['style'] = 'color: #ef4444;'
        home_tsi.append(span)

    home_turnover = soup.find(id='home-turnover')
    if home_turnover:
        home_turnover.string = turnover

    home_gainers = soup.find(id='home-gainers')
    if home_gainers:
        home_gainers.clear()
        home_gainers.append(BeautifulSoup(gainers_html, 'html.parser'))

    home_losers = soup.find(id='home-losers')
    if home_losers:
        home_losers.clear()
        home_losers.append(BeautifulSoup(losers_html, 'html.parser'))

    snapshot_date = soup.find(id='home-snapshot-date')
    if snapshot_date:
        snapshot_date.string = f'Live Terminal Feed | End-of-day, {full_date_str}'

    # Teaser section
    teaser_date = soup.find('div', class_='teaser-prem-date')
    if teaser_date:
        teaser_date.string = f'Tuesday, 18th August 2026'
    
    teaser_h3 = soup.find('h3', class_='teaser-prem-title')
    if teaser_h3:
        teaser_h3.string = teaser_title
        
    teaser_p = soup.find('p', class_='teaser-prem-body')
    if teaser_p:
        teaser_p.string = teaser_body
        
    teaser_link = soup.find('a', href=re.compile(r'/dse-wrap-'))
    if teaser_link:
        teaser_link['href'] = wrap_link
        
    # Update teaser stats
    stat_dsei = soup.find(string='DSEI')
    if stat_dsei:
        stat_dsei.find_next('div').string = dsei
        
    stat_turnover = soup.find(string='Turnover')
    if stat_turnover:
        stat_turnover.find_next('div').string = turnover
        
    stat_gainer = soup.find(string='Top Gainer')
    if stat_gainer:
        stat_gainer.find_next('div').string = top_mover
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))


    # --- Update current-prices.html ---
    with open('extracted_18_aug_data_full.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    prices = []
    in_prices = False
    for line in lines:
        line = line.strip()
        if line.startswith('Ticker | Company | Sector'):
            in_prices = True
            continue
        if in_prices:
            if not line or line.startswith('¹') or line.startswith('Change (%)'):
                if line.startswith('¹') or line.startswith('Change (%)'):
                    pass
                if not line and prices:
                    break
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                prices.append(parts)

    with open('current-prices.html', 'r', encoding='utf-8') as f:
        cp_html = f.read()
    
    soup_cp = BeautifulSoup(cp_html, 'html.parser')
    
    for elem in soup_cp.find_all(string=re.compile(r'17 August 2026|17th August 2026')):
        elem.replace_with(elem.replace('17 August', '18 August').replace('17th August', '18th August'))
        
    tbody = soup_cp.find('tbody')
    if tbody:
        tbody.clear()
        for p in prices:
            tr = soup_cp.new_tag('tr')
            for i, val in enumerate(p):
                if i == 4: # change
                    td_change = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;  font-weight: 600;")
                    c_val = val.replace('%','').replace('–','-').replace('+','')
                    try:
                        c_float = float(c_val)
                    except:
                        c_float = 0.0
                    
                    td_change['style'] += " color: var(--gain);" if c_float > 0 else (" color: var(--loss);" if c_float < 0 else "")
                    td_change.string = val
                    tr.append(td_change)
                else:
                    td = soup_cp.new_tag('td', style="padding: 1rem; border-bottom: 1px solid #eee;")
                    td.string = val
                    tr.append(td)
            tbody.append(tr)
            
    with open('current-prices.html', 'w', encoding='utf-8') as f:
        f.write(str(soup_cp))
        
        
    # --- Create dse-wrap-2026-08-18.html ---
    with open('wrap_template.html', 'r', encoding='utf-8') as f:
        wrap_html = f.read()
        
    full_text = "".join(lines)
    wrap_parts = full_text.split('=== Current Prices')
    wrap_content = wrap_parts[0]
    
    html_content = ""
    in_table = False
    
    for line in wrap_content.split('\n')[3:]: # Skip title lines
        line = line.strip()
        if not line:
            continue
        if line.startswith('1. Market Snapshot') or line.startswith('2. Top Movers') or line.startswith('3. In Focus') or line.startswith('4. Today') or line.startswith('5. Bond Market') or line.startswith('6. Strategic Outlook') or line.startswith('7. Professional') or line.startswith('8. Considerations'):
            html_content += f'<h3 style="margin-top:2rem;">{line}</h3>\n'
            in_table = False
        elif '|' in line:
            if not in_table:
                html_content += '<div style="overflow-x:auto;"><table class="prices-table" style="width:100%; text-align:left; border-collapse: collapse; margin-bottom: 1.5rem;">\n'
                html_content += '<thead><tr style="background: rgba(200,150,46,0.1);">'
                for th in line.split('|'):
                    html_content += f'<th style="padding: 0.75rem; border-bottom: 2px solid var(--gold);">{th.strip()}</th>'
                html_content += '</tr></thead><tbody>\n'
                in_table = True
            else:
                html_content += '<tr>'
                for td in line.split('|'):
                    html_content += f'<td style="padding: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05);">{td.strip()}</td>'
                html_content += '</tr>\n'
        else:
            if in_table:
                html_content += '</tbody></table></div>\n'
                in_table = False
            html_content += f'<p>{line}</p>\n'
    if in_table:
        html_content += '</tbody></table></div>\n'

    soup_wrap = BeautifulSoup(wrap_html, 'html.parser')
    
    title_tag = soup_wrap.find('title')
    if title_tag:
        title_tag.string = "Daily DSE Wrap - 18 August 2026 | Amana Capital EA"
        
    date_badge = soup_wrap.find('div', class_='article-meta-badge')
    if date_badge:
        date_badge.string = "18 August 2026"
        
    article_title = soup_wrap.find('h1', class_='article-title')
    if article_title:
        article_title.string = teaser_title
        
    article_body = soup_wrap.find('div', class_='article-body')
    if article_body:
        article_body.clear()
        article_body.append(BeautifulSoup(html_content, 'html.parser'))
        
    with open('dse-wrap-2026-08-18.html', 'w', encoding='utf-8') as f:
        f.write(str(soup_wrap))
        

    # --- Update market-intelligence-archive.html ---
    with open('market-intelligence-archive.html', 'r', encoding='utf-8') as f:
        mia_html = f.read()
        
    new_archive_row = f"""<a class="archive-row" href="/dse-wrap-2026-08-18">
                                    <div class="archive-date">18 Aug<br>2026</div>
                                    <div>
                                        <div class="archive-badge badge-equity">Equities</div>
                                        <div class="archive-content-title">{teaser_title}</div>
                                        <div class="archive-content-excerpt">{teaser_body}</div>
                                    </div>
                                    <span class="archive-cta">Read &rarr;</span>
                                </a>"""
                                
    insert_pos = mia_html.find('<div id="archiveList"')
    if insert_pos != -1:
        insert_pos = mia_html.find('>', insert_pos) + 1
        mia_html = mia_html[:insert_pos] + "\n" + new_archive_row + mia_html[insert_pos:]
        
    with open('market-intelligence-archive.html', 'w', encoding='utf-8') as f:
        f.write(mia_html)
        
    print("Update successful")

if __name__ == '__main__':
    update_18_aug()
