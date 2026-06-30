$lines = Get-Content "market-intel-raw.txt" -Encoding UTF8
$articles = @{}
$currentArticle = $null
$currentContent = @()

foreach ($line in $lines) {
    if ($line -match "^(?:Article\s+)?(\d)\.(\d)\s*(?:[\-\u2013\u2014]\s*)?(.*)") {
        if ($currentArticle -ne $null) {
            $articles[$currentArticle] = $currentContent -join "`n"
        }
        $module = $matches[1]
        $number = $matches[2]
        $title = $matches[3]
        $currentArticle = "article-$module-$number.html"
        $currentContent = @()
        $currentContent += "                <h1>$title</h1>"
    } elseif ($currentArticle -ne $null) {
        $trimmed = $line.Trim()
        if ($trimmed -eq "" -or $trimmed -match "^This document is for general informational" -or $trimmed -match "^\[pending\]") {
            continue
        }
        if ($trimmed -match "^By Amana Capital East Africa") {
            $currentContent += "                <p><em>By Amana Capital East Africa – Investor Education Series</em></p>"
            continue
        }
        if ($trimmed -match "^\d\.\s+(.*)") {
            $currentContent += "                <h2>$trimmed</h2>"
        } elseif ($trimmed -match "^(Apply It Now|Put It Into Practice|Action Step:)(.*)") {
            $currentContent += "                <div class=`"apply-it`">"
            $currentContent += "                    <strong>$($matches[1])</strong> $($matches[2])"
            $currentContent += "                </div>"
        } elseif ($trimmed -match "^Further Reading:(.*)") {
            $currentContent += "                <p><strong>Further Reading:</strong>$($matches[1])</p>"
        } elseif ($trimmed -match "^Key Takeaway") {
            $currentContent += "                <h3>Key Takeaway</h3>"
        } elseif ($trimmed.Length -lt 80 -and $trimmed -match "^[A-Z][a-zA-Z\s]+:$") {
            $currentContent += "                <h3>$trimmed</h3>"
        } else {
            $currentContent += "                <p>$trimmed</p>"
        }
    }
}
if ($currentArticle -ne $null) {
    $articles[$currentArticle] = $currentContent -join "`n"
}

Write-Host "Found $($articles.Count) articles."

foreach ($file in $articles.Keys) {
    if (Test-Path $file) {
        $html = Get-Content $file -Raw -Encoding UTF8
        $newContent = $articles[$file]
        # We replace the entire <div class="article-content">...</div> block
        $pattern = '(?s)<div class="article-content">.*?</main>'
        $replacement = "<div class=`"article-content`">`n$newContent`n            </div>`n        </div>`n    </main>"
        $html = $html -replace $pattern, $replacement
        Set-Content $file -Value $html -Encoding UTF8
        Write-Host "Updated $file"
    } else {
        Write-Host "File not found: $file"
    }
}
