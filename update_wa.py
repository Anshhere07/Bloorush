import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('onclick="scrollToCleaningMode()">BOOK\n                        NOW</button>', 'onclick="window.open(\'https://wa.me/917843021334\', \'_blank\')">BOOK\n                        NOW</button>')
html = html.replace('onclick="scrollToCleaningMode()">BOOK NOW</button>', 'onclick="window.open(\'https://wa.me/917843021334\', \'_blank\')">BOOK NOW</button>')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
