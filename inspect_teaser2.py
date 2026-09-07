import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = open('index.html', encoding='utf-8').read()

# Find the actual teaser content block
idx = c.find('Latest Research')
if idx == -1:
    idx = c.find("Today's DSE")
if idx == -1:
    idx = c.find('DSE Wrap')
    
print(f"Teaser block (at 'DSE Wrap'):")
print(c[max(0,idx-100):idx+1000])
print("\n---\n")

# Find 'Read the Full Wrap' button
idx2 = c.find('Read the Full Wrap')
if idx2 != -1:
    print("Read button context:")
    print(c[max(0,idx2-200):idx2+100])

c2 = open('market-intelligence.html', encoding='utf-8').read()
# Find the Daily DSE Wrap Archive / featured section
idx3 = c2.find('Daily DSE Wrap Archive')
if idx3 == -1:
    idx3 = c2.find('archive')
print(f"\nMI archive area:")
print(c2[max(0,idx3-50):idx3+800])
