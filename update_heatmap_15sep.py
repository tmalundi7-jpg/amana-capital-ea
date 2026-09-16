import re
import os
import json

os.chdir(r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea')

prices = {
  "AFRIPRISE": 0.0,
  "CRDB": -1.4,
  "DCB": -3.3,
  "DSE": -0.2,
  "JATU": 0.0,
  "KCB": 0.9,
  "MBP": -0.5,
  "MCB": -2.5,
  "MKCB": -0.8,
  "MUCOBA": 0.0,
  "NICO": -0.5,
  "NMB": 0.0,
  "PAL": 0.0,
  "SWIS": -1.1,
  "TBL": -0.2,
  "TCC": -1.0,
  "TCCL": 2.6,
  "TOL": 2.2,
  "TPCC": 0.0,
  "TTP": 1.2,
  "VODA": 3.6
}

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

hm_idx = text.find('const data = [')
hm_end = text.find('];', hm_idx)

if hm_idx != -1 and hm_end != -1:
    data_str = text[hm_idx:hm_end+2]
    new_data_str = data_str
    
    matches = re.finditer(r"\{\s*symbol:\s*'([^']+)',\s*marketCap:\s*([\d\.]+),\s*change:\s*([-\d\.]+)\s*\}", data_str)
    
    for m in matches:
        full_match = m.group(0)
        symbol = m.group(1)
        market_cap = m.group(2)
        
        if symbol in prices:
            new_change = prices[symbol]
            new_obj = f"{{ symbol: '{symbol}', marketCap: {market_cap}, change: {new_change} }}"
            new_data_str = new_data_str.replace(full_match, new_obj)
    
    text = text[:hm_idx] + new_data_str + text[hm_end+2:]
    
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated script.js successfully")
else:
    print("Could not find data array in script.js")
