import re

with open('script.min.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the marketData array values for the 14 stocks.
# Since the array order is hardcoded or relies on specific change values, we can parse and replace them.
# The tickers and changes for 18th are:
# AFRIPRISE: 8.8, VODA: 1.6, KCB: 0.5
# SWIS: 0, TCC: 0, TCCL: 0, TPCC: 0
# CRDB: -1.1, NMB: -1.0, TOL: -1.1, DSE: -1.7, PAL: -7.7, DCB: -1.1, TBL: -0.5

replacements = {
    'AFRIPRISE': 8.8, 'VODA': 1.6, 'KCB': 0.5,
    'SWIS': 0.0, 'TCC': 0.0, 'TCCL': 0.0, 'TPCC': 0.0,
    'CRDB': -1.1, 'NMB': -1.0, 'TOL': -1.1, 'DSE': -1.7, 'PAL': -7.7, 'DCB': -1.1, 'TBL': -0.5
}

def replacer(match):
    ticker = match.group(1)
    if ticker in replacements:
        return f'symbol:"{ticker}",change:{replacements[ticker]}'
    return match.group(0)

new_content = re.sub(r'symbol:"([^"]+)",change:([-\d\.]+)', replacer, content)

with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated script.min.js")
