import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update checkLocation
new_check_location = """function checkLocation() {
    const input = document.getElementById('locationInput').value.trim().toLowerCase();
    const validLocations = ["nagpur", "narendra nagar", "manish nagar", "chhatrepathi square", "shahjahanpur"];
    
    // Check if input exists in validLocations array
    let isValid = false;
    for(let loc of validLocations) {
        if(input.includes(loc)) {
            isValid = true;
            break;
        }
    }

    if (isValid) {
        // Location Valid
        document.getElementById('locationSection').style.display = 'none';
        document.querySelector('.hero-section').style.display = 'block';
        if (document.querySelector('.offers-section')) document.querySelector('.offers-section').style.display = 'block';
        if (document.querySelector('.quick-book-section')) document.querySelector('.quick-book-section').style.display = 'block';
        if (document.querySelector('.services-section')) document.querySelector('.services-section').style.display = 'block';
        if (document.querySelector('.trusted-section')) document.querySelector('.trusted-section').style.display = 'block';
        if (document.querySelector('.why-section')) document.querySelector('.why-section').style.display = 'block';
        if (document.querySelector('.how-works-section')) document.querySelector('.how-works-section').style.display = 'block';
        
        document.querySelector('.bottom-nav').style.display = 'flex';
        
        currentUser.location = input;
        
    } else {
        // Location Invalid
        document.getElementById('locationSection').style.display = 'none';
        document.getElementById('noServiceSection').style.display = 'flex';
    }
}"""

# Using regex to replace the old checkLocation function
js = re.sub(r'function checkLocation\(\) \{.*?\n\}', new_check_location, js, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
    
print("Location updated.")
