import re

with open("extracted_week.txt", "r", encoding="utf-8") as f:
    text = f.read()

patterns = [
    r'(?i)14th? september',
    r'(?i)15th? september',
    r'(?i)16th? september',
    r'(?i)17th? september',
    r'(?i)18th? september',
    r'(?i)next week',
    r'(?i)week ahead'
]

for p in patterns:
    matches = re.finditer(p, text)
    for m in matches:
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 100)
        print(f"Match for {p}: ... {text[start:end]} ...\n")
