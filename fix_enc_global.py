import os

def fix_file(f):
    try:
        c = open(f, 'r', encoding='utf-8').read()
    except:
        return
        
    c = c.replace('+"', '&rarr;')
    c = c.replace('+\'', '&rarr;')
    c = c.replace('?"', '&mdash;')
    c = c.replace('?T', '&rsquo;')
    c = c.replace('"?', '&#9642;') # square bullet
    
    open(f, 'w', encoding='utf-8').write(c)

fix_file('market-intelligence.html')
fix_file('market-intelligence-archive.html')
print("Fixed encoding globally")
