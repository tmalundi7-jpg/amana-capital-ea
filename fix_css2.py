import re

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

# Strip out everything from /* --- BBC/Economist Instant: No Fade, No Slide --- */
# to the end of that section
c = re.sub(r'/\* ---.*?(Economist Instant|Smooth Page Transitions).*?(?=\n\/\*|\Z)', '', c, flags=re.DOTALL|re.IGNORECASE)

# Append the correct Swup CSS
css_replace = '''
/* --- Smooth Page Transitions --- */
.transition-fade {
  transition: 0.25s opacity ease-out;
  opacity: 1;
}
html.is-animating .transition-fade {
  opacity: 0;
}
'''
c += css_replace

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

with open('style.min.css', 'w', encoding='utf-8') as f:
    f.write(c)

print("CSS transitions cleanly injected.")
