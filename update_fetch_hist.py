import os

with open('fetch_historical_dse.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_str = 'print(f"SUCCESS! Raw data saved to {filepath}")'
new_str = '''print(f"SUCCESS! Raw data saved to {filepath}")
                import subprocess
                subprocess.Popen(['notepad.exe', filepath])'''

if old_str in content:
    content = content.replace(old_str, new_str)
    with open('fetch_historical_dse.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated fetch_historical_dse.py")
else:
    print("Could not find the target string.")
