import requests
import json
import os
import datetime
from google import genai

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
MODEL_NAME = "gemini-3.6-flash"
OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ---------------------------------------------------------
# Step 1: Scrape/Extract Data
# ---------------------------------------------------------
from scrape_dse import get_dse_market_data

def fetch_dse_data():
    """
    Fetches the daily market report data from the DSE website.
    """
    print("Fetching DSE Data...")
    return get_dse_market_data()


# ---------------------------------------------------------
# Step 2: Gemini API Analysis Pipeline
# ---------------------------------------------------------
def run_analysis_pipeline(market_data):
    if not market_data or not market_data.get('text'):
        print("No market data text available for analysis.")
        return

    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("\nERROR: GEMINI_API_KEY environment variable not found!")
        print("Please set your API key in your terminal before running this script.")
        print("Example: $env:GEMINI_API_KEY='your_api_key_here'")
        print("You can get a free API key at: https://aistudio.google.com/app/apikey")
        return

    print(f"Sending data to Gemini API for analysis (Date: {market_data['date']})...")
    client = genai.Client()
    
    # ---------------------------------------------------------
    # CALL 1: INTERNAL ANALYSIS (Personal Use)
    # ---------------------------------------------------------
    print("Generating Internal Analysis (Step 1)...")
    internal_prompt = f"""You are Theophil Christian Malundi, Investment Analyst at Amana Capital East Africa, with over 40 years of institutional experience in equity trading, hedge fund management, and banking across global and frontier markets.

Your task is to perform a deep, actionable analysis of today’s Dar es Salaam Stock Exchange (DSE) market report, integrating it with the following proprietary strategies and the current portfolio holdings provided. Please calculate and include the 5% daily price caps for tomorrow based on today's closing prices.

### PORTFOLIO & STRATEGY CONTEXT (immutable)

**Current Holdings:**
- Cash: TZS 835,002 (fully liquid; no open equity positions).
- Completed cycles: CRDB bought @ 2,720, sold @ 2,850 (+TZS 130/sh). VODA bought @ 760, sold @ 780 (+TZS 20/sh). Both profitable.
- Planned re-entries (not yet placed):
  - CRDB: BUY 200 @ 2,770 GTC -> SELL 200 @ 2,840 GTC (70-TZS spread).
  - VODA: BUY 100 @ 750 GTC -> SELL 100 @ 780 GTC (30-TZS spread).
  - DCB: BUY 100 @ 550 GTC -> SELL 100 @ 590 GTC (40-TZS spread).
  - NMB: BUY 5 @ 14,700 GTC -> SELL 5 @ 15,300 GTC (pre-AGM toehold; expanded price band post-10 June).
- Approximate total deployment: TZS 757,500; residual buffer: ~TZS 77,500.

**Active Strategies & “Profitable Unknown Ways”:**
1. **Shadow Market Making (Spread Capture):** Rotate settled shares of CRDB, VODA, and DCB using limit orders only. Target TZS 60–80 spread on CRDB, TZS 20–40 on VODA, TZS 30–50 on DCB. Respect the 5% inventory rule. After selling, immediately reload with a limit buy. Never use market orders. Only initiate a cycle if the spread covers round-trip fees (~2.0-2.4%) and leaves a net profit.
2. **Block Trade Discount & Slow Bleed:** Monitor for block trades >=TZS 250M; negotiate 5-8% discount; bleed back over 10-15 sessions. (Aspirational until portfolio >TZS 5M.)
3. **Dividend Accumulation & Volume Spikes:** Accumulate high-dividend counters 4-6 weeks before ex-dividend dates. Sell half into the pre-ex-div volume spike; hold half for the 5%-WHT dividend.
4. **Bond-to-Equity Rotation Front-Running:** Use daily bond turnover as a lead indicator. When bond turnover spikes then contracts, front-run rotation into high-yield equities (CRDB, NMB, TPCC).
5. **Government Bond Liquidity Bridge:** Park idle cash in 5-25 year tax-exempt bonds (0% WHT) or UTT AMIS Liquid/Bond Fund.
6. **ETF Discount/Premium Arbitrage:** Buy iTrust/Vertex ETF only if discount >3% to NAV; sell if premium >3%.
7. **Corporate Action Price Cap Exploitation:** Exploit extra 5% daily price band during the 5-day window following dividend/rights-issue announcements.
8. **Cross-Border (NSE-DSE) Dislocation:** Monitor KCB, EABL, JHL for >=5% price divergences.
9. **Rights Issue Discount Arbitrage:** Participate in deeply discounted rights issues.
10. **Tax Optimisation:** 0% CGT, 5% WHT on listed dividends, 0% WHT on government bond interest (>=3yr).

**Key Upcoming Catalysts:**
- **10 June 2026 (WEDNESDAY):** NMB AGM to approve TZS 610.15 combined dividend. This is the most time-sensitive event. Ex-dividend date will be set shortly after; expanded 10% price cap applies for 5 working days post-AGM.
- **July/August 2026:** VODA expected FY2025 dividend announcement.
- **Ongoing:** CRDB post-dividend reinvestment flow; foreign selling absorption (29-30% of daily turnover). The 52,668-share bid wall at 2,800 has been disappearing from the order book — support may be softening, which favours a 2,770 entry.

### REQUIRED ANALYSIS SECTIONS
Provide a comprehensive report with the following sections, using a direct, institutional tone. No fluff. Every statement must be backed by the data provided.

1. MARKET PULSE & MACRO NARRATIVE
2. PORTFOLIO HOLDINGS DEEP DIVE (WITH 5% DAILY CAPS)
3. SHADOW MARKET-MAKING OPPORTUNITIES BEYOND CURRENT HOLDINGS
4. DIVIDEND & CORPORATE ACTION CALENDAR UPDATE
5. FIXED INCOME & BOND BRIDGE
6. CROSS-BORDER ARBITRAGE SNAPSHOT
7. RISK MANAGEMENT CHECK
8. FORWARD ACTION PLAN – TOMORROW’S TRADE SHEET (WITH 5% CAP)
9. STRATEGIC INSIGHT

### TODAY’S DSE MARKET REPORT
{market_data['text'][:25000]}
"""
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=internal_prompt
        )
        internal_analysis = interaction.output_text
    except Exception as e:
        print(f"Failed to generate internal analysis: {e}")
        return

    if not internal_analysis:
        print("Failed to generate internal analysis (empty response).")
        return

    # ---------------------------------------------------------
    # CALL 2: PUBLIC WRAP & CURRENT PRICES (Step 2)
    # ---------------------------------------------------------
    print("Generating Public Wrap & Current Prices (Step 2)...")
    public_prompt = f"""As a veteran in investing, analyse the following data below which includes my own analysis but do not include my strategies that I use. The purpose of analysing this set of data is to add to my website hence I do not want to disclose my strategies. The analysis will aim to provide education to the audience on how to tackle the market. You are Theophil Christian Malundi, Investment Analyst at Amana Capital East Africa, with over 40 years of institutional experience.

**CRITICAL REQUIREMENT - STRICT FORMATTING:**
You must strictly follow this exact format for the article. Do not add introductory fluff before the title.
Title format: `Daily DSE Wrap | {market_data['date']}`
Followed immediately by a thematic headline (e.g., "Massive CRDB Block Trade Absorbed as Local Investors Anchor a Quiet Start").
Followed by a brief introductory paragraph summarizing the day's main story.

Then, you must include exactly these three sections:
1. **Market Snapshot**: A table comparing today's metrics (DSEI, TSI, Equity Turnover, Shares Traded, Deals, Foreign Buying/Selling) to the previous session, followed by a brief text analysis.
2. **Top Movers**: A table with Ticker, Closing Price (TZS), Change, and Volume. Below the table, list the Gainers and Losers, followed by a brief analysis of the price actions.
3. **In Focus: [Theme of the day]**: A deep dive into the most significant event or trend of the day.

**CRITICAL REQUIREMENT - INTERACTIVE EDUCATION LINKS:**
Throughout the article, you must maintain interactive highlighted materials. Whenever you use a financial term or concept (e.g., "block trade", "All-Share Index", "yield", "VWAP", "dividend"), format it as a markdown link pointing to our investor education page. Example: `[block trade](/investor-education)`. This is to allow readers to access learning materials easily.

**CRITICAL REQUIREMENT - TONE AND SECRECY:**
Use an English tone that will be understood by everyone and maintain a professional, human tone. 
UNDER NO CIRCUMSTANCES should you disclose any of my proprietary trading strategies (e.g. shadow market making, spread capture targets, specific limit order plans) in this public wrap.

**CRITICAL REQUIREMENT - JSON METADATA:**
At the very end of your response, after the 'In Focus' section, you MUST output a JSON block wrapped in ```json ... ``` tags containing exactly these fields:
- "headline": The thematic headline you used.
- "intro": A short 1-2 sentence excerpt of the introductory paragraph.
- "dsei": The current DSEI value (e.g. "4,228.71").
- "turnover": The current Equity Turnover formatted exactly like "TZS 4.81bn" or "TZS 900m".
- "top_gainer": The ticker and percentage change of the top gainer, exactly like "SWIS +10.7%".

This JSON is required for website automation.

### MY INTERNAL ANALYSIS
{internal_analysis}

### TODAY’S DSE MARKET REPORT
{market_data['text'][:25000]}
"""
    try:
        interaction2 = client.interactions.create(
            model=MODEL_NAME,
            input=public_prompt
        )
        public_wrap = interaction2.output_text
    except Exception as e:
        print(f"Failed to generate public wrap: {e}")
        return

    import re
    # Extract JSON metadata
    metadata = None
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', public_wrap, re.DOTALL)
    if json_match:
        try:
            metadata = json.loads(json_match.group(1))
            public_wrap = public_wrap.replace(json_match.group(0), "").strip()
        except Exception as e:
            print(f"Warning: Failed to parse JSON metadata: {e}")

    # ---------------------------------------------------------
    # SAVE OUTPUTS
    # ---------------------------------------------------------
    safe_date = market_data['date'].replace(' ', '_').replace(',', '')
    
    internal_filename = f"Internal_Analysis_{safe_date}.md"
    internal_path = os.path.join(OUTPUT_DIR, internal_filename)
    with open(internal_path, 'w', encoding='utf-8') as f:
        f.write(internal_analysis)
        
    public_filename = f"Public_Wrap_{safe_date}.md"
    public_path = os.path.join(OUTPUT_DIR, public_filename)
    with open(public_path, 'w', encoding='utf-8') as f:
        f.write(public_wrap)

    raw_data_filename = f"Raw_Market_Data_{safe_date}.txt"
    raw_data_path = os.path.join(OUTPUT_DIR, raw_data_filename)
    with open(raw_data_path, 'w', encoding='utf-8') as f:
        f.write(market_data.get('text', ''))

    print(f"\nAnalysis complete!")
    print(f"Internal Strategy saved to {internal_filename}")
    print(f"Public Website Article saved to {public_filename}")
    print(f"Raw Market Data saved to {raw_data_filename}")
    
    # ---------------------------------------------------------
    # Step 2.5: Build HTML Output & Auto-Update index.html
    # ---------------------------------------------------------
    try:
        from build_html_wrap import build_wrap_html
        
        # Determine the target HTML filename based on the date
        try:
            date_part = market_data['date'].split(', ')[-1] if ', ' in market_data['date'] else market_data['date']
            parsed_date = datetime.datetime.strptime(date_part.strip(), '%d %B %Y')
            yyyy_mm_dd = parsed_date.strftime('%Y-%m-%d')
        except Exception:
            yyyy_mm_dd = safe_date
            
        html_filename = f"dse-wrap-{yyyy_mm_dd}.html"
        html_path = os.path.join(os.getcwd(), html_filename)
        
        template_path = os.path.join("templates", "wrap_template.html")
        build_wrap_html(public_path, template_path, html_path)
        
        # Auto-update index.html teaser section
        if metadata:
            index_path = 'index.html'
            with open(index_path, 'r', encoding='utf-8') as f:
                index_html = f.read()

            day_of_week = parsed_date.strftime('%A')
            date_str = f"{day_of_week}, {parsed_date.strftime('%d %B %Y')}"
            
            # Update date
            index_html = re.sub(r'(<div class="teaser-prem-date">).*?(</div>)', r'\g<1>' + date_str + r'\2', index_html)
            # Update headline
            index_html = re.sub(r'(<h3 class="teaser-prem-title">).*?(</h3>)', r'\g<1>' + metadata.get('headline', '') + r'\2', index_html)
            # Update body intro
            index_html = re.sub(r'(<p class="teaser-prem-body">).*?(</p>)', r'\g<1>' + metadata.get('intro', '') + r'\2', index_html)
            
            # Update stats
            index_html = re.sub(r'(<div class="teaser-prem-stat-label">DSEI</div>\s*<div class="teaser-prem-stat-value">).*?(</div>)', r'\g<1>' + metadata.get('dsei', '') + r'\2', index_html)
            index_html = re.sub(r'(<div class="teaser-prem-stat-label">Turnover</div>\s*<div class="teaser-prem-stat-value">).*?(</div>)', r'\g<1>' + metadata.get('turnover', '') + r'\2', index_html)
            index_html = re.sub(r'(<div class="teaser-prem-stat-label">Top Gainer</div>\s*<div class="teaser-prem-stat-value gain">).*?(</div>)', r'\g<1>' + metadata.get('top_gainer', '') + r'\2', index_html)
            
            # Update link
            index_html = re.sub(r'(<a href="/dse-wrap-)[^"]+(" class="btn btn-gold-solid".*?>Read the Full Wrap &rarr;</a>)', r'\g<1>' + yyyy_mm_dd + r'\2', index_html)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            print("Successfully updated index.html teaser section!")
            
    except Exception as e:
        print(f"Warning: Failed to build HTML automatically or update index: {e}")
        html_filename = None
    
    # ---------------------------------------------------------
    # Step 3: Publish to GitHub
    # ---------------------------------------------------------
    import base64
    print("\nPublishing Public Wrap to GitHub...")
    import os
    github_token = os.environ.get("GITHUB_TOKEN", "your_token_here")
    repo = "tmalundi7-jpg/amana-capital-ea"
    
    # We upload the newly generated HTML file to the root instead of the markdown to public_wraps
    if html_filename:
        upload_path = html_filename
        with open(html_filename, 'r', encoding='utf-8') as f:
            upload_content = f.read()
    else:
        upload_path = f"public_wraps/{public_filename}"
        upload_content = public_wrap
        
    github_path = upload_path
    url = f"https://api.github.com/repos/{repo}/contents/{github_path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if file exists to get SHA for updates
    sha = None
    check_resp = requests.get(url, headers=headers)
    if check_resp.status_code == 200:
        sha = check_resp.json().get("sha")
        
    encoded_content = base64.b64encode(upload_content.encode('utf-8')).decode('utf-8')
    payload = {
        "message": f"Publish Daily Wrap: {market_data['date']}",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    put_resp = requests.put(url, headers=headers, json=payload)
    if put_resp.status_code in [201, 200]:
        print(f"Successfully published {github_path} to GitHub repository '{repo}/{github_path}'!")
    else:
        print(f"Failed to publish to GitHub. Status: {put_resp.status_code}, Response: {put_resp.text}")

    print("\n--- PUBLIC WRAP PREVIEW ---")
    print(public_wrap[:1000] + "...\n(truncated for preview)")

if __name__ == "__main__":
    data = fetch_dse_data()
    if data:
        run_analysis_pipeline(data)
    else:
        print("Failed to retrieve market data.")
