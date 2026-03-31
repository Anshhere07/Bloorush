// Reload
function reloadPage() {
    location.reload();
}

// LOCATION (IMPORTANT FIX)
function getLocation() {
    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async function (position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById("locationText").innerText = "Fetching...";

            try {
                // Using OpenStreetMap Nominatim API for reverse geocoding (No API key required)
                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&accept-language=en`);
                const data = await response.json();

                // Extract city, town, village, or state from the response
                const city = data.address.city || data.address.town || data.address.village || data.address.state_district || data.address.state || "Unknown Location";

                document.getElementById("locationText").innerText = city;
                localStorage.setItem("bloorush_userLocation", city);
            } catch (error) {
                console.error("Error fetching location details:", error);
                document.getElementById("locationText").innerText = "Location Error";
            }
        },
        function (error) {
            alert("Please allow location access");
        }
    );
}

// OPEN LOGIN
function openLogin(e) {
    e.preventDefault();
    isLoginMode = true; // Reset state when opening modal
    updateAuthUI();
    $('#loginModal').modal('show');
}

// OPEN BOOKINGS (TABULAR UI)
function openBookings(e) {
    if (e) e.preventDefault();

    const body = document.getElementById('bookingModalBody');
    body.innerHTML = ''; // Clear previous content

    if (userBookings && userBookings.length > 0) {
        // --- HAS DATA SCENARIO ---
        let htmlContent = `
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                    <tr>
                        <th class="border-0">Booking ID</th>
                        <th class="border-0">Date</th>
                        <th class="border-0">Amount Paid</th>
                        <th class="border-0 text-center">Receipt</th>
                    </tr>
                </thead>
                <tbody>
        `;

        userBookings.forEach(booking => {
            htmlContent += `
                <tr>
                    <td class="font-weight-bold" style="color:var(--primary);">${booking.id}</td>
                    <td class="text-muted">${booking.date}</td>
                    <td class="font-weight-bold">₹${booking.total}</td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-primary shadow-sm" style="border-radius:6px;" onclick="viewBill('${booking.id}')">
                            <i class="fas fa-file-invoice mr-1"></i> View Bill
                        </button>
                    </td>
                </tr>
            `;
        });

        htmlContent += '</tbody></table></div>';
        body.innerHTML = htmlContent;
    } else {
        // --- NO DATA SCENARIO (Empty State) ---
        body.innerHTML = `
            <div class="text-center py-5">
                <div class="mb-4" style="background: var(--primary-light); width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                    <i class="fas fa-calendar-times" style="font-size: 45px; color: var(--primary);"></i>
                </div>
                <h5 class="font-weight-bold text-dark">No Past Bookings</h5>
                <p class="text-muted">Looks like you haven't made any bookings yet on Bloorush.</p>
                <button class="btn btn-primary mt-3 px-4 shadow-sm" style="border-radius: 8px;" data-dismiss="modal" onclick="document.querySelector('.services-section').scrollIntoView({ behavior: 'smooth' });">Browse Services</button>
            </div>
        `;
    }

    $('#bookingModal').modal('show');
}

function viewBill(bookingId) {
    const booking = userBookings.find(b => b.id === bookingId);
    if (booking) {
        $('#bookingModal').modal('hide');

        // Repopulate specific receipt DOM
        document.getElementById('receiptBookingId').innerText = booking.id;
        document.getElementById('receiptCustomerName').innerText = currentUser ? currentUser.name : 'Bloorush Customer';
        document.getElementById('receiptTotalAmount').innerText = booking.total;

        const itemsListHtml = booking.items.map(item => `
            <div class="receipt-item d-flex justify-content-between mb-2">
                <span>${item.name} (x${item.count})</span>
                <span class="font-weight-bold" style="color:#2c3e50;">₹${item.price * item.count}</span>
            </div>
        `).join('');
        document.getElementById('receiptItemsList').innerHTML = itemsListHtml;

        $('#successModal').modal('show');
    }
}

const GOOGLE_SHEET_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbyIUoCRGDJwtbueJf-MfMFc9_TGeihNlPK2ay-d_ed4EwjmI6IYyOivXN10CWs5juRXfQ/exec";

async function logActivityToSheet(name, email, activityType) {
    if (GOOGLE_SHEET_WEBAPP_URL === "YOUR_SCRIPT_URL_HERE") {
        console.warn("Google Sheet Web App URL not configured. Activity not logged.");
        return;
    }

    try {
        const url = new URL(GOOGLE_SHEET_WEBAPP_URL);
        url.searchParams.append("name", name || "Unknown");
        url.searchParams.append("email", email || "Unknown");
        url.searchParams.append("action", activityType);
        url.searchParams.append("timestamp", new Date().toISOString());

        await fetch(url, {
            method: 'GET',
            mode: 'no-cors' // Crucial to prevent CORS preflight blocks from a static frontend!
        });
        console.log("Activity logged to Google Sheets via webhook.");
    } catch (e) {
        console.error("Failed to log activity to Google sheet", e);
    }
}

// AUTH MODAL LOGIC & SESSION PERSISTENCE
let isLoginMode = true;
let currentUser = JSON.parse(localStorage.getItem('bloorush_currentUser')); // Persistent global session
let userBookings = JSON.parse(localStorage.getItem('bloorush_userBookings')) || []; // Persistent total booking history

// Fire initial startup logic to set correct views
document.addEventListener("DOMContentLoaded", () => {
    updateNavbarUI();
    updateCheckoutUI();

    // Attempt to restore persistent location securely
    const savedLocation = localStorage.getItem("bloorush_userLocation");
    if (savedLocation) {
        document.getElementById("locationText").innerText = savedLocation;
    }
});

function updateNavbarUI() {
    const links = document.getElementById('navbarAuthLinks');
    if (links) {
        if (currentUser) {
            links.innerHTML = `
                <a class="dropdown-item" href="#" onclick="openBookings(event)"><i class="fas fa-history mr-2" style="color:var(--primary);"></i>My Bookings</a>
                <a class="dropdown-item text-danger" href="#" onclick="logoutUser(event)"><i class="fas fa-sign-out-alt mr-2"></i>Logout</a>
            `;
        } else {
            links.innerHTML = `
                <a class="dropdown-item" href="#" onclick="openLogin(event)"><i class="fas fa-sign-in-alt mr-2" style="color:var(--primary);"></i>Login / Register</a>
            `;
        }
    }
}

function logoutUser(e) {
    if (e) e.preventDefault();
    localStorage.removeItem('bloorush_currentUser');
    location.reload();
}

function updateCheckoutUI() {
    if (currentUser) {
        if (document.getElementById('checkoutLoginState')) document.getElementById('checkoutLoginState').style.display = 'none';
        if (document.getElementById('checkoutLoggedState')) {
            document.getElementById('checkoutLoggedState').style.display = 'block';
            document.getElementById('checkoutUserName').innerText = currentUser.name;
        }
    } else {
        if (document.getElementById('checkoutLoggedState')) document.getElementById('checkoutLoggedState').style.display = 'none';
        if (document.getElementById('checkoutLoginState')) document.getElementById('checkoutLoginState').style.display = 'block';
    }
}

document.getElementById('toggleAuthMode').addEventListener('click', function (e) {
    e.preventDefault();
    isLoginMode = !isLoginMode;
    updateAuthUI();
});

function updateAuthUI() {
    const title = document.getElementById('authTitle');
    const subtitle = document.getElementById('authSubtitle');
    const submitBtn = document.getElementById('authSubmitBtn');
    const footerText = document.getElementById('authFooterText');
    const toggleBtn = document.getElementById('toggleAuthMode');
    const nameField = document.querySelector('.signup-field');
    const googleBtnText = document.getElementById('googleBtnText');

    if (isLoginMode) {
        title.innerText = "Welcome Back";
        subtitle.innerText = "Login to continue";
        submitBtn.innerText = "Login";
        footerText.innerText = "Don't have an account?";
        toggleBtn.innerText = "Sign Up";
        nameField.style.display = "none";
        googleBtnText.innerText = "Sign in with Google";
    } else {
        title.innerText = "Create Account";
        subtitle.innerText = "Join Bloorush today";
        submitBtn.innerText = "Sign Up";
        footerText.innerText = "Already have an account?";
        toggleBtn.innerText = "Login";
        nameField.style.display = "flex";
        googleBtnText.innerText = "Sign up with Google";
    }
}

// MOCK LOCAL DATABASE (FOR DEMO PURPOSES)
const DB_KEY = "bloorush_users";

function getUsers() {
    return JSON.parse(localStorage.getItem(DB_KEY) || "[]");
}

function saveUser(user) {
    const users = getUsers();
    users.push(user);
    localStorage.setItem(DB_KEY, JSON.stringify(users));
}

function showToast(title, message, isSuccess = true) {
    const toastEl = $('#authToast');
    document.getElementById('toastTitle').innerText = title;
    document.getElementById('toastBody').innerText = message;

    if (isSuccess) {
        document.getElementById('toastTitle').style.color = "var(--primary)";
    } else {
        document.getElementById('toastTitle').style.color = "red";
    }

    toastEl.toast('show');
}

// HANDLE FORM SUBMISSION (LOGIN / SIGNUP)
document.getElementById('authSubmitBtn').addEventListener('click', function (e) {
    e.preventDefault();

    const nameField = document.querySelector('.signup-field input').value.trim();
    const emailField = document.querySelector('input[type="email"]').value.trim();
    const passwordField = document.querySelector('input[type="password"]').value.trim();

    if (!emailField || !passwordField) {
        showToast("Error", "Email and Password are required!", false);
        return;
    }

    if (isLoginMode) {
        // Login Mode
        const users = getUsers();
        const user = users.find(u => u.email === emailField && u.password === passwordField);

        if (user) {
            currentUser = { name: user.name, email: user.email };
            localStorage.setItem('bloorush_currentUser', JSON.stringify(currentUser));
            updateNavbarUI();
            updateCheckoutUI();

            showToast("Success", "Successfully logged in! Welcome back, " + user.name, true);
            logActivityToSheet(user.name, user.email, "Logged In via Email");
            $('#loginModal').modal('hide');
        } else {
            showToast("Login Failed", "Invalid credentials. Please try again.", false);
        }
    } else {
        // Sign Up Mode
        if (!nameField) {
            showToast("Error", "Full Name is required for signup!", false);
            return;
        }

        const users = getUsers();
        if (users.find(u => u.email === emailField)) {
            showToast("Error", "An account with this email already exists!", false);
            return;
        }

        saveUser({ name: nameField, email: emailField, password: passwordField });

        // Auto-login the user immediately upon sign-up for seamless checkout
        currentUser = { name: nameField, email: emailField };
        localStorage.setItem('bloorush_currentUser', JSON.stringify(currentUser));
        updateNavbarUI();
        updateCheckoutUI();

        showToast("Success", "Successfully signed up and logged in!", true);
        logActivityToSheet(nameField, emailField, "Signed Up via Email");
        $('#loginModal').modal('hide');
    }
});

// GOOGLE AUTHENTICATION (OAUTH2)
const GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com"; // User must replace this!
let tokenClient;

window.onload = function () {
    // Initialize Google Token Client for custom button once script loads
    if (typeof google !== 'undefined' && google.accounts) {
        initGoogleClient();
    } else {
        // Wait and try again if GIS is loaded asynchronously
        setTimeout(() => {
            if (typeof google !== 'undefined' && google.accounts) {
                initGoogleClient();
            }
        }, 1000);
    }
};

function initGoogleClient() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_CLIENT_ID,
        scope: 'email profile',
        callback: (tokenResponse) => {
            if (tokenResponse && tokenResponse.access_token) {
                fetchGoogleUserProfile(tokenResponse.access_token);
            }
        },
    });
}

document.querySelector('.google-btn').addEventListener('click', function (e) {
    e.preventDefault();
    if (GOOGLE_CLIENT_ID === "YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com") {
        alert("Developer Note:\n\nYou must replace 'YOUR_GOOGLE_CLIENT_ID_HERE' in script.js with your actual Google OAuth Client ID to test the real login!");
        return;
    }

    if (tokenClient) {
        // Triggers the Google Login Popup
        tokenClient.requestAccessToken();
    } else {
        alert("Google Identity Services not loaded yet. Please try again.");
    }
});

function fetchGoogleUserProfile(accessToken) {
    // Fetch user details like email and name from Google
    fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
        headers: { Authorization: `Bearer ${accessToken}` }
    })
        .then(res => res.json())
        .then(userInfo => {
            console.log("Google User Info:", userInfo);

            // Set session state and update DOM securely
            currentUser = { name: userInfo.name, email: userInfo.email };
            updateCheckoutUI();

            alert(`Successfully logged in as: ${userInfo.name}\nEmail: ${userInfo.email}`);
            logActivityToSheet(userInfo.name, userInfo.email, "Logged In via Google");

            // Hide Modal on success
            $('#loginModal').modal('hide');
        })
        .catch(err => {
            console.error("Error fetching Google profile:", err);
            alert("Failed to fetch Google profile data.");
        });
}



//  Services

let cart = {};

function showCounter(btn) {
    const container = btn.parentElement;
    const counterPill = container.querySelector('.counter-pill');

    btn.style.display = 'none';
    counterPill.style.display = 'flex';

    const card = container.closest(".service-card");
    const name = card.getAttribute("data-name");
    const price = parseInt(card.getAttribute("data-price"));
    const timeLimit = card.getAttribute("data-time") || "30-40 min (MAX)";

    if (!cart[name]) {
        cart[name] = { count: 1, price: price, timeLimit: timeLimit };
    } else {
        cart[name].count++;
    }

    counterPill.querySelector('span').innerText = cart[name].count;
    updateCartUI();
}

function updateCount(btn, change) {
    const counterPill = btn.parentElement;
    const container = counterPill.parentElement;
    const addBtn = container.querySelector('.add-btn');

    const span = counterPill.querySelector("span");
    let count = parseInt(span.innerText);

    count += change;

    const card = btn.closest(".service-card");
    const name = card.getAttribute("data-name");
    const price = parseInt(card.getAttribute("data-price"));
    const timeLimit = card.getAttribute("data-time") || "30-40 min (MAX)";

    if (count <= 0) {
        count = 0;
        delete cart[name];
        counterPill.style.display = 'none';
        addBtn.style.display = 'flex';
    } else {
        cart[name] = { count, price, timeLimit };
    }

    span.innerText = count;
    updateCartUI();
}

function updateCartUI() {
    const cartEmpty = document.getElementById("cartEmpty");
    const cartItems = document.getElementById("cartItems");
    const totalPrice = document.getElementById("totalPrice");
    const cartItemsPill = document.getElementById("cartItemsPill");

    cartItems.innerHTML = "";
    let total = 0;
    let totalItems = 0;

    if (Object.keys(cart).length === 0) {
        cartEmpty.style.display = "block";
        totalPrice.innerText = "0";
        if (cartItemsPill) cartItemsPill.innerText = "0 items";
        return;
    }

    cartEmpty.style.display = "none";

    const images = {
        "Utensils Cleaning": "service_utensils_icon.png",
        "Bathroom Cleaning": "service_bathroom_icon.png",
        "Mopping & Sweeping": "service_mopping_icon.png",
        "Home Dusting": "service_dusting_icon.png",
        "Fan Cleaning": "service_fan_icon.png",
        "Window Cleaning": "service_window_icon.png"
    };

    for (let item in cart) {
        let c = cart[item];
        let itemTotal = c.count * c.price;
        total += itemTotal;
        totalItems += c.count;

        const imgSrc = images[item] || "service_utensils_icon.png";

        cartItems.innerHTML += `
        <div class="cart-item-row">
            <div class="cart-item-img">
                <img src="assets/${imgSrc}" alt="${item}">
            </div>
            <div class="cart-item-details">
                <p class="cart-item-title">${item}</p>
                <p class="cart-item-sub">₹${c.price} x ${c.count}</p>
            </div>
            <div class="cart-item-price-col">
                <p class="cart-item-price">₹${itemTotal}</p>
            </div>
            <div class="cart-counter-pill">
                <button onclick="updateCountFromCart('${item}', -1)">−</button>
                <span class="cart-count-text">${c.count}</span>
                <button onclick="updateCountFromCart('${item}', 1)">+</button>
                <div class="cart-counter-label">items</div>
            </div>
        </div>
        `;
    }

    totalPrice.innerText = total;
    if (cartItemsPill) cartItemsPill.innerText = totalItems + (totalItems === 1 ? " item" : " items");
}

function updateCountFromCart(name, change) {
    if (cart[name]) {
        cart[name].count += change;
        if (cart[name].count <= 0) {
            delete cart[name];
        }
    }
    updateCartUI();
    syncFrontEndCounters();
}

function syncFrontEndCounters() {
    const allContainers = document.querySelectorAll('.add-btn-container');
    allContainers.forEach(container => {
        const name = container.getAttribute('data-name');
        const addBtn = container.querySelector('.add-btn');
        const pill = container.querySelector('.counter-pill');
        const span = pill.querySelector('span');

        if (cart[name]) {
            addBtn.style.display = 'none';
            pill.style.display = 'flex';
            span.innerText = cart[name].count;
        } else {
            addBtn.style.display = 'flex';
            pill.style.display = 'none';
            span.innerText = '0';
        }
    });
}

// CHECKOUT LOGIC
function proceedToCheckout() {
    if (Object.keys(cart).length === 0) {
        if (typeof showToast === "function") showToast("Error", "Your cart is empty!", false);
        return;
    }

    // Hide Services, Show Checkout
    document.querySelector('.services-section').style.display = 'none';
    if (document.querySelector('.why-section')) document.querySelector('.why-section').style.display = 'none';
    if (document.querySelector('.how-works-section')) document.querySelector('.how-works-section').style.display = 'none';
    if (document.querySelector('.testimonial-section')) document.querySelector('.testimonial-section').style.display = 'none';

    document.getElementById('checkoutSection').style.display = 'block';

    // Refresh Dynamic View State dynamically
    updateCheckoutUI();

    // Populate Order Summary in Checkout
    const summaryContainer = document.getElementById('checkoutSummaryItems');
    summaryContainer.innerHTML = '';

    let total = 0;
    for (let item in cart) {
        let c = cart[item];
        let itemTotal = c.count * c.price;
        total += itemTotal;

        summaryContainer.innerHTML += `
            <div class="d-flex justify-content-between mb-3 border-bottom pb-2">
                <span class="text-muted" style="font-weight: 500;">${item} (x${c.count})</span>
                <span class="font-weight-bold text-dark">₹${itemTotal}</span>
            </div>
        `;
    }

    document.getElementById('checkoutTotalAmount').innerText = total;
}

function backToServices() {
    // Hide Checkout, Show Services
    document.getElementById('checkoutSection').style.display = 'none';
    document.querySelector('.services-section').style.display = 'block';
    if (document.querySelector('.why-section')) document.querySelector('.why-section').style.display = 'block';
    if (document.querySelector('.how-works-section')) document.querySelector('.how-works-section').style.display = 'block';
    if (document.querySelector('.testimonial-section')) document.querySelector('.testimonial-section').style.display = 'block';

    // Scroll smoothly to services
    document.querySelector('.services-section').scrollIntoView({ behavior: 'smooth' });
}

// SLOT BOOKING MODAL & WHATSAPP REDIRECT ARCHITECTURE
let selectedTimeSlot = null;

// UTILS FOR ADDRESS
function loadSavedAddresses() {
    if(!currentUser) return [];
    let addrs = localStorage.getItem('bloorush_userAddresses_' + currentUser.email);
    return addrs ? JSON.parse(addrs) : [];
}
function saveNewAddress(addrStr) {
    if(!currentUser) return;
    let addrs = loadSavedAddresses();
    if(!addrs.includes(addrStr)) {
        addrs.push(addrStr);
        localStorage.setItem('bloorush_userAddresses_' + currentUser.email, JSON.stringify(addrs));
    }
}
function toggleNewAddressForm() {
    const form = document.getElementById('newAddressForm');
    const btn = document.getElementById('toggleAddressBtn');
    if(form.style.display === 'none') {
        form.style.display = 'block';
        btn.innerText = "- Cancel New Address";
    } else {
        form.style.display = 'none';
        btn.innerText = "+ Add New Address";
    }
}

function openSlotBooking() {
    // Geofence Interceptor
    const userLocation = (document.getElementById("locationText").innerText || "").toLowerCase();
    const isAvailable = userLocation.includes("nagpur") || userLocation.includes("shahjahanpur");
    
    if (!isAvailable) {
        $('#locationErrorModal').modal('show');
        return;
    }

    if (!currentUser) {
        if (typeof showToast === "function") showToast("Authentication Required", "Please log in using the form on the left to book a slot.", false);
        return;
    }

    if (Object.keys(cart).length === 0) {
        if (typeof showToast === "function") showToast("Empty Cart", "Please add services to your cart first.", false);
        return;
    }

    let totalAmount = 0;
    for (let item in cart) {
        totalAmount += cart[item].count * cart[item].price;
    }

    // Setup Address UI
    document.getElementById('newAddressForm').style.display = 'none';
    const savedAddressBlock = document.getElementById('savedAddressBlock');
    const toggleAddrBtn = document.getElementById('toggleAddressBtn');
    const addresses = loadSavedAddresses();
    
    if (addresses.length > 0) {
        let h = '';
        addresses.forEach((ad, idx) => {
            h += `<div class="form-check mb-1">
                    <input class="form-check-input" type="radio" name="savedAddressRadio" id="addrRadio${idx}" value="${ad}" ${idx===0 ? 'checked' : ''}>
                    <label class="form-check-label text-muted" style="font-size: 0.85rem;" for="addrRadio${idx}">${ad}</label>
                  </div>`;
        });
        savedAddressBlock.innerHTML = h;
        savedAddressBlock.style.display = 'block';
        toggleAddrBtn.innerText = "+ Add New Address";
        toggleAddrBtn.style.display = 'inline-block';
    } else {
        savedAddressBlock.style.display = 'none';
        document.getElementById('newAddressForm').style.display = 'block';
        toggleAddrBtn.style.display = 'none'; // Force they write an address
    }

    // Default Date to Today
    document.getElementById('bookingDate').valueAsDate = new Date();

    // Reset slots
    document.querySelectorAll('.slot-item').forEach(el => el.classList.remove('selected'));
    selectedTimeSlot = null;

    // Inject Total into Slot Modal
    document.getElementById('slotModalTotalAmount').innerText = totalAmount;

    // Show Interactive Modal
    $('#slotBookingModal').modal('show');
}

function selectSlot(element) {
    document.querySelectorAll('.slot-item').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');
    selectedTimeSlot = element.innerText;
}

function confirmWhatsAppBooking(btn) {
    if (!selectedTimeSlot) {
        if (typeof showToast === "function") showToast("Slot Required", "Please select a time slot first.", false);
        else alert("Please select a time slot first.");
        return;
    }

    // Extract Address logic
    let finalAddress = "";
    if (document.getElementById('newAddressForm').style.display === 'block') {
        const h = document.getElementById('addrHouse').value.trim();
        const f = document.getElementById('addrFloor').value.trim();
        const s = document.getElementById('addrStreet').value.trim();
        
        if(!h || !s) {
            alert("House Number and Street Name are required for new addresses!");
            return;
        }
        finalAddress = `House: ${h}, Floor: ${f || 'N/A'}, Street: ${s}`;
        saveNewAddress(finalAddress);
    } else {
        const selectedRadio = document.querySelector('input[name="savedAddressRadio"]:checked');
        if(selectedRadio){
            finalAddress = selectedRadio.value;
        } else {
            alert("Please provide or select a service address.");
            return;
        }
    }

    // Extract Date
    const chosenDate = document.getElementById('bookingDate').value;
    if(!chosenDate) {
        alert("Please select a preferred date.");
        return;
    }

    let totalAmount = document.getElementById('slotModalTotalAmount').innerText;
    let itemsList = [];
    for (let item in cart) {
        // Output format matching user prompt
        itemsList.push(`*${item} (x${cart[item].count})*\n${cart[item].price} rs\n${cart[item].timeLimit || '30-40 min (MAX)'}`);
    }

    const message = `Hello Bloorush!
I am ${currentUser.name}, and I would like to pre-book the following premium services:

${itemsList.join('\n\n')}

*Total Estimate:* ₹${totalAmount}

*Customer Location:*
${finalAddress}
*Map Link:* https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(finalAddress)}

*Preferred Date:* ${chosenDate}
*Preferred Time Slot:* ${selectedTimeSlot}

Please confirm my booking!`;

    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/918010687985?text=${encodedMessage}`;

    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Redirecting to WhatsApp...';
    btn.disabled = true;

    setTimeout(() => {
        // Complete the system booking to save to History Table
        completeBooking("wa_" + Math.random().toString(36).substring(2, 10));
        $('#slotBookingModal').modal('hide');
        
        // Push user to WhatsApp!
        window.open(whatsappUrl, '_blank');
        
        // Reset button
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 1000);
}

function completeBooking(paymentId) {
    // 1. Generate Specific Booking ID natively
    const bookingId = "#BR-" + Math.floor(100000 + Math.random() * 900000);

    let totalAmount = 0;
    let itemsListHtml = '';
    let parsedItems = [];

    for (let item in cart) {
        let c = cart[item];
        totalAmount += c.count * c.price;
        parsedItems.push({ name: item, count: c.count, price: c.price });

        itemsListHtml += `
            <div class="receipt-item d-flex justify-content-between mb-2">
                <span>${item} (x${c.count})</span>
                <span class="font-weight-bold" style="color:#2c3e50;">₹${c.price * c.count}</span>
            </div>
        `;
    }

    // --- WRITE TO PERSISTENT DATABASE ---
    const primaryService = parsedItems.length > 0 ? parsedItems[0].name : "Premium Services";
    const serviceTitle = parsedItems.length > 1 ? primaryService + " + " + (parsedItems.length - 1) + " more" : primaryService;

    const newBooking = {
        id: bookingId,
        service: serviceTitle,
        date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
        total: totalAmount,
        items: parsedItems
    };

    userBookings.unshift(newBooking); // Add to beginning of history payload
    localStorage.setItem('bloorush_userBookings', JSON.stringify(userBookings));

    // Refresh Tabular UI mapping locally
    if (document.getElementById('bookingModalBody')) {
        // The modal content gets re-fetched upon clicking, but just to be safe
    }

    // 2. Populate Bill Nodes
    document.getElementById('receiptBookingId').innerText = bookingId;
    document.getElementById('receiptCustomerName').innerText = currentUser ? currentUser.name : 'Customer';
    document.getElementById('receiptTotalAmount').innerText = totalAmount;

    // 3. Inject Logged Items
    document.getElementById('receiptItemsList').innerHTML = itemsListHtml;

    // 4. Trigger Master Modal overlay
    $('#successModal').modal('show');

    // 5. Hard Reset the Shopping Cart
    cart = {};
    updateCartUI();
    syncFrontEndCounters();

    // Automatically redirect back to the home view underneath the overlay
    backToServices();
}