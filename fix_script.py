with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

if "window.initCacheBusting();" not in content[:500]:
    content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "document.addEventListener('DOMContentLoaded', () => {\\n    window.initCacheBusting();")

    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(content)
        
    with open('script.min.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("script.js patched for DOMContentLoaded")
