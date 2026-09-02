for f in ['market-intelligence.html', 'market-intelligence-archive.html']:
    c = open(f, 'r', encoding='utf-8').read()
    c = c.replace("+'", "&rarr;")
    c = c.replace("?\"", "&mdash;")
    c = c.replace("?T", "&rsquo;")
    c = c.replace("?\"", "&mdash;")
    c = c.replace("?T", "&rsquo;")
    open(f, 'w', encoding='utf-8').write(c)
