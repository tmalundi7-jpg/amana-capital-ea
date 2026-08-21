import re

with open('dse-wrap-2026-08-14.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('temp_new_14_wrap.html', 'r', encoding='utf-8') as f:
    new_content = f.read()

prefix = content.split('<div class="card" style="padding: 3rem;">')[0] + '<div class="card" style="padding: 3rem;">\n'
suffix = '\n            </div>\n        </div>\n    </main>' + content.split('</main>')[1]

final_content = prefix + new_content + suffix

with open('dse-wrap-2026-08-14.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Done")
