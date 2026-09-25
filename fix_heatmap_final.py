import re

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

def update_js_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        js = f.read()

    for ticker, change in changes.items():
        pattern = r"(\{symbol:'" + ticker + r"',marketCap:\d+,change:)[^\}]+(\})"
        js = re.sub(pattern, r"\g<1>" + str(change) + r"\g<2>", js)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js)

update_js_file('script.js')
update_js_file('script.min.js')
print("Heatmap updated")
