Add-Type -AssemblyName System.IO.Compression.FileSystem
$origDocx = "C:\Users\tmalu\OneDrive\Documents\Daily DSE Wrap 6th July 2026.docx"
$tempDocx = Join-Path $env:TEMP "temp_wrap_highlight.docx"
Copy-Item $origDocx -Destination $tempDocx -Force

$tempDir = Join-Path $env:TEMP "DocxExtract_Highlight"
if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
[System.IO.Compression.ZipFile]::ExtractToDirectory($tempDocx, $tempDir)

$xmlPath = Join-Path $tempDir "word\document.xml"
$xml = [xml](Get-Content $xmlPath -Raw -Encoding UTF8)

$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

$runs = $xml.SelectNodes("//w:r", $ns)
foreach ($r in $runs) {
    $highlight = $r.SelectSingleNode(".//w:highlight", $ns)
    $shd = $r.SelectSingleNode(".//w:shd", $ns)
    if ($highlight -or $shd) {
        $text = $r.SelectSingleNode(".//w:t", $ns)
        if ($text -and $text.InnerText.Trim() -ne "") {
            Write-Output $text.InnerText
        }
    }
}
