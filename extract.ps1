$transcriptPath = 'C:\Users\tmalu\.gemini\antigravity\brain\64377198-9119-4b02-a3fb-ed4757da256e\.system_generated\logs\transcript_full.jsonl'
$outputPath = 'C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main\batch1.txt'

$reader = [System.IO.StreamReader]::new($transcriptPath)
try {
    while ($null -ne ($line = $reader.ReadLine())) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        
        # Simple string matching is faster than parsing JSON for every line
        if ($line.Contains('"type":"USER_INPUT"') -and $line.Contains('Article 1.1') -and $line.Contains('Article 1.5')) {
            # Convert JSON back to object
            $data = ConvertFrom-Json $line
            if ($data.content -and $data.content.Contains('Article 1.1')) {
                [System.IO.File]::WriteAllText($outputPath, $data.content)
                Write-Host "Extracted batch 1 successfully."
                break
            }
        }
    }
} finally {
    $reader.Close()
}
