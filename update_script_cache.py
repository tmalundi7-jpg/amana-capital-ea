import os

target_dir = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
script_path = os.path.join(target_dir, "script.js")
with open(script_path, 'r', encoding='utf-8') as f:
    script_content = f.read()

injection = """
    // --- CURRENCY PAGE CACHE BUSTING ---
    // Ensure links to the Currency page always fetch the latest version
    document.querySelectorAll('a[href*="/current-prices"]').forEach(link => {
        try {
            const url = new URL(link.href);
            url.searchParams.set('v', new Date().getTime());
            link.href = url.toString();
        } catch(e) {}
    });
"""

if "CURRENCY PAGE CACHE BUSTING" not in script_content:
    script_content = script_content.replace(
        "document.addEventListener('DOMContentLoaded', () => {", 
        "document.addEventListener('DOMContentLoaded', () => {\n" + injection
    )
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    script_min_path = os.path.join(target_dir, "script.min.js")
    with open(script_min_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
        
    print("script.js updated with cache busting.")
else:
    print("Already updated script.js.")
