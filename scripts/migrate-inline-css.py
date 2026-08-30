#!/usr/bin/env python3
import re, os, sys

STYLE_MAP = {
    'margin-top: 2rem': 'mt-8', 'margin-top: 1.5rem': 'mt-6', 'margin-top: 1rem': 'mt-4',
    'margin-bottom: 2rem': 'mb-8', 'margin-bottom: 1.5rem': 'mb-6', 'margin-bottom: 1rem': 'mb-4',
    'padding: 1.5rem': 'p-6', 'padding: 1rem': 'p-4', 'padding: 0.75rem': 'p-3',
    'display: flex': 'd-flex', 'display: inline-flex': 'd-inline-flex',
    'flex-direction: column': 'flex-column', 'align-items: center': 'align-center',
    'justify-content: center': 'justify-center',
    'gap: 1rem': 'gap-4', 'gap: 0.75rem': 'gap-3', 'gap: 0.5rem': 'gap-2',
    'text-align: center': 'text-center',
    'color: #0a1628': 'text-navy', 'color: #e5b13b': 'text-gold',
}

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    matches = re.finditer(r'style="([^"]*)"', content)
    issues = []
    for match in matches:
        style_attr = match.group(1)
        for css_prop, utility_class in STYLE_MAP.items():
            if css_prop in style_attr:
                issues.append({'line': content[:match.start()].count('\n') + 1, 'style': style_attr, 'suggested': utility_class})
    return issues

def main():
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                issues = scan_file(filepath)
                if issues:
                    print(f"\n📄 {filepath}")
                    for issue in issues: print(f"  Line {issue['line']}: style=\"{issue['style']}\" \n    → Replace with: class=\"{issue['suggested']}\"")

if __name__ == '__main__': main()
