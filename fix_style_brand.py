with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

missing_css = '''
.brand-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
}
.brand-icon {
    height: 36px;
    width: auto;
    color: #FFFFFF;
}
'''
if '.brand-link {' not in content:
    content = content.replace('.navbar { height: 64px; }', '.navbar { height: 64px; }\n' + missing_css)
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added brand-link to style.css")
