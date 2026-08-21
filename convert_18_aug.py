import os

input_file = "extracted_18_aug_data_full.txt"
output_md = "output/Public_Wrap_18_August_2026.md"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

md_lines = []
in_wrap = False

for line in lines:
    line = line.strip()
    if line.startswith("=== Daily DSE Wrap"):
        in_wrap = True
        continue
    if line.startswith("=== Current Prices"):
        break # End of wrap data
    
    if not in_wrap:
        continue
        
    if line.startswith("Daily DSE Wrap |"):
        md_lines.append(f"# {line}")
        continue
        
    # Detect headings
    if line.startswith("1. Market Snapshot") or \
       line.startswith("2. Top Movers") or \
       line.startswith("3. In Focus:") or \
       line.startswith("4. Today’s Concept:") or \
       line.startswith("5. Bond Market:") or \
       line.startswith("6. Strategic Outlook:") or \
       line.startswith("7. Professional Approach:") or \
       line.startswith("8. Considerations for a Multi-Year Framework"):
        md_lines.append(f"## {line}")
        continue
        
    # Formatting subheadings
    if line in ["Near-Term (August):", "Medium-Term (Q3 2026):", "Long-Term:"]:
        md_lines.append(f"**{line}**")
        continue

    # Tables detection (contains |)
    if '|' in line and not line.startswith("Daily DSE Wrap |"):
        parts = [p.strip() for p in line.split('|')]
        
        # If this is the first row of a table, add a separator below it
        is_header = False
        if "Metric" in parts or "Ticker" in parts or "Counter" in parts:
            is_header = True
            
        md_lines.append("| " + " | ".join(parts) + " |")
        
        if is_header:
            separator = "| " + " | ".join(['---'] * len(parts)) + " |"
            md_lines.append(separator)
            
        continue

    # Normal text
    if line:
        md_lines.append(line)
    else:
        md_lines.append("")

# Write to markdown
os.makedirs("output", exist_ok=True)
with open(output_md, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(md_lines))

print(f"Generated {output_md}")
