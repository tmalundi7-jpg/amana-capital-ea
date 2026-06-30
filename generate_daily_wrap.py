import json
import os
import re
from jinja2 import Environment, FileSystemLoader

def main():
    # Load daily data
    with open('data/daily_data.json', 'r') as f:
        data = json.load(f)

    # Process stocks for top gainers & losers
    gainers = []
    losers = []
    for s in data['stocks']:
        if s['open'] > 0:
            change = ((s['close'] - s['open']) / s['open']) * 100
            s['change_pct'] = change
            if change > 0:
                gainers.append(s)
            elif change < 0:
                losers.append(s)
    
    # Sort and pick top 3
    data['gainers'] = sorted(gainers, key=lambda x: x['change_pct'], reverse=True)[:3]
    data['losers'] = sorted(losers, key=lambda x: x['change_pct'])[:3]

    # 1. Render new wrap HTML page
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('daily_wrap_template.html')
    output_html = template.render(data)
    
    new_filename = f"dse-wrap-{data['date']}.html"
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(output_html)

    # 2. Inject into Market Intelligence Hub
    wrap_card = f"""
            <div class="card" style="margin-bottom: 2rem;">
                <span style="font-size: 0.85rem; color: var(--navy-lighter); text-transform: uppercase; font-weight: 600;">{data['display_date']}</span>
                <h3>{data['in_focus']['title']}</h3>
                <p>{data['in_focus']['text']}</p>
                <a href="{new_filename}">Read Full Wrap &rarr;</a>
            </div>"""
    
    with open('market-intelligence.html', 'r', encoding='utf-8') as f:
        mi_content = f.read()
    
    # Insert new card exactly after the HTML marker
    mi_content = mi_content.replace('<!-- WRAP_LIST_START -->', f'<!-- WRAP_LIST_START -->\n{wrap_card}')
    with open('market-intelligence.html', 'w', encoding='utf-8') as f:
        f.write(mi_content)

    # 3. Inject into Homepage Snapshot
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()
    
    # Update date string
    idx_content = re.sub(r'<!-- SNAPSHOT_DATE -->.*?<!-- SNAPSHOT_DATE_END -->', 
                         f'<!-- SNAPSHOT_DATE -->{data["display_date"]}<!-- SNAPSHOT_DATE_END -->', 
                         idx_content, flags=re.DOTALL)
    
    # Update index values
    stats_html = f"""
                    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:2rem; padding: 1.5rem 0;">
                        <div style="font-size:1.1rem;"><strong style="color:var(--navy-lighter)">DSEI:</strong> {data['dsei']:,.2f}</div>
                        <div style="font-size:1.1rem;"><strong style="color:var(--navy-lighter)">TSI:</strong> {data['tsi']:,.2f}</div>
                    </div>"""
    idx_content = re.sub(r'<!-- SNAPSHOT_DATA_START -->.*?<!-- SNAPSHOT_DATA_END -->', 
                         f'<!-- SNAPSHOT_DATA_START -->{stats_html}\n                    <!-- SNAPSHOT_DATA_END -->', 
                         idx_content, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_content)

if __name__ == "__main__":
    main()
