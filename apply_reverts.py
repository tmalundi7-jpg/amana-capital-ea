import re

with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

css_patch = """
/* Governing Principles Update */
.why-section {
    background-color: var(--cream) !important;
}
.why-section .section-title, 
.why-section .section-eyebrow, 
.why-section p {
    color: var(--navy) !important;
    text-align: left !important;
}
.why-card {
    background-color: var(--cream) !important;
    border: 1px solid var(--gold) !important;
    color: var(--navy) !important;
    box-shadow: 0 4px 15px rgba(200, 150, 46, 0.15) !important;
}
.why-card h3 {
    color: var(--navy) !important;
}
.why-card p {
    color: var(--text-primary) !important;
}
.why-icon {
    background: rgba(200, 150, 46, 0.15) !important;
}

/* Ensure Daily DSE Wrap reverts to previous styling */
.teaser-premium {
    background: var(--navy) !important;
    border-top: 3px solid var(--gold) !important;
    box-shadow: 0 10px 40px rgba(11,29,58,0.15) !important;
    border-radius: 12px !important;
}
.teaser-prem-left, .teaser-prem-right {
    text-align: left !important;
}
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css + css_patch
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('temp_revert/index.old.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

old_teaser_match = re.search(r'(<section class="home-teaser">.*?</section>)', old_html, re.DOTALL)
current_teaser_match = re.search(r'(<section class="home-teaser">.*?</section>)', current_html, re.DOTALL)

if old_teaser_match and current_teaser_match:
    old_teaser = old_teaser_match.group(1)
    current_html = current_html.replace(current_teaser_match.group(1), old_teaser)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(current_html)
    print('Replaced home-teaser with old version.')
else:
    print('Could not find home-teaser section.')
