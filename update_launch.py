with open('launch_helper.ps1', 'r', encoding='utf-8') as f:
    content = f.read()

old_end = '''Set-Clipboard -Value $prompt
Write-Host "==========================================================" -ForegroundColor Green'''

new_end = '''Set-Clipboard -Value $prompt
Start-Process notepad.exe "update_instructions.txt"
Write-Host "==========================================================" -ForegroundColor Green'''

if old_end in content:
    content = content.replace(old_end, new_end)
    with open('launch_helper.ps1', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated launch_helper.ps1")
else:
    print("Could not find the target string in launch_helper.ps1")
