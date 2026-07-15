import re

HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the broken img logo with a heading in the T&C Modal
tc_logo_search = r'<img src="assets/images/logo\.png" alt="Bloorush Logo" style="max-height: 50px;">'
tc_logo_replace = '<h2 class="font-weight-bold text-primary mb-0">Bloorush</h2>'

if 'alt="Bloorush Logo"' in html:
    html = re.sub(tc_logo_search, tc_logo_replace, html)

# Also let's do a bump to version 17
html = re.sub(r'script\.js\?v=\d+', 'script.js?v=17', html)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("T&C Modal logo replaced with heading!")
