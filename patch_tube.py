import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the old absolute pills
pill_html = '<div style="position:absolute; top:-8px; left:50%; transform:translateX(-50%); background:linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); color:#d81b60; font-size:10px; padding:3px 10px; border-radius:12px; font-weight:800; white-space:nowrap; z-index:10; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">Coming Soon</div>'
html = html.replace(pill_html, '')

# 2. Insert the tube above Fan
tube_html = """
                        <!-- Coming soon tube -->
                        <div style="grid-column: 1 / -1; background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); color: #d81b60; text-align: center; padding: 10px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; margin: 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            Coming Soon: Fan cleaning and Windows cleaning will be coming soon!
                        </div>
                        <!-- Item 5 -->"""

# Replace the Item 5 comment with the tube + comment
html = html.replace('<!-- Item 5 -->', tube_html)

# Also bump script.js?v=5 to v=6 just to force a hard cache clear in case CSS is stuck
html = html.replace('script.js?v=5', 'script.js?v=6')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Tube added.")
