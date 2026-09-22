import re
with open('dse-wrap-2026-09-21.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the <p class="lead"...> block entirely.
# It starts at <p class="lead" and ends at </p>\n\n<p>The Dar
text = re.sub(r'<p class="lead" .*?</p>\n\n<p>The Dar', '<p>The Dar', text, flags=re.DOTALL)

with open('dse-wrap-2026-09-21.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed lead paragraph to exactly match 14 Sep structure.")
