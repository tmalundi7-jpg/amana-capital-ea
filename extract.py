import json
import os
import re

transcript_path = r"C:\Users\tmalu\.gemini\antigravity\brain\64377198-9119-4b02-a3fb-ed4757da256e\.system_generated\logs\transcript_full.jsonl"
output_path = r"C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main\batch1.txt"

content_blocks = []

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            if data.get("type") == "USER_INPUT":
                content = data.get("content", "")
                if "Article 1.1" in content and "Article 1.5" in content:
                    content_blocks.append(content)
        except Exception:
            pass

if content_blocks:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content_blocks[0])
    print("Extracted batch 1 successfully.")
else:
    print("Could not find batch 1 in transcript.")
