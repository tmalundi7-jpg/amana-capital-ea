$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$template = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} - Amana Capital East Africa</title>
    <link href="https://fonts.googleapis.com/css2?family=Alef:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <style>
        .article-container { max-width: 800px; margin: 4rem auto; padding: 2rem; background: var(--cream); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .article-content { font-family: 'Alef', sans-serif; color: var(--navy); }
        .article-content h1 { color: var(--navy); margin-bottom: 0.5rem; font-size: 2.2rem; }
        .article-content h2, .article-content h3, .article-content h4 { color: var(--navy); margin-top: 2rem; margin-bottom: 1rem; }
        .article-content p { line-height: 1.7; margin-bottom: 1.5rem; font-size: 1.1rem; }
        .article-content ul, .article-content ol { margin-bottom: 1.5rem; padding-left: 2rem; }
        .article-content li { margin-bottom: 0.5rem; line-height: 1.6; font-size: 1.1rem; }
        .article-content table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
        .article-content th, .article-content td { border: 1px solid #d1d5db; padding: 0.75rem; text-align: left; }
        .article-content th { background-color: var(--navy); color: white; }
        .apply-it { background: var(--cream); border-left: 4px solid var(--gold); padding: 1.5rem; margin: 2rem 0; font-style: italic; }
        .breadcrumb { margin-bottom: 2rem; font-size: 0.9rem; }
        .breadcrumb a { color: var(--gold); text-decoration: none; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container nav-container">
            <a href="index.html" class="brand-link">
                <svg viewBox="0 0 32 44" class="brand-icon"><path d="M0,44 L13,0 L19,0 L6,44Z" fill="currentColor"/><rect x="21" y="0" width="8" height="44" fill="currentColor"/><rect x="0" y="19" width="21" height="4" fill="currentColor"/></svg>
                <div class="brand-text">
                    <div class="brand-title">AMANA CAPITAL</div>
                    <div class="brand-sub">EAST AFRICA</div>
                </div>
            </a>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="market-intelligence.html">Market Intelligence</a></li>
                <li><a href="education.html" class="active">Investor Education</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
        </div>
    </nav>

    <main class="container">
        <div class="article-container">
            <div class="breadcrumb"><a href="education.html">&larr; Back to Investor Education Hub</a></div>
            <div class="article-content">
                {{BODY}}
            </div>
            
            {{APPLY_IT}}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            {{FOOTER}}
            <div class="footer-links">
                <div>&copy; 2026 Amana Capital East Africa Limited.</div>
                <div style="display: flex; gap: 1.5rem;">
                    <a href="privacy.html">Privacy Policy</a>
                    <a href="terms.html">Terms of Use</a>
                    <a href="cookies.html">Cookie Policy</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
"@

$footer = Get-Content -Path "footer.html" -Encoding UTF8 -Raw

$allText = ""
foreach ($file in @("batch1.txt", "batch2.txt", "batch3.txt", "batch4.txt")) {
    if (Test-Path $file) {
        $allText += (Get-Content -Path $file -Encoding UTF8 -Raw) + "`n"
    }
}

$applyIt42 = @"
<div class="apply-it">
    <strong>APPLY IT NOW</strong><br>
    Go to the Current Prices page and pick any stock. Divide its "Last Price" by its earnings per share (find the latest EPS in its annual report). What is the P/E ratio? Now compare that to the P/E of another stock in the same sector. Which appears cheaper? Why might the pricier one still be a better investment? (Hint: growth, moat, quality.)
</div>
"@

$applyIt53 = @"
<div class="apply-it">
    <strong>APPLY IT NOW</strong><br>
    Using an online compound interest calculator, input your current monthly investment amount, an assumed annual return of 9% (realistic for a diversified portfolio), and a horizon of 20 years. How much would you have? Now halve the return to 6% — how much difference does that make? Finally, increase the monthly contribution by just TZS 20,000. The result will prove that consistency beats both luck and genius.
</div>
"@

$lines = $allText -split "`n"
$articles = @()
$currentArticle = $null

foreach ($line in $lines) {
    # Match standard articles
    if ($line -match '^(?:###\s*)?(?:Article|New Article).*?(\d\.\d)\s*.{1,3}\s*(.*)$' -or $line -match '^(?:###\s*)?Case Study:\s*(CRDB Bank)\s*.{1,3}\s*(.*)$') {
        if ($currentArticle) {
            $articles += $currentArticle
        }
        
        $num = $matches[1]
        $title = $matches[2]
        
        if ($line -match 'Case Study:') {
            $num = "7.3"
            $title = "Case Study: CRDB Bank - A Fundamental Walk-Through"
        }

        $currentArticle = @{
            Number = $num
            Title = $title
            Lines = @()
        }
    } elseif ($currentArticle -ne $null) {
        $currentArticle.Lines += $line
    }
}

if ($currentArticle) {
    $articles += $currentArticle
}

foreach ($article in $articles) {
    $num = $article.Number
    $title = $article.Title
    $bodyLines = $article.Lines
    
    $htmlBody = "<h1>$title</h1>`n"
    
    $inTable = $false
    
    foreach ($line in $bodyLines) {
        $l = $line.Trim()
        if ($l -eq "") { continue }
        
        if ($l -match '^#{1,4}\s+(.*)') {
            $htmlBody += "<h2>$($matches[1])</h2>`n"
        } elseif ($l -match '^\d+\.\s+(.*)') {
            $htmlBody += "<h3>$($matches[1])</h3>`n"
        } elseif ($l -match '^-\s+(.*)' -or $l -match '^\*\s+(.*)') {
            $htmlBody += "<li style='margin-left: 20px;'>$($matches[1])</li>`n"
        } elseif ($l -match '\|') {
            # Very rudimentary table support
            if (-not $inTable) {
                $htmlBody += "<table>`n"
                $inTable = $true
            }
            $cells = $l -split '\|' | Where-Object { $_.Trim() -ne "" -and $_.Trim() -notmatch '^---' }
            if ($cells.Count -gt 0) {
                $htmlBody += "<tr>"
                foreach ($cell in $cells) {
                    $htmlBody += "<td>$($cell.Trim())</td>"
                }
                $htmlBody += "</tr>`n"
            }
        } else {
            if ($inTable) {
                $htmlBody += "</table>`n"
                $inTable = $false
            }
            $htmlBody += "<p>$l</p>`n"
        }
    }
    if ($inTable) {
        $htmlBody += "</table>`n"
    }
    
    # Replace bold markdown
    $htmlBody = $htmlBody -replace '\*\*(.*?)\*\*', '<strong>$1</strong>'
    
    $applyIt = ""
    if ($num -eq "4.2") { $applyIt = $applyIt42 }
    if ($num -eq "5.3") { $applyIt = $applyIt53 }
    
    $numStr = $num -replace '\.', '-'
    $fileName = "article-$numStr.html"
    
    $finalHtml = $template.Replace("{{TITLE}}", "Article $num - $title").Replace("{{BODY}}", $htmlBody).Replace("{{FOOTER}}", $footer).Replace("{{APPLY_IT}}", $applyIt)
    
    [System.IO.File]::WriteAllText("C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main\$fileName", $finalHtml, [System.Text.Encoding]::UTF8)
}

Write-Host "Generated HTML files."
