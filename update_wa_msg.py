import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the whatsapp window.open with the new function call
html = html.replace('onclick="window.open(\'https://wa.me/917843021334\', \'_blank\')">BOOK\n                        NOW</button>', 'onclick="bookFirstOrderOffer()">BOOK\n                        NOW</button>')
html = html.replace('onclick="window.open(\'https://wa.me/917843021334\', \'_blank\')">BOOK NOW</button>', 'onclick="bookFirstOrderOffer()">BOOK NOW</button>')

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_func = """
function bookFirstOrderOffer() {
    let userName = "";
    
    // Attempt to get user name from currentUser variable or localStorage
    try {
        if (typeof currentUser !== 'undefined' && currentUser && currentUser.name) {
            userName = currentUser.name;
        } else {
            const localUser = JSON.parse(localStorage.getItem('bloorush_currentUser'));
            if(localUser && localUser.name) {
                userName = localUser.name;
            }
        }
    } catch(e) {}
    
    let message = "";
    if (userName) {
        message = `Hi, I am ${userName}. This is my first booking Service. I would like to avail the ₹49 First Order offer!`;
    } else {
        message = `Hi! This is my first booking Service. I would like to avail the ₹49 First Order offer!`;
    }
    
    const encodedMessage = encodeURIComponent(message);
    window.open(`https://wa.me/917843021334?text=${encodedMessage}`, '_blank');
}
"""

if "function bookFirstOrderOffer" not in js:
    js = js + new_func

# Also bump version again
html = html.replace('script.js?v=4', 'script.js?v=5')
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("WhatsApp Message script added!")
