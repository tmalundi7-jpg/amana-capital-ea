new_tbody = """<tbody>
<tr><td class="ticker-cell">AFRIPRISE</td><td>African Pride</td><td>Commercial Services</td><td class="price-cell">615</td><td class="change-neutral">0.0%</td><td>303,615</td><td>187,405,115</td></tr>
<tr><td class="ticker-cell">CRDB</td><td>CRDB Bank</td><td>Banks & Finance</td><td class="price-cell">2,730</td><td class="change-positive">+1.9%</td><td>1,662,418</td><td>4,478,817,980</td></tr>
<tr><td class="ticker-cell">DCB</td><td>Dar es Salaam Community Bank</td><td>Banks & Finance</td><td class="price-cell">490</td><td class="change-positive">+2.1%</td><td>349,999</td><td>171,241,310</td></tr>
<tr><td class="ticker-cell">DSE</td><td>Dar es Salaam Stock Exchange</td><td>Commercial Services</td><td class="price-cell">6,410</td><td class="change-negative">–1.4%</td><td>2,754</td><td>17,668,470</td></tr>
<tr><td class="ticker-cell">KCB</td><td>KCB Group (cross-listed)</td><td>Banks & Finance</td><td class="price-cell">2,220</td><td class="change-positive">+3.7%</td><td>40,534</td><td>89,883,200</td></tr>
<tr><td class="ticker-cell">MBP</td><td>Maendeleo Bank</td><td>Banks & Finance</td><td class="price-cell">2,010</td><td class="change-positive">+1.5%</td><td>4,819</td><td>9,698,880</td></tr>
<tr><td class="ticker-cell">MCB</td><td>Mwanga Community Bank</td><td>Banks & Finance</td><td class="price-cell">400</td><td class="change-positive">+2.6%</td><td>201,179</td><td>80,780,320</td></tr>
<tr><td class="ticker-cell">MKCB</td><td>Mkamba Commercial Bank</td><td>Banks & Finance</td><td class="price-cell">3,700</td><td class="change-positive">+0.3%</td><td>2,809</td><td>10,409,660</td></tr>
<tr><td class="ticker-cell">NICO</td><td>NICO Holdings</td><td>Banks & Finance</td><td class="price-cell">4,030</td><td class="change-negative">–1.2%</td><td>22,301</td><td>89,982,610</td></tr>
<tr><td class="ticker-cell">NMB</td><td>NMB Bank</td><td>Banks & Finance</td><td class="price-cell">2,020</td><td class="change-positive">+3.6%</td><td>1,194,103</td><td>2,314,855,340</td></tr>
<tr><td class="ticker-cell">NMG</td><td>Nation Media Group (cross-listed)</td><td>Commercial Services</td><td class="price-cell">340</td><td class="change-neutral">0.0%</td><td>110</td><td>33,000</td></tr>
<tr><td class="ticker-cell">PAL</td><td>Pal Holdings</td><td>Industrials</td><td class="price-cell">305</td><td class="change-neutral">0.0%</td><td>15,611</td><td>4,761,355</td></tr>
<tr><td class="ticker-cell">SWIS</td><td>Swissport Tanzania</td><td>Commercial Services</td><td class="price-cell">2,660</td><td class="change-negative">–0.4%</td><td>2,935</td><td>7,823,020</td></tr>
<tr><td class="ticker-cell">TBL</td><td>Tanzania Breweries</td><td>Industrials</td><td class="price-cell">10,000</td><td class="change-positive">+0.9%</td><td>1,635</td><td>16,351,400</td></tr>
<tr><td class="ticker-cell">TCC</td><td>Tanga Cement</td><td>Industrials</td><td class="price-cell">12,600</td><td class="change-positive">+0.3%</td><td>17,236</td><td>217,203,400</td></tr>
<tr><td class="ticker-cell">TCCL</td><td>Tanzania Cigarette Company</td><td>Industrials</td><td class="price-cell">3,600</td><td class="change-positive">+0.8%</td><td>30,631</td><td>110,235,600</td></tr>
<tr><td class="ticker-cell">TOL</td><td>TOL Gases</td><td>Industrials</td><td class="price-cell">1,830</td><td class="change-negative">–0.5%</td><td>10,680</td><td>19,534,200</td></tr>
<tr><td class="ticker-cell">TPCC</td><td>Tanga Portland Cement</td><td>Industrials</td><td class="price-cell">5,760</td><td class="change-negative">–0.2%</td><td>8,640</td><td>49,764,100</td></tr>
<tr><td class="ticker-cell">TTP</td><td>Tatepa Public Limited Company</td><td>Commercial Services</td><td class="price-cell">475</td><td class="change-positive">+1.1%</td><td>577</td><td>273,960</td></tr>
<tr><td class="ticker-cell">VODA</td><td>Vodacom Tanzania</td><td>Commercial Services</td><td class="price-cell">1,050</td><td class="change-negative">–1.9%</td><td>283,522</td><td>299,002,890</td></tr>
</tbody>"""

import re

with open('current-prices.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<tbody>.*?</tbody>', new_tbody, c, flags=re.DOTALL)
c = c.replace('End-of-Day, Thursday, 3rd September 2026', 'End-of-Day, Friday, 4th September 2026')

with open('current-prices.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("current-prices.html updated successfully.")
