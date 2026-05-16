import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace pink colors. 
# #e91e63 is standard pink. #c2185b is dark pink. #fce4ec is very light pink (might be rgb).
html = html.replace('#e91e63', '#38b6ff')
html = html.replace('#c2185b', '#004aad') 
html = html.replace('#fce4ec', '#f0f7ff') # light pink to light blue
html = html.replace('#d81b60', '#38b6ff')

# Also sometimes pink is passed as background: pink or something. Let's see if there are any literal "pink" strings.
# But replacing literal "pink" might break things if not careful. The user specifically asked for "#38b6ff".

# Replace social links
html = html.replace('<a href="#"><i class="fab fa-instagram"></i></a>', '<a href="https://www.instagram.com/trybloorush?igsh=MTBldTNpdnZsNnM2Zw==" target="_blank"><i class="fab fa-instagram"></i></a>')
html = html.replace('<a href="#"><i class="fab fa-linkedin-in"></i></a>', '<a href="https://www.linkedin.com/company/bloorush/" target="_blank"><i class="fab fa-linkedin-in"></i></a>')
html = html.replace('<a href="#"><i class="fab fa-facebook-f"></i></a>', '<a href="https://www.facebook.com/share/1CX8hoigkz/" target="_blank"><i class="fab fa-facebook-f"></i></a>')

# Twitter reload
html = html.replace('<a href="#"><i class="fab fa-twitter"></i></a>', '<a href="#" onclick="location.reload(); return false;"><i class="fab fa-twitter"></i></a>')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Colors and links updated successfully!")
