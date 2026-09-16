import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make the body background cream
text = text.replace('<body>', '<body style=\"background-color: #FBF7F0; color: #0A1628;\">')

# Make the header cream and text dark
text = text.replace('background-color: #0B1D3A; text-align: center;', 'background-color: #FBF7F0; text-align: center;')
text = text.replace('<h1 style=\"color: #FBF7F0;', '<h1 style=\"color: #0A1628;')

# Make the footer cream and text dark
text = text.replace('background-color: #0B1D3A; padding: 3rem 0 2rem; border-top: 1px solid rgba(255,255,255,0.05);', 'background-color: #FBF7F0; padding: 3rem 0 2rem; border-top: 1px solid rgba(0,0,0,0.05);')
text = text.replace('color: rgba(251,247,240,0.5);', 'color: rgba(10, 22, 40, 0.6);')
text = text.replace('color: var(--mist);', 'color: rgba(10, 22, 40, 0.6);')

text = re.sub(r'style\.css\?v=[a-zA-Z0-9_]+', 'style.css?v=20260912_cream_fix', text)

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(text)
