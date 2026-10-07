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
    for eq in data.get('stocks') or data.get('equities') or []:
        if eq['open'] > 0:
            eq['change_pct'] = ((eq['close'] - eq['open']) / eq['open']) * 100
        else:
            eq['change_pct'] = 0.0

    equities = data.get('stocks') or data.get('equities') or []
    valid_movers = [eq for eq in equities if str(eq.get('volume')) not in ('0', '-', '')]
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
    idx_html = re.sub(r'<span class="teaser-date" id="teaser-date">.*?</span>', f'<span class="teaser-date" id="teaser-date">{data.get("display_date", "")}</span>', idx_html)
    idx_html = re.sub(r'<p class="teaser-body" id="teaser-body">.*?</p>', f'<p class="teaser-body" id="teaser-body">{(data.get("in_focus") or {}).get("text", "")[:150]}...</p>', idx_html)
    idx_html = re.sub(r'<a href="/dse-wrap-.*?" class="mk-btn mk-btn-gold" id="teaser-link">', f'<a href="/dse-wrap-{data.get("date", "")}" class="mk-btn mk-btn-gold" id="teaser-link">', idx_html)
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(idx_html)
        
    # 2. Update Current Prices (terminal table)
    # Company/sector names live in data/ticker_map.json (scraped once from the
    # published table; the daily feed carries ticker/open/close/volume only).
    try:
        with open(os.path.join(REPO_DIR, 'data', 'ticker_map.json'), encoding='utf-8') as fh:
            ticker_map = json.load(fh)
    except OSError:
        ticker_map = {}
    def _compact(n):
        try: n = float(n)
        except (TypeError, ValueError): return '-'
        if n >= 1e9: return f'{n/1e9:.2f}bn'
        if n >= 1e6: return f'{n/1e6:.2f}m'
        if n >= 1e3: return f'{n/1e3:.1f}k'
        return f'{int(n):,}'
    enriched = []
    for eq in (data.get('stocks') or data.get('equities') or []):
        chg = eq.get('change_pct')
        if chg is None and eq.get('open'):
            chg = ((eq['close'] - eq['open']) / eq['open'] * 100) if eq['open'] else 0.0
        vol = eq.get('volume') or 0
        try: turnover = float(str(vol).replace(',', '')) * float(eq.get('close') or 0)
        except (TypeError, ValueError): turnover = 0
        co, _sec = ticker_map.get(eq.get('ticker', ''), ('', ''))
        enriched.append({'ticker': eq.get('ticker', ''), 'company': co,
                         'close': eq.get('close', 0), 'change_pct': chg or 0.0,
                         'volume': vol, 'turnover_compact': _compact(turnover)})
    prices_template = env.get_template('current_prices_template.html')
    prices_snippet = prices_template.render(data=data, equities=enriched)
    cp_path = os.path.join(REPO_DIR, 'current-prices.html')
    update_file(cp_path, r'<!-- PRICES_TABLE_START -->', r'<!-- PRICES_TABLE_END -->',
                prices_snippet.replace('<!-- PRICES_TABLE_START -->', '').replace('<!-- PRICES_TABLE_END -->', '').strip())

    # 3. Market Intelligence Archive
    mi_path = os.path.join(REPO_DIR, 'market-intelligence.html')
    mi_template = env.get_template('market_intelligence_hub_template.html')
    mi_snippet = mi_template.render(data=data).replace('<!-- NEW_WRAP_ENTRY -->', '').strip()
    
    with open(mi_path, 'r', encoding='utf-8') as f:
        mi_html = f.read()
        
    if data.get('display_date', '') and data.get('display_date', '') not in mi_html:
        mi_html = mi_html.replace('<!-- NEW_WRAP_ENTRY -->', '<!-- NEW_WRAP_ENTRY -->\\n' + mi_snippet)
    
    # MI Snapshot Update
    mi_html = re.sub(r'<div class="snapshot-value[^"]*" id="mi-dsei">.*?</div>', f'<div class="snapshot-value" id="mi-dsei">{data.get("dsei", data.get("market_snapshot", {}).get("dsei", ""))}</div>', mi_html)
    mi_html = re.sub(r'<div class="snapshot-value[^"]*" id="mi-tsi">.*?</div>', f'<div class="snapshot-value" id="mi-tsi">{data.get("tsi", data.get("market_snapshot", {}).get("tsi", ""))}</div>', mi_html)
    mi_html = re.sub(r'<div class="snapshot-value[^"]*" id="mi-turnover">.*?</div>', f'<div class="snapshot-value" id="mi-turnover">{data.get("equity_turnover_bn", data.get("market_snapshot", {}).get("equity_turnover", ""))}</div>', mi_html)
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
