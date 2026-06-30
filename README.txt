Deployment Guide - Amana Capital East Africa

1. HTML Generation Completed
All 34 Investor Education articles have been generated as standalone HTML files (`article-*.html`).
The master hub `education.html` has been updated to link to all of these articles.
The global footer (with the enhanced regulatory disclaimer) has been injected into all existing root pages (index.html, about.html, etc.).

2. Manual Upload to GitHub
Because this environment does not have Git installed, you must upload these files manually to your GitHub repository:
- Go to your GitHub repository in the web browser.
- Click "Add file" -> "Upload files".
- Drag and drop all the newly generated `article-*.html` files, `education.html`, and the modified root HTML files (`index.html`, `about.html`, `contact.html`, `market-intelligence.html`, etc.) into the upload area.
- Commit the changes directly to your main branch.

3. Automated Deployment
If you are using GitHub Pages or a GitHub Actions workflow to deploy the site:
- Make sure your repository is set up with GitHub Pages pointing to the `main` branch.
- If you have an action that requires a Personal Access Token (`GH_PAT`), ensure it is configured in your repository secrets (Settings > Secrets and variables > Actions > New repository secret).
- Once the files are uploaded, the GitHub Actions workflow will trigger automatically and deploy your site to the live domain.

4. Next Steps
Review the live site once deployed. Verify that the "Apply It Now" boxes appear correctly in Articles 4.2 and 5.3, and that the Enhanced Disclaimer displays properly at the bottom of all pages.
