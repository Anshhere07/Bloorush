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

// OPEN BOOKINGS
function openBookings(e) {
    e.preventDefault();

    const body = document.getElementById('bookingModalBody');
    body.innerHTML = ''; // Clear previous content

    // You can test the "Data" view by adding objects inside this array!
    // Example: [{ service: "Home Cleaning", date: "24-Oct-2026", status: "Completed", price: "$50" }]
    const myBookings = [];

    if (myBookings && myBookings.length > 0) {
        // --- HAS DATA SCENARIO ---
        let htmlContent = '<div class="row">';
        myBookings.forEach(booking => {
            const badgeClass = booking.status === 'Completed' ? 'badge-success' : 'badge-warning';
            htmlContent += `
                <div class="col-md-6 mb-3">
                    <div class="card shadow-sm border-0" style="border-radius: 12px; background: #f8f9fa;">
                        <div class="card-body">
                            <h5 class="card-title font-weight-bold" style="color: var(--primary);">${booking.service}</h5>
                            <p class="card-text text-muted mb-1"><i class="fas fa-calendar-alt mr-2"></i>${booking.date}</p>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <span class="badge ${badgeClass} p-2">${booking.status}</span>
                                <span class="font-weight-bold" style="font-size:1.1rem;">${booking.price}</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        htmlContent += '</div>';
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
                <button class="btn btn-outline-primary mt-3 px-4 shadow-sm" style="border-radius: 8px;" data-dismiss="modal">Browse Services</button>
            </div>
        `;
    }

    $('#bookingModal').modal('show');
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

// AUTH MODAL LOGIC
let isLoginMode = true;

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
        showToast("Success", "Successfully signed up! You can now log in.", true);
        logActivityToSheet(nameField, emailField, "Signed Up via Email");

        // Auto switch back to login mode
        isLoginMode = true;
        updateAuthUI();

        // Clear password field to force them to type it again to login securely
        document.querySelector('input[type="password"]').value = '';
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
            alert(`Successfully logged in as: ${userInfo.name}\nEmail: ${userInfo.email}`);

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
    
    if(!cart[name]) {
        cart[name] = { count: 1, price: price };
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

    if (count <= 0) {
        count = 0;
        delete cart[name];
        counterPill.style.display = 'none';
        addBtn.style.display = 'flex';
    } else {
        cart[name] = { count, price };
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
        if(cartItemsPill) cartItemsPill.innerText = "0 items";
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
    if(cartItemsPill) cartItemsPill.innerText = totalItems + (totalItems === 1 ? " item" : " items");
}

function updateCountFromCart(name, change) {
    if(cart[name]) {
        cart[name].count += change;
        if(cart[name].count <= 0) {
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
        
        if(cart[name]) {
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
        if(typeof showToast === "function") showToast("Error", "Your cart is empty!", false);
        return;
    }
    
    // Hide Services, Show Checkout
    document.querySelector('.services-section').style.display = 'none';
    if(document.querySelector('.why-section')) document.querySelector('.why-section').style.display = 'none';
    if(document.querySelector('.how-works-section')) document.querySelector('.how-works-section').style.display = 'none';
    if(document.querySelector('.testimonial-section')) document.querySelector('.testimonial-section').style.display = 'none';
    
    document.getElementById('checkoutSection').style.display = 'block';
    
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
    if(document.querySelector('.why-section')) document.querySelector('.why-section').style.display = 'block';
    if(document.querySelector('.how-works-section')) document.querySelector('.how-works-section').style.display = 'block';
    if(document.querySelector('.testimonial-section')) document.querySelector('.testimonial-section').style.display = 'block';
    
    // Scroll smoothly to services
    document.querySelector('.services-section').scrollIntoView({ behavior: 'smooth' });
}