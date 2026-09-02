with open('dse-wrap-2026-09-02.html', 'r', encoding='utf-8') as f:
    c = f.read()

bad_chars = set()
for char in c:
    if ord(char) > 127:
        bad_chars.add(char)

print("Bad chars:")
for bc in bad_chars:
    print(repr(bc), ord(bc))
