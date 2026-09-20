import json
content = open('17_main_full.txt', encoding='utf-8').read()
# Let's write a python script to generate the 18th content based on the structure of 17th
# But first we need to inspect the tables
with open('temp_tables.txt', 'w', encoding='utf-8') as f:
    f.write(content)
