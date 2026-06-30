Get-ChildItem -Path . -Filter *.html -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $newContent = [regex]::Replace($content, 'href="([a-zA-Z0-9_-]+)\.html"', 'href="/$1"')
    if ($content -cne $newContent) {
        Set-Content -Path $_.FullName -Value $newContent -NoNewline
        Write-Host "Updated: $($_.FullName)"
    }
}
