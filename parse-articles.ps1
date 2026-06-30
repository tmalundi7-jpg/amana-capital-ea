$lines = Get-Content "market-intel-raw.txt"
$articles = @{}
$currentArticle = $null
$currentContent = @()

foreach ($line in $lines) {
    if ($line -match "^(?:Article\s+)?(\d)\.(\d)\s*[-–]\s*(.*)") {
        if ($currentArticle -ne $null) {
            $articles[$currentArticle] = $currentContent
        }
        $module = $matches[1]
        $number = $matches[2]
        $title = $matches[3]
        $currentArticle = "article-$module-$number"
        $currentContent = @()
        $currentContent += "<h1>$title</h1>"
    } elseif ($currentArticle -ne $null) {
        if ($line.Trim() -eq "" -or $line -match "^This document is for general informational") {
            continue
        }
        if ($line -match "^By Amana Capital East Africa") {
            continue
        }
        if ($line -match "^\d\.\s+(.*)") {
            $h2 = $matches[1]
            $currentContent += "<h2>$h2</h2>"
        } elseif ($line.Length -lt 80 -and $line -match "^[A-Z]") {
            # Potentially a sub-heading
            $currentContent += "<h3>$line</h3>"
        } else {
            $currentContent += "<p>$line</p>"
        }
    }
}
if ($currentArticle -ne $null) {
    $articles[$currentArticle] = $currentContent
}

$articles["article-1-1"] | Out-File "test-article-1-1.html"
