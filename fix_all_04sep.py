import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Dates
c = re.sub(
    r'(<div class="snapshot-subtitle">End-of-day summary for )[^<]*(</div>)',
    r'\g<1>4th September 2026\g<2>',
    c
)
c = re.sub(
    r'(<div class="terminal-title">DSE TERMINAL FEED // )[^<]*(</div>)',
    r'\g<1>04 SEP 2026\g<2>',
    c
)

# 2. Snapshot Metrics
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

# 3. Gainers
idx_gainers = c.find('<div class="list-title">Top Gainers</div>')
if idx_gainers != -1:
    gainers_block = c[idx_gainers:idx_gainers+1500]
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>',
        gainers_block, count=1, flags=re.DOTALL
    )
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>NMB\g<4>+3.6%\g<5>',
        gainers_block, count=1, flags=re.DOTALL
    )
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>NMB\g<4>+3.6%\g<5>MCB\g<6>+2.6%\g<7>',
        gainers_block, count=1, flags=re.DOTALL
    )
    c = c[:idx_gainers] + gainers_block + c[idx_gainers+1500:]

# 4. Losers
idx_losers = c.find('<div class="list-title">Top Losers</div>')
if idx_losers != -1:
    losers_block = c[idx_losers:idx_losers+1500]
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>',
        losers_block, count=1, flags=re.DOTALL
    )
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>DSE\g<4>-1.4%\g<5>',
        losers_block, count=1, flags=re.DOTALL
    )
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>DSE\g<4>-1.4%\g<5>TOL\g<6>-0.5%\g<7>',
        losers_block, count=1, flags=re.DOTALL
    )
    c = c[:idx_losers] + losers_block + c[idx_losers+1500:]

# 5. Teaser
idx_teaser = c.find('TEASER_CARD_START')
if idx_teaser != -1:
    teaser_block = c[idx_teaser:idx_teaser+3000]

    teaser_block = re.sub(
        r'(<div class="teaser-prem-date">)[^<]*(</div>)',
        r'\g<1>Friday, 4th September 2026\g<2>',
        teaser_block
    )
    teaser_block = re.sub(
        r'(<h3 class="teaser-prem-title">)[^<]*(</h3>)',
        r'\g<1>Daily DSE Wrap | Friday, 4th September 2026\g<2>',
        teaser_block
    )
    teaser_block = re.sub(
        r'(<p class="teaser-prem-body">)[^<]*(</p>)',
        r'\g<1>The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730.\g<2>',
        teaser_block
    )

    teaser_block = re.sub(
        r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
        r'\g<1>4,523.81\g<2>',
        teaser_block
    )
    teaser_block = re.sub(
        r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">)[^<]*(</div>)',
        r'\g<1>TZS 8.18 bn\g<2>',
        teaser_block
    )
    teaser_block = re.sub(
        r'(<div class="teaser-prem-stat-label">Top Gainer</div>.*?<span>)[^<]*(</span>.*?<span[^>]*>)[^<]*(</span>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>',
        teaser_block, flags=re.DOTALL
    )
    teaser_block = re.sub(
        r'(<div class="teaser-prem-stat-label">Top Loser</div>.*?<span>)[^<]*(</span>.*?<span[^>]*>)[^<]*(</span>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>',
        teaser_block, flags=re.DOTALL
    )

    teaser_block = re.sub(
        r'(<a href=")/dse-wrap-[0-9\-]+(" class="teaser-prem-btn">)',
        r'\g<1>/dse-wrap-2026-09-04\g<2>',
        teaser_block
    )

    c = c[:idx_teaser] + teaser_block + c[idx_teaser+3000:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)


# --- MARKET INTELLIGENCE HTML ---
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(
    r'(<div class="hero-meta">.*?<span class="meta-date">)[^<]*(</span>)',
    r'\g<1>04 Sep 2026\g<2>',
    c, flags=re.DOTALL
)

c = re.sub(
    r'(<div class="snapshot-subtitle">End-of-day summary for )[^<]*(</div>)',
    r'\g<1>4th September 2026\g<2>',
    c
)
c = re.sub(
    r'(<div class="terminal-title">DSE TERMINAL FEED // )[^<]*(</div>)',
    r'\g<1>04 SEP 2026\g<2>',
    c
)

c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

idx_gainers = c.find('<!-- GAINERS_START -->')
if idx_gainers != -1:
    gainers_block = c[idx_gainers:idx_gainers+1500]
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>',
        gainers_block, count=1, flags=re.DOTALL
    )
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>NMB\g<4>+3.6%\g<5>',
        gainers_block, count=1, flags=re.DOTALL
    )
    gainers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-gain">)[^<]*(</span>.*?</div>)',
        r'\g<1>KCB\g<2>+3.7%\g<3>NMB\g<4>+3.6%\g<5>MCB\g<6>+2.6%\g<7>',
        gainers_block, count=1, flags=re.DOTALL
    )
    c = c[:idx_gainers] + gainers_block + c[idx_gainers+1500:]

idx_losers = c.find('<!-- LOSERS_START -->')
if idx_losers != -1:
    losers_block = c[idx_losers:idx_losers+1500]
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>',
        losers_block, count=1, flags=re.DOTALL
    )
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>DSE\g<4>-1.4%\g<5>',
        losers_block, count=1, flags=re.DOTALL
    )
    losers_block = re.sub(
        r'(<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>.*?<div class="list-item">.*?<span>)[^<]*(</span>.*?<span class="change-loss">)[^<]*(</span>.*?</div>)',
        r'\g<1>VODA\g<2>-1.9%\g<3>DSE\g<4>-1.4%\g<5>TOL\g<6>-0.5%\g<7>',
        losers_block, count=1, flags=re.DOTALL
    )
    c = c[:idx_losers] + losers_block + c[idx_losers+1500:]

idx_spotlight = c.find('<!-- SPOTLIGHT_START -->')
if idx_spotlight != -1:
    spotlight_block = c[idx_spotlight:idx_spotlight+2500]

    spotlight_block = re.sub(
        r'(<a href=")/dse-wrap-[0-9\-]+(" class="spotlight-card">)',
        r'\g<1>/dse-wrap-2026-09-04\g<2>',
        spotlight_block
    )
    spotlight_block = re.sub(
        r'(<div class="spotlight-date">)[^<]*(</div>)',
        r'\g<1>Friday, 4th September 2026\g<2>',
        spotlight_block
    )
    spotlight_block = re.sub(
        r'(<div class="spotlight-title">)[^<]*(</div>)',
        r'\g<1>Daily DSE Wrap | Friday, 4th September 2026\g<2>',
        spotlight_block
    )
    spotlight_block = re.sub(
        r'(<div class="spotlight-excerpt">)[^<]*(</div>)',
        r'\g<1>The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730...\g<2>',
        spotlight_block
    )

    c = c[:idx_spotlight] + spotlight_block + c[idx_spotlight+2500:]

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated both index.html and market-intelligence.html")
