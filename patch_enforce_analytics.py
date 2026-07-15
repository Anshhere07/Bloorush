import re

JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Enforce phone number requirement in confirmWhatsAppBooking
enforce_search = """    let userPhoneNumber = document.getElementById('userPhone') ? document.getElementById('userPhone').value.trim() : '';
    let finalTotalVal = parseInt(document.getElementById('slotModalTotalAmount').innerText.replace(/,/g, '')) || 0;
"""

enforce_replace = """    let userPhoneNumber = document.getElementById('userPhone') ? document.getElementById('userPhone').value.trim() : '';
    
    // ENFORCE PHONE NUMBER
    if (!userPhoneNumber) {
        alert("Please enter your Phone Number before confirming.");
        return;
    }
    
    let finalTotalVal = parseInt(document.getElementById('slotModalTotalAmount').innerText.replace(/,/g, '')) || 0;
"""

if "ENFORCE PHONE NUMBER" not in js:
    js = js.replace(enforce_search, enforce_replace)

# 2. Modify recordAnalyticsAndUser to be ultra-resilient
analytics_search = """async function recordAnalyticsAndUser(name, phone, revenue) {
    if(!phone) return;
    // 1. Update Global Analytics
    const stats = await getFirestoreDoc('stats', 'global') || { revenue: 0, bookings: 0, coupons: 0 };
    stats.revenue += revenue;
    stats.bookings += 1;
    await setFirestoreDoc('stats', 'global', stats);
    
    // 2. Update User Database
    const users = await getFirestoreDoc('stats', 'users') || {};
    if (!users[phone]) {
        users[phone] = { name: name, totalBookings: 0, lastBooking: null };
    }
    users[phone].totalBookings += 1;
    users[phone].lastBooking = new Date().toISOString();
    await setFirestoreDoc('stats', 'users', users);
}"""

analytics_replace = """async function recordAnalyticsAndUser(name, phone, revenue) {
    if(!phone) phone = "Guest_" + Math.floor(Math.random()*10000);
    
    try {
        // 1. Update Global Analytics
        let stats = await getFirestoreDoc('stats', 'global') || { revenue: 0, bookings: 0, coupons: 0 };
        stats.revenue = (stats.revenue || 0) + revenue;
        stats.bookings = (stats.bookings || 0) + 1;
        await setFirestoreDoc('stats', 'global', stats);
        
        // 2. Update User Database
        let users = await getFirestoreDoc('stats', 'users') || {};
        if (!users[phone]) {
            users[phone] = { name: name || 'Guest', totalBookings: 0, lastBooking: null };
        }
        users[phone].totalBookings += 1;
        users[phone].lastBooking = new Date().toISOString();
        await setFirestoreDoc('stats', 'users', users);
        
        console.log("Analytics Successfully Saved!");
    } catch(e) {
        console.error("Failed to save analytics:", e);
    }
}"""

js = js.replace(analytics_search, analytics_replace)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print("JS Analytics enforcement patched!")
