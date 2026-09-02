import re
import io

# 1. Read the raw HTML output
with open('dse-wrap-2026-09-01.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 2. Fix missing spaces around links (if they got stripped or mangled)
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

# Also fix the weird left arrow from the template if it got mangled
c = c.replace('+? Back', '&larr; Back')
c = c.replace('\xe2\x86\x90 Back', '&larr; Back')

# 3. Apply the Considerations styling
# We want to match EXACTLY `<h2... >7. Considerations...</h2>` and the following text.
# The `(?=<div class="article-disclaimer")` or `(?=<p><em>For general)` is a good boundary.
def repl(m):
    h2_tag = m.group(1)
    text = m.group(2)
    # Convert the h2 to h3
    h3_tag = h2_tag.replace('<h2', '<h3').replace('2.5rem;', '0; font-size: 1.4rem;')
    
    return f'<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">\n{h3_tag}7. Considerations for a Multi-Year Framework</h3>{text}\n</div>'

c = re.sub(r'(<h2.*?>)7\. Considerations for a Multi-Year Framework</h2>(.*?)(?=<div class="article-disclaimer"|<p><em>For general informational)', repl, c, flags=re.DOTALL)

# 4. Remove the extra mammoth disclaimer if it exists BEFORE the actual disclaimer block
c = re.sub(r'<p><em>For general informational.*?</em></p>\s*(?=<div class="article-disclaimer")', '', c, flags=re.DOTALL)

with open('dse-wrap-2026-09-01.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied fixes to dse-wrap-2026-09-01.html")
