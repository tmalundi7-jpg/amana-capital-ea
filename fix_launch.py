import re

with open('launch_helper.ps1', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("- Update the 'Live DSE Snapshot' metrics", "- Update the hero meta date under \"Latest Report\" at the top.\n- Update the 'Live DSE Snapshot' metrics")

with open('launch_helper.ps1', 'w', encoding='utf-8') as f:
    f.write(c)
