$targetNav = @"
<nav class="navbar">
<div class="container nav-container">
<a class="brand-link" href="/">
<svg aria-hidden="true" class="brand-icon" viewbox="0 0 32 44"><path d="M0,44 L13,0 L19,0 L6,44Z" fill="currentColor"></path><rect fill="currentColor" height="44" width="8" x="21" y="0"></rect><rect fill="currentColor" height="4" width="21" x="0" y="19"></rect></svg>
<div class="brand-text vertical-logo">
<span class="logo-word-primary">AMANA CAPITAL</span>
<span class="logo-word-secondary">East Africa Limited</span>
</div>
</a>

<button aria-label="Open menu" class="mobile-toggle" id="mobile-toggle">&#9776;</button>
<ul class="nav-links" id="nav-links">
<li><a href="/">Home</a></li>
<li><a href="/market-intelligence">Market Intelligence</a></li>
<li><a href="/education">Investor Education</a></li>
<li><a href="/bond-calculator">Bond Calculator</a></li>
<li><a href="/risk-profiler">Risk Profiler</a></li>
<li><a href="/about">About</a></li>
<li><a href="/contact">Contact</a></li>
</ul>
</div>
</nav>
"@

$files = Get-ChildItem -Filter *.html -Recurse -File

foreach ($file in $files) {
    # Skip backup and output files to avoid messing things up
    if ($file.Name -match "\.bak" -or $file.Name -match "mammoth_output") { continue }
    
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # Check if file has a nav
    if ($content -match '(?s)<nav class="navbar">.*?</nav>') {
        $newContent = $content -replace '(?s)<nav class="navbar">.*?</nav>', $targetNav
        
        if ($newContent -cne $content) {
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
            Write-Host "Updated $($file.Name)"
        }
    }
}
