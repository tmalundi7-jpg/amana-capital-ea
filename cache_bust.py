import glob

for filename in glob.glob('*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'script.min.js?v=20260830' in c or 'script.min.js?v=20260904' in c:
        # Replace old version strings
        c = c.replace('script.min.js?v=20260830_final_polish_27', 'script.min.js?v=20260907_heatmap_fix')
        c = c.replace('script.min.js?v=20260904_heatmap', 'script.min.js?v=20260907_heatmap_fix')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(c)

print("Cache bust complete.")
