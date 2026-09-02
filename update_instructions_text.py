with open('update_instructions.txt', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('added—', 'added and ')
c = c.replace('addedâ€”', 'added and ')
# also fix the replacement character if it exists
c = c.replace('added?"use', 'added and use')
c = c.replace('addeduse', 'added and use')

with open('update_instructions.txt', 'w', encoding='utf-8') as f:
    f.write(c)
print("Fixed update_instructions.txt")
