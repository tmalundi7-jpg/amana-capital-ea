@echo off
powershell.exe -ExecutionPolicy Bypass -Command "$latest = Get-ChildItem -Path '.\output' -Filter 'Raw_Market_Data_*.txt' | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($latest) { Start-Process $latest.FullName } else { Write-Host 'No raw data files found.' -ForegroundColor Red; Pause }"
