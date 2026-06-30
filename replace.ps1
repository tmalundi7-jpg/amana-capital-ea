$pattern = '(?s)losses\s+(?:â€”|—|â€"|-)\s+including\s+the\s+total\s+loss\s+of\s+your\s+invested\s+capital\s+(?:â€”|—|â€"|-)\s+which\s+you\s+alone\s+will\s+bear\.?'
$replacement = 'losses including the total loss of your invested capital which you alone will bear.'
Get-ChildItem -Filter "*.html" -Recurse | ForEach-Object {
    $path = $_.FullName
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    
    $changed = $false
    if ($content -match $pattern) {
        $content = [regex]::Replace($content, $pattern, $replacement)
        $changed = $true
    }
    
    if ($content.Contains('â€”')) {
        $content = $content.Replace('â€”', '-')
        $changed = $true
    }

    if ($changed) {
        [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        Write-Host "Updated $path"
    }
}
