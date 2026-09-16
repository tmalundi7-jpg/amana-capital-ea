import os
import glob
import re

def run():
    target_dir = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
    
    # 1. READ INDEX.HTML AND EXTRACT HEADER
    index_path = os.path.join(target_dir, "index.html")
    with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    nav_match = re.search(r'(<nav class="navbar">.*?</nav>)', content, re.DOTALL)
    if not nav_match:
        print("Could not find nav in index.html")
        exit(1)
        
    canonical_nav = nav_match.group(1)
    
    # Remove active class from the canonical nav so we have a clean slate
    # E.g. <a class="active" href="/"> -> <a href="/">
    canonical_nav = re.sub(r'\s*class="active"\s*', ' ', canonical_nav)
    # clean up any extra spaces
    canonical_nav = canonical_nav.replace(' <a ', '<a ').replace('" >', '">')
    
    # Ensure current-prices link in the nav has a cache buster if it exists
    # Wait, current-prices isn't in the main nav in index.html!
    
    html_files = glob.glob(os.path.join(target_dir, "*.html"))
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
        
        # Extract active href from existing nav
        old_nav_match = re.search(r'<nav\s+class="[^"]*navbar[^"]*".*?</nav>', file_content, flags=re.DOTALL)
        active_href = None
        if old_nav_match:
            old_nav = old_nav_match.group(0)
            active_m = re.search(r'<a[^>]*class="[^"]*active[^"]*"[^>]*href="([^"]+)"', old_nav)
            if active_m:
                active_href = active_m.group(1)
        
        # If not found in HTML, try to guess
        if not active_href:
            fn = os.path.basename(filepath)
            if fn == "index.html":
                active_href = "/"
            elif "market-intelligence" in fn or "article" in fn or "dse-wrap" in fn:
                active_href = "/market-intelligence"
            elif "education" in fn or "investing" in fn:
                active_href = "/education"
            elif "bond-calculator" in fn:
                active_href = "/bond-calculator"
            elif "risk-profiler" in fn:
                active_href = "/risk-profiler"
            elif "about" in fn:
                active_href = "/about"
            elif "contact" in fn:
                active_href = "/contact"
            else:
                active_href = "/"
                
        # Inject active class into canonical nav
        new_nav = canonical_nav
        if active_href:
            # We want to replace <a href="active_href"> with <a class="active" href="active_href">
            # But the canonical nav might not have it exactly like that.
            pattern = r'(<a\s+href="' + re.escape(active_href) + r'")'
            new_nav = re.sub(pattern, r'\1 class="active"', new_nav)
            
        # Replace the nav in the file
        new_content = file_content
        if old_nav_match:
            new_content = new_content[:old_nav_match.start()] + new_nav + new_content[old_nav_match.end():]
        
        # Cache busting for Currency page
        # Replace ALL links to /current-prices to /current-prices?v=nocache
        new_content = re.sub(r'href="/current-prices(\.html)?"', r'href="/current-prices?v=latest"', new_content)
        
        if os.path.basename(filepath) == 'current-prices.html':
            if '<meta http-equiv="Cache-Control"' not in new_content:
                meta_tags = """<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0" />\n<meta http-equiv="Pragma" content="no-cache" />\n<meta http-equiv="Expires" content="0" />\n"""
                new_content = new_content.replace('<head>', '<head>\n' + meta_tags)

        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    print("Fixed headers in all HTML files.")

    # 3. UPDATE README.md
    readme_path = os.path.join(target_dir, "README.md")
    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
        readme_content = f.read()

    guardrail_note = """
## 🔒 GUARDRAILS (DO NOT MODIFY)
- **HEADER LOCK**: The `<nav class="navbar">` header is LOCKED and must remain identical across all pages (same text, fonts, colors, spacing, etc.). It must NOT be changed unless explicitly requested by the site owner.
- **CURRENCY PAGE LOCK**: The Currency page (`current-prices.html`) must always serve the latest content on first load. Cache-busting is enforced via query strings on links (`?v=latest`) and meta cache-control tags in the HTML. Any future update must not reintroduce a stale-content or refresh-required behaviour. Future content updates must inherit these settings automatically.
"""
    if "GUARDRAILS" not in readme_content:
        readme_content += "\n" + guardrail_note
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    print("README.md updated with guardrails.")

if __name__ == "__main__":
    run()
