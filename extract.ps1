Add-Type -AssemblyName System.IO.Compression.FileSystem

$docx1 = "C:\Users\tmalu\OneDrive\Documents\Current Prices - 3rd July 2026.docx"
$docx2 = "C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 3rd July 2026.docx"
$out = "C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main\extracted_data.json"

function Extract-DocxText($path) {
    if (-not (Test-Path $path)) { return "File not found: $path" }
    
    $tempDir = Join-Path $env:TEMP ([guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path $tempDir | Out-Null
    
    [System.IO.Compression.ZipFile]::ExtractToDirectory($path, $tempDir)
    
    $xmlPath = Join-Path $tempDir "word\document.xml"
    $xmlContent = Get-Content -Path $xmlPath -Raw
    
    # Very simple regex to extract text from <w:t> tags
    $matches = [regex]::Matches($xmlContent, '(?<=<w:t[^>]*>).*?(?=</w:t>)')
    $text = @()
    foreach ($m in $matches) {
        $text += $m.Value
    }
    
    Remove-Item -Path $tempDir -Recurse -Force
    return ($text -join " ")
}

$text1 = Extract-DocxText $docx1
$text2 = Extract-DocxText $docx2

$data = @{
    prices = $text1
    wrap = $text2
}

$data | ConvertTo-Json -Depth 3 | Set-Content -Path $out
Write-Host "Extraction successful."
