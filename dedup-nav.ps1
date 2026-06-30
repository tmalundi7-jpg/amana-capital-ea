$files = Get-ChildItem -Path "C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main" -Filter "*.html"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # We want to remove the second occurrence of the nav block if it exists
    # The block starts with <nav class="navbar"> and ends with </nav>
    
    $regex = '(?s)(<nav class="navbar">.*?</nav>)'
    $matches = [regex]::Matches($content, $regex)
    
    if ($matches.Count -gt 1) {
        # Keep the first match, remove all subsequent matches
        $firstMatch = $matches[0].Value
        # Replace all matches with a unique token temporarily
        $content = [regex]::Replace($content, $regex, "___NAV_PLACEHOLDER___")
        
        # Replace the FIRST token with the actual nav
        $regexPlaceholder = [regex]"___NAV_PLACEHOLDER___"
        $content = $regexPlaceholder.Replace($content, $firstMatch, 1)
        
        # Replace remaining tokens with empty string
        $content = $content -replace "___NAV_PLACEHOLDER___", ""
        
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Fixed double nav in $($file.Name)"
    }
}
