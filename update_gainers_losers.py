import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update Top Gainers
new_gainers = """<div class="snapshot-mover" id="home-gainers" style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span>MUCOBA <span style="color:var(--gain)">+3.6%</span></span>
                <span>PAL <span style="color:var(--gain)">+3.3%</span></span>
                <span>MBP <span style="color:var(--gain)">+2.9%</span></span>
  </div>"""

html = re.sub(
    r'<div class="snapshot-mover" id="home-gainers".*?</div>',
    new_gainers,
    html,
    flags=re.DOTALL
)

# Update Top Losers
new_losers = """<div class="snapshot-mover" id="home-losers" style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span>TTP <span style="color:var(--loss)">-2.3%</span></span>
                <span>TCC <span style="color:var(--loss)">-1.6%</span></span>
                <span>SWIS <span style="color:var(--loss)">-1.5%</span></span>
  </div>"""

html = re.sub(
    r'<div class="snapshot-mover" id="home-losers".*?</div>',
    new_losers,
    html,
    flags=re.DOTALL
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Gainers/Losers updated")
