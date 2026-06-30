$files = Get-ChildItem -Path "C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main" -Filter "article-*.html"

$insertText = @"
<div class="article-container">
            <div class="breadcrumb"><a href="education.html">&larr; Back to Investor Education Hub</a></div>
            <div class="article-content">
"@

foreach ($file in $files) {
    if ($file.Name -match "^article-1-[12]\.html$") {
        # skip 1-1 and 1-2, or wait, maybe the user specifically said 1-3 to 7-5.
    }
    
    $content = Get-Content $file.FullName -Raw
    
    # Check if it already has breadcrumb
    if ($content -notmatch 'class="breadcrumb"') {
        # Replace <main...> with <main...> + insertText
        $content = $content -replace '(<main[^>]*>)', "`$1`n$insertText"
        
        # Replace </main> with </div></div></main>
        $content = $content -replace '(</main>)', "</div></div>`n`$1"
        
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Updated $($file.Name)"
    }
}
