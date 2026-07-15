import re

JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update fetchPublicCoupons to show "No coupons available"
fetch_coupons_old = """    if(activeCoupons.length === 0) {
        wrapper.style.display = 'none';
        return;
    }"""
fetch_coupons_new = """    wrapper.style.display = 'block';
    if(activeCoupons.length === 0) {
        container.innerHTML = '<div class="text-muted text-center w-100 p-2"><small>No coupons available.</small></div>';
        return;
    }"""
js = js.replace(fetch_coupons_old, fetch_coupons_new)

# 2. Update Admin Dashboard load to render charts and CRUD buttons
admin_load_old = """async function loadAdminDashboard() {
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
}"""

admin_load_new = """async function loadAdminDashboard() {
    // Analytics
    const analytics = await getFirestoreDoc('stats', 'global') || { revenue: 0, bookings: 0, coupons: 0 };
    document.getElementById('statRevenue').innerText = analytics.revenue;
    document.getElementById('statBookings').innerText = analytics.bookings;
    document.getElementById('statCouponsUsed').innerText = analytics.coupons;
    
    // Render Charts
    renderAdminCharts(analytics);
    
    // Users Table
    loadAdminUsers();
    
    // Active Coupons
    loadAdminCoupons();
}

let revenueChartInstance = null;
let bookingsChartInstance = null;

function renderAdminCharts(analytics) {
    if(typeof Chart === 'undefined') return;
    
    // Mock historical data leading up to current totals
    const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today'];
    const revData = [0, 0, 0, 0, 0, 0, analytics.revenue];
    const bkgData = [0, 0, 0, 0, 0, 0, analytics.coupons];
    
    const revCtx = document.getElementById('revenueChart');
    if(revenueChartInstance) revenueChartInstance.destroy();
    if(revCtx) {
        revenueChartInstance = new Chart(revCtx, {
            type: 'line',
            data: { labels, datasets: [{ label: 'Revenue (₹)', data: revData, borderColor: '#38b6ff', tension: 0.3, fill: true, backgroundColor: 'rgba(56, 182, 255, 0.1)' }] },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
    
    const bkgCtx = document.getElementById('bookingsChart');
    if(bookingsChartInstance) bookingsChartInstance.destroy();
    if(bkgCtx) {
        bookingsChartInstance = new Chart(bkgCtx, {
            type: 'bar',
            data: { labels, datasets: [{ label: 'Coupons Redeemed', data: bkgData, backgroundColor: '#ffc107' }] },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
}

async function loadAdminUsers() {
    const users = await getFirestoreDoc('stats', 'users') || {};
    const tbody = document.getElementById('adminUsersTable');
    if (Object.keys(users).length > 0) {
        let html = '';
        for(let phone in users) {
            let u = users[phone];
            let nameEscaped = u.name ? u.name.replace(/'/g, "\\'") : 'Unknown';
            html += `<tr>
                <td>${u.name}</td>
                <td>${phone}</td>
                <td>${u.totalBookings}</td>
                <td>${u.lastBooking ? new Date(u.lastBooking).toLocaleDateString() : 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="openAdminEditUser('${phone}', '${nameEscaped}', ${u.totalBookings})"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteAdminUser('${phone}')"><i class="fas fa-trash"></i></button>
                </td>
            </tr>`;
        }
        tbody.innerHTML = html;
    } else {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No users found.</td></tr>';
    }
}

function openAdminEditUser(phone, name, bookings) {
    document.getElementById('editUserPhone').value = phone;
    document.getElementById('editUserName').value = name;
    document.getElementById('editUserBookings').value = bookings;
    $('#adminEditUserModal').modal('show');
}

async function saveAdminUserEdit() {
    const phone = document.getElementById('editUserPhone').value;
    const name = document.getElementById('editUserName').value;
    const bookings = parseInt(document.getElementById('editUserBookings').value) || 0;
    
    const users = await getFirestoreDoc('stats', 'users') || {};
    if(users[phone]) {
        users[phone].name = name;
        users[phone].totalBookings = bookings;
        await setFirestoreDoc('stats', 'users', users);
        $('#adminEditUserModal').modal('hide');
        loadAdminUsers(); // refresh
    }
}

async function deleteAdminUser(phone) {
    if(confirm("Are you sure you want to delete user " + phone + "?")) {
        const users = await getFirestoreDoc('stats', 'users') || {};
        if(users[phone]) {
            delete users[phone];
            await setFirestoreDoc('stats', 'users', users);
            loadAdminUsers();
        }
    }
}
"""
js = js.replace(admin_load_old, admin_load_new)

# Update users table headers in HTML (Ah I already modified HTML, I should add Action header via python)
# Wait, I can do it here in the python script.
with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

import os
html_path = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    h = f.read()

h = h.replace('<th>Last Booking</th>', '<th>Last Booking</th><th>Actions</th>')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(h)

print("JS CRUD and Chart injected successfully!")
