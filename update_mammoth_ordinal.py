import re

with open('mammoth_html_wrap.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Add a function to get ordinal suffix
inject_ordinal = '''
def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        return str(n) + 'th'
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
'''
if 'def get_ordinal' not in c:
    c = inject_ordinal + c

# Replace the date_str line
old_date = "date_str = date_obj.strftime(f'%A, {date_obj.day} %B %Y')"
new_date = "date_str = date_obj.strftime(f'%A, {get_ordinal(date_obj.day)} %B %Y')"

if old_date in c:
    c = c.replace(old_date, new_date)
    with open('mammoth_html_wrap.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated mammoth script to use ordinal dates.")
else:
    print("Could not find date formatting string.")
