import os

files_to_fix = ['current-prices.html']

for filepath in files_to_fix:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace all legacy variables with hardcoded hex values
    text = text.replace('var(--navy)', '#0B1D3A')
    text = text.replace('var(--cream)', '#FBF7F0')
    text = text.replace('var(--mist)', '#9A9490')
    text = text.replace('var(--gold)', '#C8962E')
    text = text.replace('var(--stone)', '#E8E2D9')
    
    # We also want to revert the body style to default to let the site theme work, 
    # but hardcode the card colors so the container matches the legacy UI
    text = text.replace('<body style=\"background-color: #FBF7F0; color: #0A1628;\">', '<body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
