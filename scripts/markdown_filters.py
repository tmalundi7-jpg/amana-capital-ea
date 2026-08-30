import re

def extract_pullquote(content):
    pattern = r"{% pullquote %}(.*?){% endpullquote %}"
    match = re.search(pattern, content, re.DOTALL)
    if match: return match.group(1).strip()
    return None

def replace_pullquotes(content, template):
    pattern = r"{% pullquote %}(.*?){% endpullquote %}"
    def replacer(match):
        return f'''<blockquote class="pullquote"><span class="pullquote-icon">"</span><p class="pullquote-text">{match.group(1).strip()}</p><cite class="pullquote-cite">– Daily Market Wrap</cite></blockquote>'''
    return re.sub(pattern, replacer, content, flags=re.DOTALL)
