$dateStr = '1 September 2026'
$wrap = Get-ChildItem -Path "C:\Users\tmalu\Documents" -Filter "Daily DSE Wrap*$dateStr.docx" | Select-Object -First 1
$prices = Get-ChildItem -Path "C:\Users\tmalu\Documents" -Filter "Current Prices*$dateStr.docx" | Select-Object -First 1
Write-Host "Wrap: $($wrap.FullName)"
Write-Host "Prices: $($prices.FullName)"
