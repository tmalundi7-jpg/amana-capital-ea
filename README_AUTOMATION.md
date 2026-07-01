# Amana Capital East Africa - Content Automation System

## Overview
This repository contains a fully automated CI/CD pipeline that instantly generates, updates, and deploys daily DSE market reports, archive pages, and homepage snapshots. The system runs on GitHub Actions and uses Python with Jinja2 templates.

## Setup Instructions
1. **Clone the repository:** Ensure you have the main branch checked out.
2. **Permissions:** Go to your GitHub repository Settings > Secrets and Variables > Actions. Create a new repository secret named GH_PAT. Paste a Personal Access Token (with epo permissions) into this field. This allows the GitHub Action to commit files on your behalf.
3. **Daily Usage:** To trigger a daily update, simply take the daily data, format it into data/daily_data.json based on the schema, and push it to the main branch.
4. **Triggering manually:** You can also navigate to GitHub Actions > "Daily Wrap Automation" > "Run workflow" to trigger it on demand.
5. **Scheduled run:** The workflow is also scheduled to run at 14:00 UTC (5:00 PM EAT) on weekdays.

## How to write the Daily JSON
The data/daily_data.json file is the brain of the operation. Open it and modify the market_snapshot, oreign_flow, and equities list with the new data. Ensure the 	rade_date (e.g. "2026-07-02") and publication_date (e.g. "2 July 2026") are correct. 

The nalysis block allows the CIO/Analyst to write out the qualitative segments of the wrap (In Focus, Strategic Outlook, etc.). 

## Troubleshooting
- **Workflow fails during generation:** Check the syntax of your daily_data.json. A missing comma or unclosed quote will break JSON parsing.
- **Pages don't update:** Ensure GH_PAT is valid and hasn't expired.
- **Formatting looks wrong:** Ensure you aren't using HTML tags inside the JSON strings unless explicitly supported. The Python script handles percentage calculations automatically.
