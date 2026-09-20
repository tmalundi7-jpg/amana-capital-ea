content = open('rebuild_18_perfect_final.py', 'r', encoding='utf-8').read()
content = content.replace(".replace('', '&minus;')", "")
with open('rebuild_18_perfect_final2.py', 'w', encoding='utf-8') as f:
    f.write(content)
