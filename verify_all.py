import re
from bs4 import BeautifulSoup

def check_html(filename):
    print(f"\n--- Checking {filename} ---")
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check DSEI, TSI, Turnover
    print("Text snippets:")
    for text in ['11 September 2026', '11th September 2026', '4,658.31', '10,400.36', '16.64', 'TZS 16.64']:
        if text in html:
            print(f"FOUND: {text}")
        else:
            print(f"MISSING: {text}")

check_html('index.html')
check_html('market-intelligence.html')
check_html('current-prices.html')
