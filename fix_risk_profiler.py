import glob
import re
import os

def fix_duplicate_links():
    files = glob.glob('**/*.html', recursive=True)
    fixed_count = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex to find the <ul class="nav-links"> block
        nav_match = re.search(r'(<ul[^>]*class="[^"]*nav-links[^"]*"[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
        if nav_match:
            nav_content = nav_match.group(2)
            # Find all occurrences of risk-profiler list items
            rp_pattern = re.compile(r'\s*<li>\s*<a href="/risk-profiler"[^>]*>Risk Profiler</a>\s*</li>')
            matches = rp_pattern.findall(nav_content)
            
            if len(matches) > 1:
                # We have duplicates! Let's remove the second one.
                # Replace the exact nav_content within the main string
                # We'll replace the matches one by one, keeping the first.
                
                new_nav_content = nav_content
                # finditer helps us find positions
                occurrences = [m for m in rp_pattern.finditer(new_nav_content)]
                # we remove from the back to not mess up indices
                for match in reversed(occurrences[1:]):
                    new_nav_content = new_nav_content[:match.start()] + new_nav_content[match.end():]
                
                new_content = content[:nav_match.start(2)] + new_nav_content + content[nav_match.end(2):]
                
                with open(f, 'w', encoding='utf-8') as outfile:
                    outfile.write(new_content)
                fixed_count += 1
                print(f"Fixed duplicate in: {f}")
    
    print(f"Total files fixed: {fixed_count}")

if __name__ == '__main__':
    fix_duplicate_links()
