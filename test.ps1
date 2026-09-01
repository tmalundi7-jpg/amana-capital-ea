$dateStr = '1 September 2026'
Get-ChildItem -Path "C:\Users\tmalu\Documents" -Filter "Daily DSE Wrap*$dateStr.docx" | Select-Object FullName
