import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_style = 'style="font-size: 0.8rem; border-radius: 6px; width: 90%; text-align: center; margin: 0 auto; display: block;"'
new_style = 'style="font-size: 0.85rem; font-weight: 600; border-radius: 8px; width: 95%; text-align: center; text-align-last: center; margin: 6px auto; display: block; background-color: #f4f9ff; color: #004aad; border: 1px solid #b3d4ff; padding: 6px 20px 6px 5px; box-shadow: 0 2px 6px rgba(0,74,173,0.08); cursor: pointer; appearance: none; -webkit-appearance: none; background-image: url(\'data:image/svg+xml;utf8,<svg fill=%22%23004aad%22 height=%2224%22 viewBox=%220 0 24 24%22 width=%2224%22 xmlns=%22http://www.w3.org/2000/svg%22><path d=%22M7 10l5 5 5-5z%22/><path d=%22M0 0h24v24H0z%22 fill=%22none%22/></svg>\'); background-repeat: no-repeat; background-position-x: 95%; background-position-y: 50%; outline: none; transition: all 0.2s ease;" onmouseover="this.style.borderColor=\'#004aad\'" onmouseout="this.style.borderColor=\'#b3d4ff\'"'

html = html.replace(old_style, new_style)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Dropdowns styled beautifully!")
