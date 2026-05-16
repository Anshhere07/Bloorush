import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add ID to Cleaning Mode section wrapper
html = html.replace('<div class="services-main-card px-3" style="background: transparent; box-shadow: none;">', '<div id="cleaningModeSection" class="services-main-card px-3" style="background: transparent; box-shadow: none;">')

# 2. Add onclick to BOOK NOW buttons
html = html.replace('<button class="btn btn-dark" style="border-radius: 20px; font-weight: bold; padding: 5px 20px;">BOOK\n                        NOW</button>', '<button class="btn btn-dark" style="border-radius: 20px; font-weight: bold; padding: 5px 20px;" onclick="scrollToCleaningMode()">BOOK\n                        NOW</button>')
html = html.replace('<button class="btn btn-dark" style="border-radius: 20px; font-weight: bold; padding: 5px 20px;">BOOK NOW</button>', '<button class="btn btn-dark" style="border-radius: 20px; font-weight: bold; padding: 5px 20px;" onclick="scrollToCleaningMode()">BOOK NOW</button>')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_func = """function scrollToCleaningMode() {
    if(document.getElementById('homeView').style.display === 'none') {
        const homeNavBtn = document.querySelector('.bottom-nav-item[onclick*="homeView"]');
        switchTab('homeView', homeNavBtn);
    }
    
    setTimeout(() => {
        const section = document.getElementById('cleaningModeSection');
        if(section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 100);
}
"""

if "function scrollToCleaningMode" not in js:
    js = js + "\n\n" + new_func

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("BOOK NOW functionality added!")
