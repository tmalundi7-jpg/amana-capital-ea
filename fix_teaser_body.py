import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_teaser_body = "The DSE has entered a new era. Local capital is firmly in control as CRDB hits a post-split high of 2,940, pushing the DSEI to 4,682.13 while bond turnover contracts for the third consecutive session."

html = re.sub(r'<p class="teaser-prem-body">.*?</p>', f'<p class="teaser-prem-body">{new_teaser_body}</p>', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated teaser body")
