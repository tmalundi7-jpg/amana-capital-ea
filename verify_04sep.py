import sys, io, re
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check(name, expected, text, exact=False):
    if exact:
        if expected == text:
            print(f"  [PASS] {name} == {expected}")
        else:
            print(f"  [FAIL] {name} expected '{expected}', got '{text}'")
    else:
        if expected in text:
            print(f"  [PASS] {name} contains '{expected}'")
        else:
            print(f"  [FAIL] {name} missing '{expected}'. Content snippet: {text[:100]}")

print("============ index.html ============")
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Dates
check("Snapshot subtitle date", "4th September 2026", c)
check("Terminal feed date", "04 September 2026", c)

# 2. Metrics
soup = BeautifulSoup(c, 'html.parser')
dsei = soup.find(id='home-dsei').text.strip()
tsi = soup.find(id='home-tsi').text.strip()
turnover = soup.find(id='home-turnover').text.strip()
check("DSEI", "4,523.81", dsei, True)
check("TSI", "9,826.80", tsi, True)
check("Turnover", "TZS 8.18 bn", turnover, True)

# 3. Gainers / Losers
# Let's find the gainers list
gainers_section = c[c.find('<div class="list-title">Top Gainers</div>'):c.find('<div class="list-title">Top Losers</div>')]
check("Gainer 1 Ticker", "KCB", gainers_section)
check("Gainer 1 Change", "+3.7%", gainers_section)
check("Gainer 2 Ticker", "NMB", gainers_section)
check("Gainer 2 Change", "+3.6%", gainers_section)
check("Gainer 3 Ticker", "MCB", gainers_section)
check("Gainer 3 Change", "+2.6%", gainers_section)

losers_section = c[c.find('<div class="list-title">Top Losers</div>'):c.find('TEASER_CARD_START')]
check("Loser 1 Ticker", "VODA", losers_section)
check("Loser 1 Change", "-1.9%", losers_section)
check("Loser 2 Ticker", "DSE", losers_section)
check("Loser 2 Change", "-1.4%", losers_section)
check("Loser 3 Ticker", "TOL", losers_section)
check("Loser 3 Change", "-0.5%", losers_section)

# 4. Teaser
teaser_section = c[c.find('TEASER_CARD_START'):c.find('<!-- END TEASER -->')] if '<!-- END TEASER -->' in c else c[c.find('TEASER_CARD_START'):c.find('TEASER_CARD_START')+3000]
check("Teaser Date", "Friday, 4th September 2026", teaser_section)
check("Teaser Headline", "Daily DSE Wrap | Friday, 4th September 2026", teaser_section)
check("Teaser Intro", "The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730.", teaser_section)
check("Teaser URL", "/dse-wrap-2026-09-04", teaser_section)


print("\n============ market-intelligence.html ============")
with open('market-intelligence.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Dates
check("Hero meta date", "04 Sep 2026", c)
check("Snapshot subtitle date", "4th September 2026", c)

# 2. Metrics
soup = BeautifulSoup(c, 'html.parser')
dsei = soup.find(id='home-dsei').text.strip()
tsi = soup.find(id='home-tsi').text.strip()
turnover = soup.find(id='home-turnover').text.strip()
check("DSEI", "4,523.81", dsei, True)
check("TSI", "9,826.80", tsi, True)
check("Turnover", "TZS 8.18 bn", turnover, True)

# 3. Gainers / Losers
gainers_section = c[c.find('<!-- GAINERS_START -->'):c.find('<!-- LOSERS_START -->')]
check("MI Gainer 1", "KCB", gainers_section)
check("MI Gainer 1 Change", "+3.7%", gainers_section)
check("MI Gainer 2", "NMB", gainers_section)
check("MI Gainer 3", "MCB", gainers_section)

losers_section = c[c.find('<!-- LOSERS_START -->'):c.find('<!-- MARKET SNAPSHOT END -->')]
check("MI Loser 1", "VODA", losers_section)
check("MI Loser 1 Change", "-1.9%", losers_section)
check("MI Loser 2", "DSE", losers_section)
check("MI Loser 3", "TOL", losers_section)

# 4. Spotlight
spotlight_section = c[c.find('<!-- SPOTLIGHT_START -->'):c.find('<!-- SPOTLIGHT_END -->')] if '<!-- SPOTLIGHT_END -->' in c else c[c.find('<!-- SPOTLIGHT_START -->'):c.find('<!-- SPOTLIGHT_START -->')+3000]
check("Spotlight URL", "/dse-wrap-2026-09-04", spotlight_section)
check("Spotlight Date", "Friday, 4th September 2026", spotlight_section)
check("Spotlight Title", "Daily DSE Wrap | Friday, 4th September 2026", spotlight_section)
check("Spotlight Excerpt", "The Dar es Salaam Stock Exchange closed the week with a session that confirmed a fundamental shift in market dynamics. Equity turnover moderated to a still-impressive TZS 8.18 billion, with CRDB leading the charge to a new post-split high of 2,730...", spotlight_section)

