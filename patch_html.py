import os

HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Firebase SDK to head
if "firebase-app.js" not in html:
    firebase_scripts = """
    <!-- Firebase SDK (v9 compat) -->
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-firestore-compat.js"></script>
"""
    html = html.replace('</head>', firebase_scripts + '</head>')


# 2. Add T&C Gate Modal (before closing body)
tc_modal = """
<!-- T&C Gate Modal -->
<div class="modal fade" id="tcGateModal" data-backdrop="static" data-keyboard="false" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="border-radius: 15px;">
      <div class="modal-header bg-primary text-white" style="border-radius: 15px 15px 0 0;">
        <h5 class="modal-title font-weight-bold"><i class="fas fa-file-contract mr-2"></i> Terms & Conditions</h5>
      </div>
      <div class="modal-body text-center p-4">
        <img src="assets/bloorush_logo.png" alt="Bloorush Logo" style="width: 80px; margin-bottom: 20px;">
        <h5 class="font-weight-bold mb-3">Welcome to Bloorush!</h5>
        <p class="text-muted" style="font-size: 0.9rem;">By continuing to use our premium cleaning services, you agree to our Terms of Service and Privacy Policy. Your trust and satisfaction are our highest priorities.</p>
        <button class="btn btn-primary btn-block mt-4" style="border-radius: 20px; font-weight: bold;" onclick="acceptTC()">I Agree & Continue</button>
      </div>
    </div>
  </div>
</div>
"""
if "tcGateModal" not in html:
    html = html.replace('<!-- Include Scripts -->', tc_modal + '\n<!-- Include Scripts -->')

# 3. Add Admin Panel UI
admin_panel = """
<!-- Admin Panel (Hidden by Default) -->
<div id="adminPanelSection" style="display: none; padding: 40px 15px; background: #f8f9fa; min-height: 100vh;">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="font-weight-bold text-primary"><i class="fas fa-cogs mr-2"></i> Admin Panel</h2>
            <button class="btn btn-outline-danger" onclick="exitAdmin()"><i class="fas fa-sign-out-alt mr-1"></i> Exit Admin</button>
        </div>
        
        <div class="row">
            <!-- Slot Manager -->
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0" style="border-radius: 15px;">
                    <div class="card-body">
                        <h5 class="font-weight-bold mb-3"><i class="far fa-clock mr-2 text-primary"></i> Slot Capacity Manager</h5>
                        <p class="text-muted" style="font-size: 0.85rem;">Manage available slots for a specific date.</p>
                        
                        <input type="date" id="adminSlotDate" class="form-control mb-3" onchange="loadAdminSlots()">
                        
                        <div id="adminSlotsContainer">
                            <p class="text-muted text-center py-4"><small>Select a date to manage slots.</small></p>
                        </div>
                        
                        <button class="btn btn-primary btn-block mt-3" onclick="saveAdminSlots()">Save Capacity</button>
                    </div>
                </div>
            </div>
            
            <!-- Coupon Manager -->
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0" style="border-radius: 15px;">
                    <div class="card-body">
                        <h5 class="font-weight-bold mb-3"><i class="fas fa-ticket-alt mr-2 text-primary"></i> Coupon Manager</h5>
                        <p class="text-muted" style="font-size: 0.85rem;">Create or disable promotional coupons.</p>
                        
                        <div class="input-group mb-3">
                            <input type="text" id="newCouponCode" class="form-control" placeholder="Coupon Code (e.g., FESTIVE50)">
                            <input type="number" id="newCouponDiscount" class="form-control" placeholder="₹ Discount">
                            <div class="input-group-append">
                                <button class="btn btn-success" onclick="createCoupon()">Create</button>
                            </div>
                        </div>
                        
                        <hr>
                        <div id="adminCouponsContainer">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""
if "adminPanelSection" not in html:
    html = html.replace('<!-- Checkout Section (Hidden by Default) -->', admin_panel + '\n<!-- Checkout Section (Hidden by Default) -->')

# 4. Add Admin Footer Link
footer_admin = """
            <div class="col-md-3 mb-4">
                <h5 class="font-weight-bold">Legal</h5>
                <ul class="list-unstyled">
                    <li><a href="#" class="text-white" style="text-decoration: none;">Privacy Policy</a></li>
                    <li><a href="#" class="text-white" style="text-decoration: none;">Terms of Service</a></li>
                    <li><a href="#" class="text-white" style="text-decoration: none; opacity: 0.3;" onclick="promptAdminLogin(event)">Admin Access</a></li>
                </ul>
            </div>
"""
# Replace the Legal section in footer
if "promptAdminLogin" not in html:
    # Need to find the legal section safely
    import re
    html = re.sub(r'<div class="col-md-3 mb-4">\s*<h5 class="font-weight-bold">Legal</h5>\s*<ul class="list-unstyled">.*?</ul>\s*</div>', footer_admin, html, flags=re.DOTALL)

# 5. OpenStreetMap Address Lookup + Coupon Input in Slot Booking Modal
# Find the address section inside slotBookingModal
osm_input = """
                    <!-- Address Lookup -->
                    <div class="mb-3">
                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-map-marker-alt mr-2"></i>Service Address</label>
                        
                        <div class="input-group mb-2">
                            <input type="text" id="osmAddressInput" class="form-control" placeholder="Search address via OpenStreetMap..." style="border-radius: 8px 0 0 8px;">
                            <div class="input-group-append">
                                <button class="btn btn-primary" onclick="searchOSMAddress()" style="border-radius: 0 8px 8px 0;"><i class="fas fa-search"></i></button>
                            </div>
                        </div>
                        <div id="osmResults" class="list-group mb-3" style="max-height: 150px; overflow-y: auto; display: none;"></div>
"""
if "osmAddressInput" not in html:
    html = html.replace('<div class="mb-3">\n                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-map-marker-alt mr-2"></i>Service Address</label>', osm_input)


coupon_input = """
                    <!-- Coupon Code -->
                    <div class="mb-3 p-3 bg-light" style="border-radius: 12px; border: 1px dashed #ccc;">
                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-ticket-alt mr-2"></i>Apply Coupon</label>
                        <div class="input-group">
                            <input type="text" id="couponInput" class="form-control text-uppercase" placeholder="Enter Code">
                            <div class="input-group-append">
                                <button class="btn btn-outline-primary" id="applyCouponBtn" onclick="applyCoupon()">Apply</button>
                            </div>
                        </div>
                        <small id="couponMessage" class="form-text text-success" style="display:none;"></small>
                    </div>

                    <div class="mb-3">
                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="far fa-calendar-alt mr-2"></i>Preferred Date</label>
"""
if "couponInput" not in html:
    html = html.replace('<div class="mb-3">\n                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="far fa-calendar-alt mr-2"></i>Preferred Date</label>', coupon_input)

# Let's ensure the slot items container is dynamically recognizable
html = html.replace('<div class="d-flex flex-wrap gap-2">', '<div class="d-flex flex-wrap gap-2" id="dynamicSlotsContainer">')

# Also increment version to v8 to break cache
html = html.replace('script.js?v=7', 'script.js?v=8')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated with Firebase, T&C Gate, Admin Panel, OSM, and Coupon UI.")
