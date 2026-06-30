$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$footerSnippet = @"
            <div class="footer-disclaimer" style="margin-bottom: 2rem; font-size: 0.9rem; color: #9ca3af; line-height: 1.6;">
                <strong>Regulatory Disclaimer:</strong> This document is for general informational and educational purposes only. 
                Nothing contained herein constitutes financial, investment, legal, or tax 
                advice and should not be relied upon as such. Any investment decision you 
                make is solely your own responsibility. The value of investments and the 
                income from them can go down as well as up, and you may not get back the 
                amount originally invested. Past performance is not a reliable indicator 
                of future results. Capital is at risk, and you may incur losses — including 
                the total loss of your invested capital — which you alone will bear.
                <br><br>
                Amana Capital East Africa Limited is a registered investment advisory and 
                fund management firm under the Capital Markets and Securities Authority 
                (CMSA), Tanzania. Licence number: [pending]. Our registration does not 
                imply that CMSA approves or endorses the contents of this material.
            </div>
"@

$files = @(
    "about.html", "contact.html", "cookies.html", "current-prices.html", 
    "dse-wrap-2026-06-28.html", "dse-wrap-2026-06-29.html", "index.html", 
    "investing-101-1.html", "investing-101-2.html", "market-intelligence.html", 
    "privacy.html", "terms.html"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content -Path $file -Encoding UTF8 -Raw
        $newContent = [regex]::Replace($content, '(?s)<div class="footer-disclaimer">.*?</div>', $footerSnippet)
        if ($newContent -ne $content) {
            [System.IO.File]::WriteAllText("C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main\$file", $newContent, [System.Text.Encoding]::UTF8)
            Write-Host "Updated $file"
        }
    }
}
Write-Host "Disclaimer update complete."
