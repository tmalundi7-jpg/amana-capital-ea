with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

import re
css_replace = '''/* --- Smooth Page Transitions --- */
.transition-fade {
  transition: opacity 0.25s ease-out;
  opacity: 1;
}
html.is-animating .transition-fade {
  opacity: 0;
}'''

# Replace the block that forces no transitions
c = re.sub(r'/\* ---.*?Economist Instant.*?html\.is-changing \.transition-main \{.*?\}', css_replace, c, flags=re.DOTALL)
# Also just in case, let's just search and replace
c = re.sub(r'/\* ---.*?Economist Instant.*?animation: none !important;\n\}', css_replace, c, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

with open('style.min.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated CSS")
