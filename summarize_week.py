import re
with open("extracted_week.txt", "r", encoding="utf-8") as f:
    text = f.read()

# We can just extract the daily equity turnover from the files.
turnovers = []
for line in text.splitlines():
    if "Equity turnover" in line or "equity turnover" in line:
        print(line)
