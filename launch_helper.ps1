$inputDate = Read-Host "Enter report date (dd/MM/yyyy) or press Enter to use today's date"

if ([string]::IsNullOrWhiteSpace($inputDate)) {
    $targetDate = Get-Date
    if ($targetDate.DayOfWeek -eq 'Saturday') {
        Write-Host "Today is Saturday. Using Friday's data..." -ForegroundColor Cyan
        $targetDate = $targetDate.AddDays(-1)
    }
    elseif ($targetDate.DayOfWeek -eq 'Sunday') {
        Write-Host "Today is Sunday. Using Friday's data..." -ForegroundColor Cyan
        $targetDate = $targetDate.AddDays(-2)
    }
} else {
    try {
        $targetDate = [datetime]::ParseExact($inputDate, 'dd/MM/yyyy', $null)
    } catch {
        Write-Host "Invalid date format. Please use dd/MM/yyyy (e.g. 31/08/2026)" -ForegroundColor Red
        exit 1
    }
}

$dateStr = $targetDate.ToString("d MMMM yyyy")
$shortDate = $targetDate.ToString("yyyy-MM-dd")

$wrapDoc = "C:\Users\tmalu\Documents\Daily DSE Wrap $dateStr.docx"
$pricesDoc = "C:\Users\tmalu\Documents\Current Prices $dateStr.docx"

Write-Host "Looking for files for $($dateStr):"
Write-Host "- $wrapDoc"
Write-Host "- $pricesDoc"
Write-Host ""

$missing = $false
if (!(Test-Path $wrapDoc)) {
    Write-Host "ERROR: Daily Wrap document not found at $wrapDoc" -ForegroundColor Red
    $missing = $true
}
if (!(Test-Path $pricesDoc)) {
    Write-Host "ERROR: Current Prices document not found at $pricesDoc" -ForegroundColor Red
    $missing = $true
}

if ($missing) {
    exit 1
}

$prompt = @"
Please process the new daily wrap and update the website exactly according to the following instructions. 
The new data is located in "$wrapDoc" and the prices are in "$pricesDoc".

1. Generate the New Wrap Page:
Parse the new docx file and generate a new dedicated HTML page (e.g., dse-wrap-$shortDate.html). Maintain the exact text, headings, bullet points, and tables.

2. Update the Home Page (index.html):
- Live DSE Snapshot: Update the snapshot date label, DSEI, TSI, Turnover, Top 3 Gainers, and Top 3 Losers. Ensure you update the inner grid values (like id="home-dsei").
- CRITICAL HTML SAFETY: Do NOT delete or modify the outer `<div>` flexbox wrappers when updating the lists of Gainers/Losers. Just update the inner spans.
- Bottom Teaser (Latest Research / Today's DSE Wrap): Update the teaser date, headline title, introductory paragraph, the mini-stats below it, and the href link in the "Read the Full Wrap" button to point to the new wrap page.

3. Update Market Intelligence (market-intelligence.html):
- Update the 'Live DSE Snapshot' metrics, Top Gainers, and Top Losers to match the homepage.
- CRITICAL HTML SAFETY: Do NOT delete or modify the outer `<div>` flexbox wrappers when updating the lists of Gainers/Losers. Just update the inner text values.
- Under 'Daily DSE Wrap Archive', update the featured spotlight to point to the newly generated wrap page. Update its href link, date, title, and short excerpt.

4. Update Current Prices (current-prices.html):
- Rebuild the main equities table using the latest prices.
- Update the Market Snapshot bar at the top (DSEI, TSI, Total Turnover, Volume, and Date).

5. Update the Archive (market-intelligence-archive.html):
- Add the newly generated wrap into the archive list.
- CRITICAL: Format the new entry exactly like the older entries using the list-style <div class="arc-row"> structure, NOT the <a class="archive-row"> card structure. Ensure the alternating background color pattern (background: rgba(11,29,58,0.02)) is perfectly maintained.

Please ensure NO external data is added—use ONLY the figures provided in the source documents. Deploy subagents if necessary to accomplish this. Do not stop until everything is done professionally with no errors or issues. Once you have verified all changes across these four files, commit and push to live.
"@

Set-Content -Path "update_instructions.txt" -Value $prompt -Encoding UTF8
Set-Clipboard -Value $prompt
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "SUCCESS! The instructions have been copied to your clipboard!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Simply open Antigravity, press Ctrl+V to paste, and hit Enter." -ForegroundColor Yellow
exit 0
