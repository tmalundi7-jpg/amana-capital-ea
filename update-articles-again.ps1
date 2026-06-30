$files = Get-ChildItem -Path "C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main" -Filter "article-*.html" | Where-Object { $_.Name -notmatch "^article-1-[12]\.html$" }

$insertText = @"
<div class="article-container">
            <div class="breadcrumb"><a href="education.html">&larr; Back to Investor Education Hub</a></div>
            <div class="article-content">
"@

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Check if the exact insertText is already there. If not, maybe it has some part of it.
    if ($content -notmatch 'class="article-container"') {
        # Insert after <main ...>
        $content = $content -replace '(<main[^>]*>)', "`$1`n$insertText"
        $content = $content -replace '(</main>)', "</div></div>`n`$1"
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Updated $($file.Name)"
    } else {
        Write-Host "Skipped $($file.Name) - already has article-container"
    }
}
