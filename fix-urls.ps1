$dir = "C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main"
$files = Get-ChildItem -Path $dir -Filter "*.html"
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $newContent = $content.Replace('href="index.html"', 'href="/"')
    if ($content -cne $newContent) {
        [System.IO.File]::WriteAllText($file.FullName, $newContent)
        Write-Host "Updated $($file.Name)"
    }
}

$env:Path += ";C:\Program Files\Git\cmd"
Set-Location $dir
git add .
git commit -m "Clean URLs: replace index.html links with root path /"
git push origin main
