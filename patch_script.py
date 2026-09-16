import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

add_functions = '''
window.initCacheBusting = function() {
    document.querySelectorAll('a[href*="/current-prices"]').forEach(link => {
        try {
            link.setAttribute('data-no-swup', 'true');
            const url = new URL(link.href, window.location.origin);
            url.searchParams.set('v', new Date().getTime());
            link.href = url.toString();
        } catch(e) {}
    });
};
'''

# Check if already patched
if 'window.initCacheBusting = function()' not in content:
    content = re.sub(
        r'// --- CURRENCY PAGE CACHE BUSTING ---.*?catch\(e\) \{\}\s*\}\);',
        'window.initCacheBusting();',
        content,
        flags=re.DOTALL
    )

    content += '\\n' + add_functions

    swup_hook_replacement = '''swup.hooks.on('page:view', () => {
            window.initCacheBusting();'''
    content = content.replace("swup.hooks.on('page:view', () => {", swup_hook_replacement)

    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    with open('script.min.js', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("script.js patched")
else:
    print("script.js already patched")
