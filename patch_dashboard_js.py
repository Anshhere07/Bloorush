import os

JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Replace the old Admin & Coupon logic block
old_admin_search = """// --- ADMIN PANEL LOGIC ---"""
old_admin_end = """function refreshSlotTotal() {"""

# We need to slice the string safely or use regex
import re
pattern = re.compile(r'// --- ADMIN PANEL LOGIC ---.*?function refreshSlotTotal\(\) {', re.DOTALL)

new_admin_and_coupon = """// --- ADVANCED ADMIN & COUPON ENGINE ---
function promptAdminLogin(e) {
    e.preventDefault();
    const pwd = prompt("Enter Admin Password:");
    if (pwd === "BloorushAdmin2026") {
        document.body.innerHTML = ''; 
        document.body.innerHTML = document.getElementById('adminPanelSection').outerHTML;
        document.getElementById('adminPanelSection').style.display = 'block';
        
        // Load initial dashboard data
        loadAdminDashboard();
    } else if (pwd !== null) {
        alert("Incorrect password.");
    }
}

function exitAdmin() {
    location.reload(); 
}

async function loadAdminDashboard() {
    // Analytics
    const analytics = await getFirestoreDoc('stats', 'global') || { revenue: 0, bookings: 0, coupons: 0 };
    document.getElementById('statRevenue').innerText = analytics.revenue;
    document.getElementById('statBookings').innerText = analytics.bookings;
    document.getElementById('statCouponsUsed').innerText = analytics.coupons;
    
    // Users Table
    const users = await getFirestoreDoc('stats', 'users') || {};
    const tbody = document.getElementById('adminUsersTable');
    if (Object.keys(users).length > 0) {
        let html = '';
        for(let phone in users) {
            let u = users[phone];
            html += `<tr>
                <td>${u.name}</td>
                <td>${phone}</td>
                <td>${u.totalBookings}</td>
                <td>${new Date(u.lastBooking).toLocaleDateString()}</td>
            </tr>`;
        }
        tbody.innerHTML = html;
    }
    
    // Active Coupons
    loadAdminCoupons();
}

async function createAdvancedCoupon() {
    const code = document.getElementById('newCouponCode').value.toUpperCase().trim();
    const type = document.getElementById('newCouponType').value;
    const discount = parseInt(document.getElementById('newCouponDiscount').value);
    const expiry = document.getElementById('newCouponExpiry').value;
    const globalLimit = parseInt(document.getElementById('newCouponGlobalLimit').value) || 0;
    const userLimit = parseInt(document.getElementById('newCouponUserLimit').value) || 1;
    
    if(!code || !discount || !expiry) return alert("Please fill all fields.");
    
    const couponData = {
        code, type, discount, expiry, globalLimit, userLimit,
        usedCount: 0,
        active: true
    };
    
    await setFirestoreDoc('coupons', code, couponData);
    
    // Track in index of coupons
    let couponList = await getFirestoreDoc('stats', 'couponList') || { codes: [] };
    if(!couponList.codes.includes(code)) {
        couponList.codes.push(code);
        await setFirestoreDoc('stats', 'couponList', couponList);
    }
    
    alert(`Coupon ${code} created successfully!`);
    loadAdminCoupons();
}

async function loadAdminCoupons() {
    const container = document.getElementById('adminCouponsContainer');
    let couponList = await getFirestoreDoc('stats', 'couponList') || { codes: [] };
    
    if(couponList.codes.length === 0) {
        container.innerHTML = '<p class="text-muted">No active coupons.</p>';
        return;
    }
    
    let html = '<div class="list-group">';
    for(let code of couponList.codes) {
        let c = await getFirestoreDoc('coupons', code);
        if(!c) continue;
        let expired = new Date(c.expiry) < new Date() ? '<span class="badge badge-danger">Expired</span>' : '';
        let active = c.active ? '<span class="badge badge-success">Active</span>' : '<span class="badge badge-secondary">Disabled</span>';
        let val = c.type === 'flat' ? `₹${c.discount} OFF` : `${c.discount}% OFF`;
        
        html += `
        <div class="list-group-item d-flex justify-content-between align-items-center mb-2" style="border-radius: 8px;">
            <div>
                <h6 class="mb-1 font-weight-bold">${c.code} ${active} ${expired}</h6>
                <small class="text-muted">${val} | Expires: ${c.expiry} | Uses: ${c.usedCount} / ${c.globalLimit === 0 ? 'Unlimited' : c.globalLimit}</small>
            </div>
            <button class="btn btn-sm ${c.active ? 'btn-outline-danger' : 'btn-outline-success'}" onclick="toggleCoupon('${c.code}', ${!c.active})">
                ${c.active ? 'Disable' : 'Enable'}
            </button>
        </div>`;
    }
    html += '</div>';
    container.innerHTML = html;
}

async function toggleCoupon(code, status) {
    let c = await getFirestoreDoc('coupons', code);
    if(c) {
        c.active = status;
        await setFirestoreDoc('coupons', code, c);
        loadAdminCoupons();
    }
}

async function loadAdminSlots() {
    const date = document.getElementById('adminSlotDate').value;
    if(!date) return;
    const container = document.getElementById('adminSlotsContainer');
    
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

// --- PUBLIC COUPON ENGINE ---
let appliedCouponDiscount = 0;
let appliedCouponCode = "";

async function fetchPublicCoupons() {
    const container = document.getElementById('publicCouponsList');
    const wrapper = document.getElementById('availableOffersContainer');
    let couponList = await getFirestoreDoc('stats', 'couponList') || { codes: [] };
    
    let activeCoupons = [];
    for(let code of couponList.codes) {
        let c = await getFirestoreDoc('coupons', code);
        if(c && c.active && new Date(c.expiry) >= new Date() && (c.globalLimit === 0 || c.usedCount < c.globalLimit)) {
            activeCoupons.push(c);
        }
    }
    
    if(activeCoupons.length === 0) {
        wrapper.style.display = 'none';
        return;
    }
    
    wrapper.style.display = 'block';
    let html = '';
    activeCoupons.forEach(c => {
        let text = c.type === 'flat' ? `₹${c.discount} OFF` : `${c.discount}% OFF`;
        html += `
        <div class="border border-primary rounded p-2 text-center" style="min-width: 120px; cursor: pointer; background: #eef7ff;" onclick="document.getElementById('couponInput').value = '${c.code}'; applyCoupon();">
            <div class="font-weight-bold text-primary" style="font-size: 0.9rem;">${c.code}</div>
            <small class="text-muted">${text}</small>
        </div>`;
    });
    container.innerHTML = html;
}

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
    const userPhone = document.getElementById('userPhone').value.trim(); // We need a phone to check per-user limits, assuming userPhone exists
    
    if(!code) {
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "Please enter a code.";
        return;
    }
    
    const c = await getFirestoreDoc('coupons', code);
    
    if (!c || !c.active) {
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "Invalid or expired coupon.";
        resetCoupon();
        return;
    }
    
    if (new Date(c.expiry) < new Date()) {
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "This coupon has expired.";
        resetCoupon();
        return;
    }
    
    if (c.globalLimit > 0 && c.usedCount >= c.globalLimit) {
        msg.style.display = 'block';
        msg.className = "form-text text-danger";
        msg.innerText = "Coupon usage limit reached.";
        resetCoupon();
        return;
    }
    
    // Check per user limit if phone is provided
    if (userPhone) {
        const userUsage = await getFirestoreDoc('coupon_usage', `${code}_${userPhone}`) || { count: 0 };
        if (userUsage.count >= c.userLimit) {
            msg.style.display = 'block';
            msg.className = "form-text text-danger";
            msg.innerText = "You have reached the usage limit for this coupon.";
            resetCoupon();
            return;
        }
    }
    
    // Calculate discount
    let rawTotal = 0;
    for (let item in cart) rawTotal += cart[item].count * cart[item].price;
    
    appliedCouponDiscount = c.type === 'flat' ? c.discount : (rawTotal * (c.discount / 100));
    appliedCouponCode = c.code;
    
    msg.style.display = 'block';
    msg.className = "form-text text-success";
    msg.innerText = `Coupon Applied! -₹${appliedCouponDiscount.toFixed(0)}`;
    refreshSlotTotal();
}

function resetCoupon() {
    appliedCouponDiscount = 0;
    appliedCouponCode = "";
    refreshSlotTotal();
}

function refreshSlotTotal() {"""

js = pattern.sub(new_admin_and_coupon, js)

# Inject data tracking before whatsapp
wa_search = """let msg = `Hi, I am ${document.getElementById('userName').value}, this is my first booking request:\\n\\n`;"""
wa_replace = """// -- LOG ANALYTICS & USER DATA --
    recordAnalyticsAndUser(document.getElementById('userName').value, document.getElementById('userPhone').value, finalTotal);
    if (typeof appliedCouponCode !== 'undefined' && appliedCouponCode !== "") {
        recordCouponUsage(appliedCouponCode, document.getElementById('userPhone').value);
    }
    
    let msg = `Hi, I am ${document.getElementById('userName').value}, this is my first booking request:\\n\\n`;"""

js = js.replace(wa_search, wa_replace)

# Function to record tracking
analytics_func = """
// --- DATA TRACKING FUNCTIONS ---
async function recordAnalyticsAndUser(name, phone, revenue) {
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
}

async function recordCouponUsage(code, phone) {
    // Increment global coupon usage
    const c = await getFirestoreDoc('coupons', code);
    if(c) {
        c.usedCount += 1;
        await setFirestoreDoc('coupons', code, c);
    }
    
    // Increment global stats
    const stats = await getFirestoreDoc('stats', 'global') || { revenue: 0, bookings: 0, coupons: 0 };
    stats.coupons += 1;
    await setFirestoreDoc('stats', 'global', stats);
    
    // Record per-user usage
    if(phone) {
        const userUsage = await getFirestoreDoc('coupon_usage', `${code}_${phone}`) || { count: 0 };
        userUsage.count += 1;
        await setFirestoreDoc('coupon_usage', `${code}_${phone}`, userUsage);
    }
}
"""
js += analytics_func


# Trigger fetchPublicCoupons when slot modal opens
open_modal_search = """appliedCouponDiscount = 0;"""
open_modal_replace = """fetchPublicCoupons();
    appliedCouponDiscount = 0;"""
js = js.replace(open_modal_search, open_modal_replace)


with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print("JS Advanced Architecture injected successfully!")
