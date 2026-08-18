# Amana Capital EA

## Project Overview
This repository contains the codebase and automation scripts for the Amana Capital East Africa website. The platform serves as the central hub for market intelligence, presenting the latest Dar es Salaam Stock Exchange (DSE) insights, live snapshots, and daily market wraps. All files track the state of the live production website and facilitate seamless deployments.

## Features
- **Market Intelligence Page**: An archive of historical market wraps and deep-dive equity analysis.
- **Live DSE Snapshot**: Real-time tracker for the DSEI, TSI, Turnover, and the day's Top Gainers and Losers.
- **Daily DSE Wrap**: A daily digest of market activity, highlighted on the homepage.
- **DSE Market Heatmap**: Visual representation of the latest top movers in the market.
- **Quick Links / Current Prices**: Direct access to essential market metrics.
- **Research Archive**: A dedicated repository for previously published DSE wraps and research reports.

## Tech Stack
- **HTML5**: For the semantic structure of the website.
- **CSS3 / Vanilla CSS**: For layout and dynamic styling, including custom color variables for gain/loss indicators.
- **JavaScript**: For interactive components and basic client-side logic.
- **Python (Automation)**: Scripts for parsing DSE Word documents, injecting DOM updates into HTML, QA validation, and cache purging.
- **JSON**: Used as the intermediate structured data format extracted from daily wraps.

## Repository Structure
```
├── .Cloudflare API/                 # (Ignored) Local Cloudflare API credentials for cache purging
├── output/                          # Markdown output of parsed wraps and market data
├── update_evidence_*/               # Screenshots and validation artifacts from QA checks
├── index.html                       # The website homepage featuring the Daily DSE Wrap and Live Snapshot
├── market-intelligence.html         # Main insights and intelligence page
├── market-intelligence-archive.html # Archive for previous daily wraps
├── script.js / script.min.js        # Client-side JavaScript logic
├── style.css / style.min.css        # Main stylesheet
├── extracted_dse_data_*.json        # JSON payloads extracted from the daily Word documents
├── purge_cloudflare.py              # Script to manually purge Cloudflare CDN edge cache
├── qa_verify_final.py               # Script used to validate DOM injection of market data
├── update_website.py                # Automation script to update HTML files
└── README.md                        # Project documentation (this file)
```

## Local Setup
1. **Clone the repository:** 
   ```bash
   git clone https://github.com/tmalundi7-jpg/amana-capital-ea.git
   cd amana-capital-ea
   ```
2. **Run locally:** No complex build step is required. You can serve the site locally using Python's built-in HTTP server to preview changes:
   ```bash
   python -m http.server 8000
   ```
3. **Dependencies:** The Python automation scripts require a few basic libraries (e.g., `python-docx` for Word document extraction, `beautifulsoup4` for HTML manipulation). Install them via pip if running the update workflow locally.

## DSE Daily Wrap Update Workflow
The daily process for updating the DSE market data follows this strict flow:
1. **Extraction:** A Python script (or an AI agent) reads the source Word document (e.g., `Daily DSE Wrap 18 August 2026.docx`) and extracts key metrics (DSEI, Turnover, Top Mover, Gainers, Losers).
2. **JSON Generation:** The extracted data is saved to a date-stamped JSON file, such as `extracted_dse_data_18_aug_2026.json`.
3. **Website Update:** The extracted values are systematically injected into `index.html` (replacing the previous day's metrics) without altering the layout or CSS.
4. **Archive Rotation:** The previous day's wrap is migrated to the `market-intelligence-archive.html` page.
5. **Validation:** A QA script (like `qa_verify_final.py`) parses the updated HTML to confirm that all required strings and values have been correctly injected.
6. **Commit:** The updated `index.html`, any updated archive pages, and the new JSON file are committed to the repository.

## Deployment
1. **Push to Production:** The website is deployed automatically when changes are pushed to the `main` branch of this repository.
   ```bash
   git push origin main
   ```
2. **Cache Clearing:** Since the live site is behind Cloudflare, aggressive caching may prevent updates from showing immediately. A cache purge script (`purge_cloudflare.py`) is executed post-deployment using the Cloudflare API to invalidate the CDN cache.

## Important Files
- `index.html`: The core landing page that receives daily updates.
- `extracted_dse_data_18_aug_2026.json` (and similar date-stamped files): The historical raw data extracted for the daily wraps.
- `qa_verify_final.py`: The headless DOM checking script used to ensure the live HTML matches the extracted JSON.

## Security and Privacy
- **API Keys:** Never store API keys, Cloudflare tokens, or deployment secrets in tracked files in this repository. Ensure that the `.Cloudflare API/` directory and `.env` files are added to `.gitignore`.
- Use environment variables (or GitHub Secrets if using GitHub Actions) for all sensitive operations.

## License
No license is currently specified. All rights reserved by Amana Capital East Africa.
