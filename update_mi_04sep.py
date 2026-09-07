import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Hero Date
c = re.sub(
    r'(<div class="hero-meta">.*?<span class="meta-date">)[^<]*(</span>)',
    r'\g<1>04 Sep 2026\g<2>',
    c, flags=re.DOTALL
)

# 2. Snapshot subtitle
c = re.sub(
    r'(<div class="snapshot-subtitle">End-of-day summary for )[^<]*(</div>)',
    r'\g<1>4th September 2026\g<2>',
    c
)

# 3. Snapshot metrics
c = re.sub(r'(<div class="metric-value"[^>]*id="home-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="metric-value"[^>]*id="home-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="metric-value"[^>]*id="home-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

# 4. Gainers
idx_gainers = c.find('<!-- GAINERS_START -->')
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

# 5. Losers
idx_losers = c.find('<!-- LOSERS_START -->')
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

# 6. Archive Featured Spotlight
idx_spotlight = c.find('<!-- SPOTLIGHT_START -->')
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

print("Updated market-intelligence.html")
