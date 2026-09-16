import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Hero Date:", re.findall(r'<p class="hero-date">([^<]+)</p>', c))
print("DSEI End-of-Day:", re.findall(r'id="home-snapshot-date"[^>]*>([^<]+)</div>', c))
print("Daily DSE Wrap Date:", re.findall(r'<h3 class="teaser-prem-title">([^<]+)</h3>', c))
print("Terminal Feed Date:", re.findall(r'<div class="terminal-feed-header"[^>]*>.*?End-of-day[^<]*<span[^>]*>([^<]+)</span>', c, re.DOTALL))
print("Read the Full Wrap link:", re.findall(r'<a[^>]*href="([^"]+)"[^>]*>Read the Full Wrap', c))
