import re

with open('dse-wrap-2026-09-14.html', 'r', encoding='utf-8') as f:
    text14 = f.read()

with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    text21 = f.read()

# Get the exact layout from 14 Sep for the disclaimer
# It goes from the closing </div> of section 7, to the end of the </main> tag.
# Actually, let's just grab from <p style="font-size: 0.85rem; color: var(--mist); up to </main>
disc14_match = re.search(r'<p style="font-size: 0.85rem; color: var\(--mist\).*?</main>', text14, re.DOTALL)
disc14 = disc14_match.group(0)

# Replace the end of 21 Sep
# It starts at <div class="article-disclaimer" up to </main>
# But wait, in 21 Sep there's an extra </div> before the disclaimer.
# Let's find Section 7 in 21 Sep:
sec7_end = text21.find('market\'s natural rhythm do the heavy lifting.</p>\n</div>')
if sec7_end != -1:
    # the end of the section 7 div is at sec7_end + len(...)
    cut_point = sec7_end + len('market\'s natural rhythm do the heavy lifting.</p>\n</div>')
    
    # from cut_point to </main>, replace with disc14
    main_end = text21.find('</main>', cut_point) + len('</main>')
    
    text21_new = text21[:cut_point] + '\n' + disc14 + text21[main_end:]
    
    with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
        f.write(text21_new)
    print('Perfectly matched the layout of the end of the article.')
else:
    print('Could not find Section 7 end in 21 Sep.')
