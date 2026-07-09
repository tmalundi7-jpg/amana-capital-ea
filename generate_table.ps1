Add-Type -AssemblyName System.IO.Compression.FileSystem
$origDocx = "C:\Users\tmalu\OneDrive\Documents\Current Prices - 09th July 2026.docx"
$tempDocx = Join-Path $env:TEMP "temp_prices_generate_9.docx"
Copy-Item $origDocx -Destination $tempDocx -Force

$tempDir = Join-Path $env:TEMP "DocxExtract_Gen_9"
if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
[System.IO.Compression.ZipFile]::ExtractToDirectory($tempDocx, $tempDir)

$xmlPath = Join-Path $tempDir "word\document.xml"
$xml = [xml](Get-Content $xmlPath -Raw -Encoding UTF8)
$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

$tables = $xml.SelectNodes("//w:tbl", $ns)
$table = $tables[0]
$rows = $table.SelectNodes(".//w:tr", $ns)

$html = @"
<table class="data-table" style="margin: 0; width: 100%; border-collapse: collapse;">
    <thead>
        <tr style="background-color: var(--navy); color: var(--white); text-align: left;">
            <th style="padding: 1rem;">Ticker</th>
            <th style="padding: 1rem;">Company</th>
            <th style="padding: 1rem;">Sector</th>
            <th style="padding: 1rem; text-align: right;">Last Price (TZS)</th>
            <th style="padding: 1rem; text-align: right;">Change (%)</th>
            <th style="padding: 1rem; text-align: right;">Volume</th>
            <th style="padding: 1rem; text-align: right;">Turnover (TZS)</th>
        </tr>
    </thead>
    <tbody>
"@ + "
"

for ($i = 1; $i -lt $rows.Count; $i++) {
    $row = $rows[$i]
    $cells = $row.SelectNodes(".//w:tc", $ns)
    $cellTexts = @()
    foreach ($cell in $cells) {
        $paras = $cell.SelectNodes(".//w:p", $ns)
        $cellText = ""
        foreach ($p in $paras) {
            $texts = $p.SelectNodes(".//w:t", $ns)
            $pText = ""
            foreach ($t in $texts) {
                $pText += $t.InnerText
            }
            $cellText += $pText + " "
        }
        $cellText = $cellText.Trim()
        $cellText = $cellText -replace '\p{Pd}', '-'
        $cellText = $cellText -replace '[^0-9\.\+\-%,A-Za-z \(\)&]', ''
        $cellTexts += $cellText
    }
    
    if ($cellTexts.Count -lt 7) { continue }
    
    $ticker = $cellTexts[0]
    $company = $cellTexts[1]
    $sector = $cellTexts[2]
    $price = $cellTexts[3]
    $change = $cellTexts[4]
    $volume = $cellTexts[5]
    $turnover = $cellTexts[6]
    
    $changeHtml = $change
    if ($change -like "*+*") {
        $changeHtml = "<span style='color:var(--gain)'>$change</span>"
    } elseif ($change -like "*-*") {
        $changeHtml = "<span style='color:var(--loss)'>$change</span>"
    }
    
    $html += "        <tr style='border-bottom: 1px solid var(--stone);'>
"
    $html += "            <td style='padding: 1rem; font-weight: 600;'>$ticker</td>
"
    $html += "            <td style='padding: 1rem;'>$company</td>
"
    $html += "            <td style='padding: 1rem; color: var(--mist);'>$sector</td>
"
    $html += "            <td style='padding: 1rem; text-align: right;'>$price</td>
"
    $html += "            <td style='padding: 1rem; text-align: right;'>$changeHtml</td>
"
    $html += "            <td style='padding: 1rem; text-align: right;'>$volume</td>
"
    $html += "            <td style='padding: 1rem; text-align: right;'>$turnover</td>
"
    $html += "        </tr>
"
}

$html += "    </tbody>
</table>"

$fileContent = Get-Content "current-prices.html" -Raw -Encoding UTF8
$fileContent = $fileContent -replace '(?s)<table class="data-table".*?</table>', $html
$fileContent = $fileContent -replace 'End-of-day data, 6th July 2026', 'End-of-day data, 9th July 2026'
Set-Content "current-prices.html" -Value $fileContent -Encoding UTF8
Write-Output "Table replaced successfully in current-prices.html"
