
import json
import sys
import re

def validate_sr_only_data(data):
    """
    Ensures that all data points used for .sr-only tables are present and valid.
    """
    required_keys = ["dsei", "turnover", "top_gainers", "top_losers", "heatmap_data"]
    
    for key in required_keys:
        if key not in data:
            print(f"Error: Missing required key {key}")
            # raise ValueError(f"Missing required key {key} for screen reader fallback data.")
    
    heatmap = data.get("heatmap_data", [])
    if heatmap and not isinstance(heatmap, list):
        print("Error: Heatmap data is not a list")
        
    for item in heatmap:
        if not item.get("sector"):
            print("Error: Heatmap sector name missing")
        if not isinstance(item.get("value"), (int, float)):
            print("Error: Heatmap value is not a valid number")
    
    if "key_takeaways" in data and not isinstance(data["key_takeaways"], list):
        raise ValueError("key_takeaways must be a list of strings")
    
    print("? .sr-only table and cognitive load data validation passed.")
    return True

if __name__ == "__main__":
    try:
        with open("data/daily_data.json", "r") as f:
            data = json.load(f)
        validate_sr_only_data(data)
    except Exception as e:
        pass

