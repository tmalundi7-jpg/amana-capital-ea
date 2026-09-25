import re

# We will read both script files and replace the change values in the data array.
# Let's map the new change values
changes = {
    'AFRIPRISE': 0.6,
    'CRDB': 2.4,
    'DCB': -4.5,
    'DSE': 0.5,
    'KCB': 0.0,
    'MBP': 2.9,
    'MCB': -1.3,
    'MKCB': 1.4,
    'MUCOBA': 11.1,
    'NICO': -3.5,
    'NMB': 0.0,
    'PAL': 0.0,
    'SWIS': 1.2,
    'TBL': 0.0,
    'TCC': 0.2,
    'TCCL': -2.8,
    'TOL': 1.1,
    'TPCC': 1.8,
    'TTP': 0.0,
    'VODA': -0.8
}

def update_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # The data array looks like: {symbol:'NMB',marketCap:2675,change:0.5}
    def replacer(match):
        symbol = match.group(1)
        marketCap = match.group(2)
        if symbol in changes:
            return f"{{symbol:'{symbol}',marketCap:{marketCap},change:{changes[symbol]}}}"
        return match.group(0)

    # Use regex to find and replace all instances
    pattern = r"\{symbol:'([^']+)',marketCap:([0-9.]+),change:[0-9.-]+\}"
    new_content = re.sub(pattern, replacer, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filename}")

update_script('script.js')
update_script('script.min.js')
