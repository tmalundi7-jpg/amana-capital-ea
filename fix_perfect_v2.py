import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- INDEX.HTML ---
with open('test_index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Dates
c = c.replace('End-of-day summary for 3rd September 2026', 'End-of-day summary for 4th September 2026')
c = c.replace('Terminal Feed | End-of-day &middot; 3 September 2026', 'Terminal Feed | End-of-day &middot; 4 September 2026')

# 2. Snapshot metrics
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="home-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

# 3. Gainers
gainers_repl = '''<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>KCB <span style="color:var(--gain)">+3.7%</span></span>
            <span>NMB <span style="color:var(--gain)">+3.6%</span></span>
            <span>MCB <span style="color:var(--gain)">+2.6%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-gainers"[^>]*>.*?</div>', gainers_repl, c, flags=re.DOTALL)

# 4. Losers
losers_repl = '''<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span>VODA <span style="color:var(--loss)">-1.9%</span></span>
            <span>DSE <span style="color:var(--loss)">-1.4%</span></span>
            <span>TOL <span style="color:var(--loss)">-0.5%</span></span>
          </div>'''
c = re.sub(r'<div class="snapshot-mover" id="home-losers"[^>]*>.*?</div>', losers_repl, c, flags=re.DOTALL)

# 5. Teaser
c = c.replace('Thursday, 3rd September 2026', 'Friday, 4th September 2026')
c = c.replace('The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day figure in months. The driver was a single block trade in CRDB involving 11.2 million shares worth approximately TZS 30 billion, the largest such transaction in recent memory. Foreign investors sold nearly a third of the day\'s turnover, yet CRDB closed higher.', 'The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730.')
c = c.replace('4,442.62</div>', '4,523.81</div>')
c = c.replace('TZS 42.93 bn</div>', 'TZS 8.18 bn</div>')
c = c.replace('/dse-wrap-2026-09-03', '/dse-wrap-2026-09-04')
c = c.replace('<span>MBP</span>', '<span>KCB</span>')
c = c.replace('>+8.2%</span>', '>+3.7%</span>')
c = c.replace('<span>TICL</span>', '<span>VODA</span>')
c = c.replace('>-2.9%</span>', '>-1.9%</span>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)


# --- MARKET INTELLIGENCE ---
with open('test_mi.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Hero Date
c = c.replace('<strong>03 Sep 2026</strong>', '<strong>04 Sep 2026</strong>')

# Metrics
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-dsei"[^>]*>)[^<]*(</div>)', r'\g<1>4,523.81\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-tsi"[^>]*>)[^<]*(</div>)', r'\g<1>9,826.80\g<2>', c)
c = re.sub(r'(<div class="snapshot-value"[^>]*id="mi-turnover"[^>]*>)[^<]*(</div>)', r'\g<1>TZS 8.18 bn\g<2>', c)

# Gainers
gainers_repl_mi = '''<!-- GAINERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>KCB</span> <span style="color:var(--gain)">+3.7%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>NMB</span> <span style="color:var(--gain)">+3.6%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>MCB</span> <span style="color:var(--gain)">+2.6%</span></div>
      </div>
      <!-- GAINERS_END -->'''
c = re.sub(r'<!-- GAINERS_START -->.*?<!-- GAINERS_END -->', gainers_repl_mi, c, flags=re.DOTALL)

# Losers
losers_repl_mi = '''<!-- LOSERS_START -->
      <div style="display:flex; flex-direction:column; gap:0.15rem; width:100%;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>VODA</span> <span style="color:var(--loss)">-1.9%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>DSE</span> <span style="color:var(--loss)">-1.4%</span></div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700; color:var(--cream);"><span>TOL</span> <span style="color:var(--loss)">-0.5%</span></div>
      </div>
      <!-- LOSERS_END -->'''
c = re.sub(r'<!-- LOSERS_START -->.*?<!-- LOSERS_END -->', losers_repl_mi, c, flags=re.DOTALL)

# Spotlight
c = c.replace('/dse-wrap-2026-09-03', '/dse-wrap-2026-09-04')
c = c.replace('Thursday, 3rd September 2026', 'Friday, 4th September 2026')
c = c.replace('The Dar es Salaam Stock Exchange delivered its most dramatic session of the quarter on Thursday, with equity turnover exploding to TZS 42.93 billion — the highest single-day figure in months...', 'The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730...')

with open('market-intelligence.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated perfectly from test_*.html to target files")
