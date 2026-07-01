import os
import re
from datetime import datetime

def update_market_intelligence_archive(repo_dir, new_date_str, new_title, new_subtitle, new_url):
    mi_path = os.path.join(repo_dir, "market-intelligence.html")
    with open(mi_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # If this date is already the first one, don't duplicate
    if new_date_str in html.split('<tbody>')[1][:200]:
        print("Date already at the top of the archive. Skipping insertion.")
        return

    # Find the tbody of the archive table and insert right after it
    tbody_start = html.find('<tbody>')
    if tbody_start == -1:
        print("Could not find tbody in market-intelligence.html")
        return
    
    tbody_end_idx = tbody_start + len('<tbody>')
    
    # We will determine the background color dynamically (alternate) in a real script,
    # but for simplicity, we just insert the new row with no background, 
    # and we can rely on CSS nth-child if we update the CSS, or just insert it.
    new_row = f'''
                                  <tr>
                                      <td style="width: 25%; font-weight: 600; color: var(--mist); font-size: 0.85rem; text-transform: uppercase;">{new_date_str}</td>
                                      <td><strong>{new_title}</strong><br><span style="font-size:0.85rem; color:#555;">{new_subtitle}</span></td>
                                      <td style="text-align: right;"><a href="{new_url}" class="gold-link">Read &rarr;</a></td>
                                  </tr>'''
    
    updated_html = html[:tbody_end_idx] + new_row + html[tbody_end_idx:]
    
    with open(mi_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("Archive updated successfully, previous records preserved.")

# Example Usage (when new data comes in):
# update_market_intelligence_archive('.', '2 July 2026', 'Market Rebound Continues', 'Brief subtitle here', '/dse-wrap-2026-07-02')
