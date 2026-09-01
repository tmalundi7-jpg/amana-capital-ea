$dateStr = '1 September 2026'
Get-ChildItem -Path "C:\Users\tmalu\Documents" -Filter "Current Prices*$dateStr.docx" | Select-Object FullName
