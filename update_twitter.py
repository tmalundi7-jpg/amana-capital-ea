import os

contact_file = r'C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\contact.html'

with open(contact_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific Twitter placeholder
old_twitter_link = '<a href="#" class="ct-social-btn" aria-label="X / Twitter">'
new_twitter_link = '<a href="https://x.com/Theo_christian7" class="ct-social-btn" aria-label="X / Twitter" target="_blank" rel="noopener">'

if old_twitter_link in content:
    content = content.replace(old_twitter_link, new_twitter_link)
    
    with open(contact_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Twitter link updated successfully.")
else:
    print("Could not find the placeholder Twitter link in contact.html")
