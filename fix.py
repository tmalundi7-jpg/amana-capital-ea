import glob
import re
import os

files = glob.glob('**/*.html', recursive=True)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the nav-links block
    nav_match = re.search(r'(<ul[^>]*class="[^"]*nav-links[^"]*"[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
    if nav_match:
        nav_content = nav_match.group(2)
        
        # Count risk profiler links in nav_content
        rp_count = nav_content.count('href="/risk-profiler"')
        if rp_count > 1:
            print(f"Found {rp_count} risk profiler links in {f} navigation.")
            # Remove all but the first
            
            parts = nav_content.split('href="/risk-profiler"')
            # Reconstruct
            new_nav_content = parts[0] + 'href="/risk-profiler"'
            
            # This is fragile if the <li> wraps it. Let's just find the exact <li> block.
            lines = nav_content.split('\n')
            new_lines = []
            found_one = False
            for line in lines:
                if 'href="/risk-profiler"' in line:
                    if not found_one:
                        new_lines.append(line)
                        found_one = True
                    else:
                        print(f"Removing duplicate line: {line.strip()}")
                else:
                    new_lines.append(line)
            
            new_nav_str = '\n'.join(new_lines)
            new_content = content[:nav_match.start(2)] + new_nav_str + content[nav_match.end(2):]
            
            with open(f, 'w', encoding='utf-8') as outfile:
                outfile.write(new_content)
