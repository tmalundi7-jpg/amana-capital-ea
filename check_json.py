import json
from bs4 import BeautifulSoup
import re
import os

with open("extracted_dse_wrap_17_aug_2026.json", "r", encoding="utf-8") as f:
    wrap_data = json.load(f)

with open("extracted_current_prices_17_aug_2026.json", "r", encoding="utf-8") as f:
    prices_data = json.load(f)

# Update market-intelligence.html
with open("market-intelligence.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Update snapshot
snapshot = wrap_data.get("snapshot", {})
if "DSEI" in snapshot:
    soup.find(id="mi-dsei").string = snapshot["DSEI"]
    # Add span if needed, need to parse exactly how it is represented in JSON.

print(wrap_data.keys())
print(prices_data.keys())
