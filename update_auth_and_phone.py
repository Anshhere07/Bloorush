import re

# Update index.html
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace phone number
html = html.replace('8010687985', '7843021334')

# Remove Google Auth Button
google_btn_pattern = r'<!-- Google Auth Button \(UI\) -->\s*<button class="btn btn-block google-btn shadow-sm mb-4">.*?</button>\s*<div class="divider text-center mb-4">\s*<span class="text-muted">OR</span>\s*</div>'
html = re.sub(google_btn_pattern, '', html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Update script.js
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace phone number
js = js.replace('8010687985', '7843021334')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Phone number updated and Google login button removed successfully.")
