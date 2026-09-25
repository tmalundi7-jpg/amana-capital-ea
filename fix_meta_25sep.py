import re
with open('dse-wrap-2026-09-25.html', 'r', encoding='utf-8') as f:
    h = f.read()

h = re.sub(r'<title>.*?</title>', '<title>Daily DSE Wrap | Friday, 25th September 2026 | Amana Capital East Africa</title>', h)
h = re.sub(r'<meta content="Read our daily Dar es Salaam Stock Exchange.*?" name="description"/>', '<meta content="Read our daily Dar es Salaam Stock Exchange (DSE) wrap for Friday, 25th September 2026. Get institutional-grade market intelligence, top movers, and equity research from Amana Capital East Africa." name="description"/>', h)
h = re.sub(r'<link href="https://www\.amana-capital-ea\.co\.tz/dse-wrap-.*?.html" rel="canonical"/>', '<link href="https://www.amana-capital-ea.co.tz/dse-wrap-2026-09-25.html" rel="canonical"/>', h)

with open('dse-wrap-2026-09-25.html', 'w', encoding='utf-8') as f:
    f.write(h)
print("Fixed meta tags")
