import re
content = open('dse-wrap-2026-09-17.html', encoding='utf-8').read()
match = re.search(r'(</h1>)(.*?)(<div class="article-disclaimer")', content, re.DOTALL)
if match:
    print("Start of content in 17th:")
    print(repr(match.group(2)[:500]))
    print("...")
    print("End of content in 17th:")
    print(repr(match.group(2)[-500:]))
