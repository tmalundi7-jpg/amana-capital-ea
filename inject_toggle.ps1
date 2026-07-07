$htmlFiles = Get-ChildItem -Path . -Filter *.html -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $modified = $false
    
    if ($content -notmatch 'id="theme-toggle"') {
        $content = $content -replace '<button class="mobile-toggle"', '<button id="theme-toggle" class="theme-toggle" aria-label="Toggle Dark Mode">🌙</button>`n        <button class="mobile-toggle"'
        $modified = $true
    }
    
    if ($content -notmatch 'theme-toggle\.js') {
        # use case insensitive replace for </body>
        $content = $content -ireplace '</body>', '<script src="/js/theme-toggle.js"></script>`n</body>'
        $modified = $true
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
    }
}
