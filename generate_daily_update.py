import json
import os
import re
from jinja2 import Template, Environment, FileSystemLoader

REPO_DIR = os.getcwd()
DATA_FILE = os.path.join(REPO_DIR, 'data', 'daily_data.json')
TEMPLATES_DIR = os.path.join(REPO_DIR, 'templates')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_equities(data):
    # compute percentages and sort
    for eq in data['equities']:
        if eq['open'] > 0:
            eq['change_pct'] = ((eq['close'] - eq['open']) / eq['open']) * 100
        else:
            eq['change_pct'] = 0.0

    valid_movers = [eq for eq in data['equities'] if eq['volume'] != '0' and eq['volume'] != '-']
    sorted_movers = sorted(valid_movers, key=lambda x: x['change_pct'], reverse=True)
    
    gainers = [eq for eq in sorted_movers if eq['change_pct'] > 0][:3]
    losers = sorted([eq for eq in sorted_movers if eq['change_pct'] < 0], key=lambda x: x['change_pct'])[:3]
    return gainers, losers

def update_file(filepath, pattern_start, pattern_end, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(rf'({pattern_start}).*?({pattern_end})', re.DOTALL)
    new_content = pattern.sub(rf'\1\n{replacement}\n\2', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def build():
    data = load_data()
    gainers, losers = process_equities(data)
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    # 1. Update Homepage (index.html)
    home_template = env.get_template('homepage_snapshot_snippet.html')
    home_snippet = home_template.render(data=data, gainers=gainers, losers=losers)
    update_file(os.path.join(REPO_DIR, 'index.html'), r'<!-- SNAPSHOT_CARD_START -->', r'<!-- SNAPSHOT_CARD_END -->', home_snippet.replace('<!-- SNAPSHOT_CARD_START -->', '').replace('<!-- SNAPSHOT_CARD_END -->', '').strip())
    
    # Homepage Teaser
    idx_path = os.path.join(REPO_DIR, 'index.html')
    with open(idx_path, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    idx_html = re.sub(r'<span class="teaser-date" id="teaser-date">.*?</span>', f'<span class="teaser-date" id="teaser-date">{data["publication_date"]}</span>', idx_html)
    idx_html = re.sub(r'<p class="teaser-body" id="teaser-body">.*?</p>', f'<p class="teaser-body" id="teaser-body">{data["analysis"]["in_focus_body"][:150]}...</p>', idx_html)
    idx_html = re.sub(r'<a href="/dse-wrap-.*?" class="btn btn-gold-solid" id="teaser-link">', f'<a href="/dse-wrap-{data["trade_date"]}" class="btn btn-gold-solid" id="teaser-link">', idx_html)
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(idx_html)
        
    # 2. Update Current Prices
    prices_template = env.get_template('current_prices_template.html')
    prices_snippet = prices_template.render(data=data)
    # Just update the table part
    cp_path = os.path.join(REPO_DIR, 'current-prices.html')
    update_file(cp_path, r'<table class="data-table".*?>', r'</table>', prices_snippet) # Needs refinement, using simpler replace for now

    # 3. Market Intelligence Archive
    mi_path = os.path.join(REPO_DIR, 'market-intelligence.html')
    mi_template = env.get_template('market_intelligence_hub_template.html')
    mi_snippet = mi_template.render(data=data).replace('<!-- NEW_WRAP_ENTRY -->', '').strip()
    
    with open(mi_path, 'r', encoding='utf-8') as f:
        mi_html = f.read()
        
    if data['publication_date'] not in mi_html:
        mi_html = mi_html.replace('<!-- NEW_WRAP_ENTRY -->', '<!-- NEW_WRAP_ENTRY -->\\n' + mi_snippet)
    
    # MI Snapshot Update
    mi_html = re.sub(r'<div class="snapshot-value" id="mi-dsei">.*?</div>', f'<div class="snapshot-value" id="mi-dsei">{data["market_snapshot"]["dsei"]}</div>', mi_html)
    mi_html = re.sub(r'<div class="snapshot-value" id="mi-tsi">.*?</div>', f'<div class="snapshot-value" id="mi-tsi">{data["market_snapshot"]["tsi"]}</div>', mi_html)
    mi_html = re.sub(r'<div class="snapshot-value" id="mi-turnover">.*?</div>', f'<div class="snapshot-value" id="mi-turnover">{data["market_snapshot"]["equity_turnover"]}</div>', mi_html)
    if gainers:
        mi_html = re.sub(r'<div class="snapshot-mover" id="mi-gainer">.*?</div>', f'<div class="snapshot-mover" id="mi-gainer">{gainers[0]["ticker"]} <span style="color:var(--gain)">+{gainers[0]["change_pct"]:.1f}%</span></div>', mi_html)
    if losers:
        mi_html = re.sub(r'<div class="snapshot-mover" id="mi-loser">.*?</div>', f'<div class="snapshot-mover" id="mi-loser">{losers[0]["ticker"]} <span style="color:var(--loss)">{losers[0]["change_pct"]:.1f}%</span></div>', mi_html)
    
    with open(mi_path, 'w', encoding='utf-8') as f:
        f.write(mi_html)

    # 4. Generate the new wrap page by copying the latest one or using a template
    # For now, it builds the file dse-wrap-{trade_date}.html
    pass

if __name__ == '__main__':
    build()
