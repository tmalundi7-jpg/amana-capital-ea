with open('script.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Add Swup initialization
swup_init = '''
/* --- Swup Initialization --- */
document.addEventListener('DOMContentLoaded', () => {
    if (typeof Swup !== 'undefined') {
        const swup = new Swup({
            containers: ['#swup'],
            plugins: [
                new SwupScriptsPlugin({
                    head: true,
                    body: true
                })
            ]
        });

        swup.hooks.on('page:view', () => {
            // Re-init specific features if necessary
            if (typeof window.initDSEHeatmap === 'function') {
                window.initDSEHeatmap();
            }
            if (typeof Weglot !== 'undefined') {
                Weglot.initialize({ api_key: 'wg_22a6f434974df4dee513e25f34fc5e009' });
            }
        });
    }
});
'''

# If not already in there, append it
if 'new Swup' not in c:
    c += '\n' + swup_init

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(c)
with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Swup initialized in script.js")
