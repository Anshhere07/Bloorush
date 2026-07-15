import os

JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add initialization block at the very top for T&C and Firebase
init_block = """
// --- ARCHITECTURE UPGRADE: FIREBASE & T&C ---
const firebaseConfig = {
    // Developer Note: Replace this with your actual Firebase config!
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

let db = null;
try {
    if (firebaseConfig.apiKey !== "YOUR_API_KEY") {
        firebase.initializeApp(firebaseConfig);
        db = firebase.firestore();
        console.log("Firebase initialized successfully.");
    } else {
        console.warn("Firebase not configured. Using localStorage fallback mode.");
    }
} catch (e) {
    console.error("Firebase init failed:", e);
}

// Fallback DB wrappers
async function getFirestoreDoc(collection, docId) {
    if (db) {
        const doc = await db.collection(collection).doc(docId).get();
        return doc.exists ? doc.data() : null;
    } else {
        const data = JSON.parse(localStorage.getItem(`db_${collection}_${docId}`) || "null");
        return data;
    }
}
async function setFirestoreDoc(collection, docId, data) {
    if (db) {
        await db.collection(collection).doc(docId).set(data);
    } else {
        localStorage.setItem(`db_${collection}_${docId}`, JSON.stringify(data));
    }
}

// T&C Gate Logic
document.addEventListener("DOMContentLoaded", () => {
    if (!localStorage.getItem("bloorush_tc_accepted")) {
        $('#tcGateModal').modal('show');
    }
});

function acceptTC() {
    localStorage.setItem("bloorush_tc_accepted", "true");
    $('#tcGateModal').modal('hide');
}

"""

if "firebaseConfig" not in js:
    js = init_block + js


# 2. Add Admin Panel Logic
admin_logic = """
// --- ADMIN PANEL LOGIC ---
function promptAdminLogin(e) {
    e.preventDefault();
    const pwd = prompt("Enter Admin Password:");
    if (pwd === "BloorushAdmin2026") {
        document.body.innerHTML = ''; // Hide everything else for true client-side lock
        document.body.innerHTML = document.getElementById('adminPanelSection').outerHTML;
        document.getElementById('adminPanelSection').style.display = 'block';
    } else if (pwd !== null) {
        alert("Incorrect password.");
    }
}

function exitAdmin() {
    location.reload(); // Quick way to restore DOM
}

async function loadAdminSlots() {
    const date = document.getElementById('adminSlotDate').value;
    if(!date) return;
    const container = document.getElementById('adminSlotsContainer');
    
    // Default slots structure
    let slots = await getFirestoreDoc('slots', date) || {
        "10:00 AM - 12:00 PM": 2,
        "01:00 PM - 03:00 PM": 3,
        "04:00 PM - 06:00 PM": 1
    };
    
    let html = '';
    for(let time in slots) {
        html += `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span>${time}</span>
            <input type="number" class="form-control form-control-sm slot-capacity-input" data-time="${time}" value="${slots[time]}" style="width: 80px;">
        </div>`;
    }
    container.innerHTML = html;
}

async function saveAdminSlots() {
    const date = document.getElementById('adminSlotDate').value;
    if(!date) return alert("Select a date first.");
    
    const inputs = document.querySelectorAll('.slot-capacity-input');
    let data = {};
    inputs.forEach(inp => {
        data[inp.getAttribute('data-time')] = parseInt(inp.value);
    });
    
    await setFirestoreDoc('slots', date, data);
    alert("Slot capacity saved live!");
}

async function createCoupon() {
    const code = document.getElementById('newCouponCode').value.toUpperCase().trim();
    const discount = parseInt(document.getElementById('newCouponDiscount').value);
    
    if(!code || !discount) return alert("Please fill both fields.");
    
    await setFirestoreDoc('coupons', code, { discount: discount, active: true });
    alert(`Coupon ${code} created for ₹${discount}!`);
    document.getElementById('newCouponCode').value = '';
    document.getElementById('newCouponDiscount').value = '';
}
"""

if "promptAdminLogin" not in js:
    js += admin_logic


# 3. Add OSM Logic and Coupon logic
osm_coupon_logic = """
// --- OSM & COUPON LOGIC ---
let appliedCouponDiscount = 0;

async function searchOSMAddress() {
    const query = document.getElementById('osmAddressInput').value.trim();
    if(!query) return;
    
    const resBox = document.getElementById('osmResults');
    resBox.innerHTML = '<div class="p-2 text-muted">Searching...</div>';
    resBox.style.display = 'block';
    
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query + ', Nagpur')}`);
        const data = await response.json();
        
        if (data.length === 0) {
            resBox.innerHTML = '<div class="p-2 text-danger">No results found.</div>';
            return;
        }
        
        let html = '';
        data.slice(0, 5).forEach(place => {
            html += `<a href="#" class="list-group-item list-group-item-action py-2" onclick="selectOSMAddress('${place.display_name.replace(/'/g, "\\'")}')" style="font-size: 0.85rem;">${place.display_name}</a>`;
        });
        resBox.innerHTML = html;
    } catch(e) {
        resBox.innerHTML = '<div class="p-2 text-danger">Error fetching address.</div>';
    }
}

function selectOSMAddress(address) {
    document.getElementById('osmAddressInput').value = address;
    document.getElementById('osmResults').style.display = 'none';
}

async function applyCoupon() {
    const code = document.getElementById('couponInput').value.toUpperCase().trim();
    const msg = document.getElementById('couponMessage');
    
    if(!code) {
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "Please enter a code.";
        return;
    }
    
    const couponData = await getFirestoreDoc('coupons', code);
    
    if (couponData && couponData.active) {
        appliedCouponDiscount = couponData.discount;
        msg.style.display = 'block';
        msg.className = "form-text text-success";
        msg.innerText = `Coupon Applied! -₹${appliedCouponDiscount}`;
        refreshSlotTotal();
    } else {
        appliedCouponDiscount = 0;
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "Invalid or expired coupon.";
        refreshSlotTotal();
    }
}

function refreshSlotTotal() {
    let rawTotal = 0;
    for (let item in cart) rawTotal += cart[item].count * cart[item].price;
    
    let finalAmount = rawTotal;
    if (rawTotal >= 199) finalAmount -= 49; // existing special discount logic
    finalAmount -= appliedCouponDiscount;
    
    if(finalAmount < 0) finalAmount = 0;
    document.getElementById('slotModalTotalAmount').innerText = finalAmount;
}

// Hook into date change to fetch live slots
document.getElementById('bookingDate').addEventListener('change', async function() {
    const date = this.value;
    const container = document.getElementById('dynamicSlotsContainer');
    
    if(!date) return;
    
    // Fetch live slots
    let slots = await getFirestoreDoc('slots', date) || {
        "10:00 AM - 12:00 PM": 2,
        "01:00 PM - 03:00 PM": 3,
        "04:00 PM - 06:00 PM": 1
    };
    
    let html = '';
    for(let time in slots) {
        let capacity = slots[time];
        let isFull = capacity <= 0;
        let opacity = isFull ? '0.4' : '1';
        let ptr = isFull ? 'none' : 'auto';
        let label = isFull ? 'Full' : `${capacity} left`;
        
        html += `
        <div class="slot-item border rounded p-2 text-center" 
             style="cursor: pointer; opacity: ${opacity}; pointer-events: ${ptr}; flex: 1 1 30%; min-width: 100px; transition: 0.2s;"
             onclick="selectSlot(this)">
            <p class="mb-0 font-weight-bold" style="font-size: 0.85rem;">${time}</p>
            <small class="text-muted">${label}</small>
        </div>`;
    }
    
    if(container) {
        container.innerHTML = html;
    }
});
"""

if "searchOSMAddress" not in js:
    js += osm_coupon_logic


# Modify confirmWhatsAppBooking to use OSM Address if provided
wa_search = """if (document.getElementById('newAddressForm').style.display === 'block') {"""
wa_replace = """let osmAddr = document.getElementById('osmAddressInput') ? document.getElementById('osmAddressInput').value.trim() : '';
    if (osmAddr) {
        finalAddress = osmAddr;
    } else if (document.getElementById('newAddressForm').style.display === 'block') {"""

js = js.replace(wa_search, wa_replace)

# Modify confirmWhatsAppBooking to inject Coupon
coupon_wa_search = """if (originalTotal >= 199) {
        discountStr = "\\n*Discount:* -₹49";
        finalTotal -= 49;
    }"""
coupon_wa_replace = """if (originalTotal >= 199) {
        discountStr += "\\n*Special Discount:* -₹49";
        finalTotal -= 49;
    }
    if (typeof appliedCouponDiscount !== 'undefined' && appliedCouponDiscount > 0) {
        discountStr += `\\n*Coupon Discount:* -₹${appliedCouponDiscount}`;
        finalTotal -= appliedCouponDiscount;
    }"""

js = js.replace(coupon_wa_search, coupon_wa_replace)

# Reset appliedCouponDiscount when modal opens
open_modal_search = """document.getElementById('slotModalTotalAmount').innerText = totalAmount;"""
open_modal_replace = """appliedCouponDiscount = 0;
    if(document.getElementById('couponMessage')) document.getElementById('couponMessage').style.display = 'none';
    if(document.getElementById('couponInput')) document.getElementById('couponInput').value = '';
    
    document.getElementById('slotModalTotalAmount').innerText = totalAmount;"""
js = js.replace(open_modal_search, open_modal_replace)


with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print("JS Architecture Updated!")
