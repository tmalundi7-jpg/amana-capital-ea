def update_js():
    with open('script.min.js', 'r', encoding='utf-8') as f:
        js = f.read()

    js_old = '''        const data = [
        { symbol: 'NMB', marketCap: 2675, change: 4.95 },
        { symbol: 'TBL', marketCap: 3200, change: 0.0 },
        { symbol: 'CRDB', marketCap: 1515, change: 2.2 },
        { symbol: 'VODA', marketCap: 1200, change: 1.9 },
        { symbol: 'TPCC', marketCap: 900, change: 0.7 },
        { symbol: 'NICO', marketCap: 700, change: -0.5 },
        { symbol: 'KCB', marketCap: 380, change: -0.9 },
        { symbol: 'TCCL', marketCap: 120, change: 0.0 },
        { symbol: 'TOL', marketCap: 85, change: 10.4 },
        { symbol: 'SWIS', marketCap: 100, change: 1.5 },
        { symbol: 'DCB', marketCap: 80, change: -2.0 },
        { symbol: 'MBP', marketCap: 65, change: 4.0 },
        { symbol: 'MCB', marketCap: 62, change: 0.0 },
        { symbol: 'NMG', marketCap: 50, change: 0.0 }
    ];'''

    js_new = '''        const data = [
        { symbol: 'NMB', marketCap: 2675, change: -0.5 },
        { symbol: 'TBL', marketCap: 3200, change: -0.1 },
        { symbol: 'CRDB', marketCap: 1515, change: 2.8 },
        { symbol: 'VODA', marketCap: 1200, change: 0.0 },
        { symbol: 'TPCC', marketCap: 900, change: -0.3 },
        { symbol: 'NICO', marketCap: 700, change: -2.1 },
        { symbol: 'KCB', marketCap: 380, change: 3.8 },
        { symbol: 'TCCL', marketCap: 120, change: -4.3 },
        { symbol: 'TOL', marketCap: 85, change: 5.7 },
        { symbol: 'SWIS', marketCap: 100, change: -1.5 },
        { symbol: 'DCB', marketCap: 80, change: 1.1 },
        { symbol: 'MBP', marketCap: 65, change: 3.4 },
        { symbol: 'MCB', marketCap: 62, change: 1.3 },
        { symbol: 'NMG', marketCap: 50, change: 0.0 }
    ];'''

    if js_old in js:
        js = js.replace(js_old, js_new)
        with open('script.min.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("script.min.js updated.")
    else:
        print("FAIL: JS old string not found")

update_js()
