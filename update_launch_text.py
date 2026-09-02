with open('launch_helper.ps1', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace different representations of the garbled text
c = c.replace('added—', 'added and ')
c = c.replace('addedâ€”', 'added and ')

with open('launch_helper.ps1', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated launch_helper.ps1")

try:
    with open('Launch for DSE REPORT.bat', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('added—', 'added and ')
    c = c.replace('addedâ€”', 'added and ')
    with open('Launch for DSE REPORT.bat', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated Launch for DSE REPORT.bat")
except FileNotFoundError:
    print("Launch for DSE REPORT.bat not found, skipping.")

