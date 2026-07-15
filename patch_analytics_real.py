import re

JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# The injection target:
wa_search = r"(const message = `Hello Bloorush!)"

wa_replace = """// -- LOG ANALYTICS & USER DATA --
    let userPhoneNumber = document.getElementById('userPhone') ? document.getElementById('userPhone').value.trim() : '';
    let finalTotalVal = parseInt(document.getElementById('slotModalTotalAmount').innerText.replace(/,/g, '')) || 0;
    let uName = typeof currentUser !== 'undefined' && currentUser.name ? currentUser.name : (document.getElementById('userName') ? document.getElementById('userName').value : 'Guest');
    
    if(typeof recordAnalyticsAndUser === 'function') {
        recordAnalyticsAndUser(uName, userPhoneNumber, finalTotalVal);
    }
    if (typeof appliedCouponCode !== 'undefined' && appliedCouponCode !== "") {
        if(typeof recordCouponUsage === 'function') {
            recordCouponUsage(appliedCouponCode, userPhoneNumber);
        }
    }

    \\1"""

# Use regex to insert right before const message
js = re.sub(wa_search, wa_replace, js)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print("JS Analytics correctly patched inside confirmWhatsAppBooking!")
