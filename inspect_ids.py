import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('index.html', encoding='utf-8').read()
ids = re.findall(r'id="((?:home|teaser|snapshot|terminal)-[^"]+)"', c)
print("=== index.html relevant IDs ===")
for i in sorted(set(ids)):
    # print actual value
    m = re.search(rf'id="{re.escape(i)}"[^>]*>([^<]*)<', c)
    val = m.group(1).strip() if m else "???"
    print(f"  {i!r:50s} => {val!r}")

c2 = open('market-intelligence.html', encoding='utf-8').read()
ids2 = re.findall(r'id="((?:mi)-[^"]+)"', c2)
print("\n=== market-intelligence.html relevant IDs ===")
for i in sorted(set(ids2)):
    m = re.search(rf'id="{re.escape(i)}"[^>]*>([^<]*)<', c2)
    val = m.group(1).strip() if m else "???"
    print(f"  {i!r:50s} => {val!r}")
