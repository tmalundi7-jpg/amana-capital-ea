import urllib.request
import ssl

urls = [
    "https://www.amana-capital-ea.co.tz/",
    "https://www.amana-capital-ea.co.tz/current-prices",
    "https://www.amana-capital-ea.co.tz/market-intelligence",
    "https://www.amana-capital-ea.co.tz/dse-wrap-2026-09-11"
]

ctx = ssl.create_default_context()
for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, context=ctx)
        print(f"OK: {url} -> {res.status}")
    except Exception as e:
        print(f"ERROR: {url} -> {e}")
