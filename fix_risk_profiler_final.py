import glob
import re

files = glob.glob('*.html')
fixed = 0
for f in files:
    if 'test_pdf' in f or '.bak' in f: continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to find nav block
    nav_match = re.search(r'(<ul[^>]*class="[^>]*nav-links[^>]*"[^>]*>)(.*?)(</ul>)', content, re.DOTALL)
    if nav_match:
        nav_content = nav_match.group(2)
        # find all Risk Profiler links
        matches = list(re.finditer(r'<li[^>]*>\s*<a href="/risk-profiler"[^>]*>.*?</a>\s*</li>', nav_content, re.DOTALL))
        if len(matches) > 1:
            # We have duplicates! Let's remove all but the first one.
            new_nav = nav_content
            for m in reversed(matches[1:]):
                new_nav = new_nav[:m.start()] + new_nav[m.end():]
            
            new_content = content[:nav_match.start(2)] + new_nav + content[nav_match.end(2):]
            with open(f, 'w', encoding='utf-8') as outfile:
                outfile.write(new_content)
            fixed += 1

print(f'Fixed duplicate nav in {fixed} files')
