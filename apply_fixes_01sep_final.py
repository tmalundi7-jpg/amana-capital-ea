import re

# 1. Read the raw HTML output
with open('dse-wrap-2026-09-01.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 2. Fix missing spaces around links
c = c.replace('read<a', 'read <a')
c = c.replace('</a>and<a', '</a> and <a')
c = c.replace('</em>A<a', '</em> <a')
c = c.replace('</em><a', '</em> <a')
c = c.replace('<strong>A', '<strong>')
c = c.replace('</strong>A', '</strong> ')
c = c.replace('bond:</strong>ATZS', 'bond:</strong> TZS')
c = c.replace('bond:</strong>TZS', 'bond:</strong> TZS')
c = c.replace('<strong>NMB</strong>Ais', '<strong>NMB</strong> is')
c = c.replace('<strong>NMB</strong>is', '<strong>NMB</strong> is')
c = c.replace('<strong>CRDB</strong>Ais', '<strong>CRDB</strong> is')
c = c.replace('<strong>CRDB</strong>is', '<strong>CRDB</strong> is')
c = c.replace('<strong>VODA</strong>Ahas', '<strong>VODA</strong> has')
c = c.replace('<strong>VODA</strong>has', '<strong>VODA</strong> has')
c = c.replace('<strong>Bond yields</strong>Aare', '<strong>Bond yields</strong> are')
c = c.replace('<strong>Bond yields</strong>are', '<strong>Bond yields</strong> are')
c = c.replace('series.</strong>AIf', 'series.</strong> If')
c = c.replace('series.</strong>If', 'series.</strong> If')
c = c.replace('signals.</strong>AWhen', 'signals.</strong> When')
c = c.replace('signals.</strong>When', 'signals.</strong> When')
c = c.replace('bands.</strong>AThey', 'bands.</strong> They')
c = c.replace('bands.</strong>They', 'bands.</strong> They')
c = c.replace('volatility.</strong>ANMB', 'volatility.</strong> NMB')
c = c.replace('volatility.</strong>NMB', 'volatility.</strong> NMB')
c = c.replace('last.</strong>AThe', 'last.</strong> The')
c = c.replace('last.</strong>The', 'last.</strong> The')
c = c.replace('days.</strong>ADaily', 'days.</strong> Daily')
c = c.replace('days.</strong>Daily', 'days.</strong> Daily')
c = c.replace('risk.</strong>ANever', 'risk.</strong> Never')
c = c.replace('risk.</strong>Never', 'risk.</strong> Never')
c = c.replace('neutral ?" buying', 'neutral &mdash; buying')
c = c.replace('compressing ?" falling', 'compressing &mdash; falling')
c = c.replace('two weeks ?" the', 'two weeks &mdash; the')
c = c.replace('flow reversal ?" all', 'flow reversal &mdash; all')
c = c.replace('opportunities are there ?" in', 'opportunities are there &mdash; in')

# Also fix the weird left arrow from the template
c = c.replace('+? Back', '&larr; Back')
c = c.replace('\xe2\x86\x90 Back', '&larr; Back')

# 3. Apply the Considerations styling
# Use str.split to safely wrap the last section
split_marker = '<h2 style="color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h2>'

if split_marker in c:
    parts = c.split(split_marker)
    before_7 = parts[0]
    after_7 = parts[1]
    
    # Check if there is an extra disclaimer inside after_7
    after_7 = re.sub(r'<p><em>For general informational.*?</em></p>\s*(?=<div class="article-disclaimer")', '', after_7, flags=re.DOTALL)
    
    # We also don't want the actual main disclaimer to be inside the cream box.
    # The template puts `<div class="article-disclaimer"` at the end.
    if '<div class="article-disclaimer"' in after_7:
        sub_parts = after_7.split('<div class="article-disclaimer"')
        considerations_text = sub_parts[0]
        disclaimer_html = '<div class="article-disclaimer"' + sub_parts[1]
        
        # Build the final html
        new_header = '<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem; margin-bottom: 1.5rem;">7. Considerations for a Multi-Year Framework</h3>'
        wrapped_7 = f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{new_header}{considerations_text}\n</div>\n{disclaimer_html}'
        
        c = before_7 + wrapped_7
        print("Successfully wrapped section 7!")
    else:
        print("Could not find article-disclaimer in after_7")
else:
    print("Could not find section 7 marker!")

with open('dse-wrap-2026-09-01.html', 'w', encoding='utf-8') as f:
    f.write(c)
