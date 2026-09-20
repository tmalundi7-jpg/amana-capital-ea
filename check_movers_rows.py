content = open('dse-wrap-2026-09-18.html', encoding='utf-8').read()
import re
print("Top Movers rows:", content.count('<strong style="color: #000;">', content.find('Top Movers'), content.find('AFRIPRISE</strong> was the standout')))
